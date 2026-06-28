"""generate_article task: title + project context → full SEO article."""
import json
import re

SYSTEM = (
    "Kamu adalah penulis konten SEO profesional berbahasa Indonesia. "
    "Kamu menulis artikel panjang, informatif, ramah SEO, dan enak dibaca. "
    "Gunakan Markdown untuk format artikel."
)


def _build_prompt(title, keyword, n_words, project):
    return (
        f'Tulis artikel SEO lengkap dengan judul: "{title}"\n\n'
        f"Konteks:\n"
        f"- Keyword utama: {keyword}\n"
        f"- Niche: {project.get('niche') or '-'}\n"
        f"- Bahasa: {project.get('language') or 'Indonesia'}\n"
        f"- Gaya bahasa: {project.get('tone') or 'informatif'}\n"
        f"- Target pembaca: {project.get('target_audience') or 'umum'}\n\n"
        f"Panjang target: sekitar {n_words} kata.\n\n"
        "Struktur artikel (Markdown):\n"
        "- 2-3 paragraf pembuka\n"
        "- 3-5 section dengan heading ## (H2), sub-section ### (H3) jika perlu\n"
        "- Paragraf kesimpulan\n\n"
        "Setelah artikel selesai, tambahkan satu baris kosong lalu blok JSON berikut:\n"
        "```json\n"
        '{"meta_description": "...", "image_prompt": "..."}\n'
        "```\n"
        "- meta_description: ringkasan 120-155 karakter untuk metatag SEO\n"
        "- image_prompt: prompt bahasa Inggris untuk generate featured image\n\n"
        "PENTING: Tulis artikel terlebih dahulu, JSON hanya di bagian paling akhir."
    )


def _parse(content):
    body = content
    meta_description = ""
    image_prompt = ""

    match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.S)
    if match:
        body = content[: match.start()].strip()
        try:
            data = json.loads(match.group(1))
            meta_description = str(data.get("meta_description") or "")[:160]
            image_prompt = str(data.get("image_prompt") or "")
        except (json.JSONDecodeError, AttributeError):
            pass
    else:
        # Fallback: bare JSON object near the end
        tail = content[-2000:]
        m2 = re.search(r'\{[^{}]*"meta_description"[^{}]*\}', tail, re.S)
        if m2:
            idx = content.rfind(m2.group(0))
            body = content[:idx].strip()
            try:
                data = json.loads(m2.group(0))
                meta_description = str(data.get("meta_description") or "")[:160]
                image_prompt = str(data.get("image_prompt") or "")
            except (json.JSONDecodeError, AttributeError):
                pass

    return {
        "body": body,
        "meta_description": meta_description,
        "image_prompt": image_prompt,
        "word_count": len(body.split()),
    }


def run(payload, gateway):
    title = payload.get("title", "")
    keyword = payload.get("keyword", "")
    n_words = int(payload.get("n_words") or 1200)
    project = payload.get("project") or {}

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": _build_prompt(title, keyword, n_words, project)},
    ]
    content = gateway.generate_text(messages, temperature=0.7, max_tokens=4000)
    result = _parse(content)

    featured_image_url = ""
    if result["image_prompt"]:
        try:
            featured_image_url = gateway.generate_image(result["image_prompt"])
        except Exception:
            pass
    result["featured_image_url"] = featured_image_url

    return result
