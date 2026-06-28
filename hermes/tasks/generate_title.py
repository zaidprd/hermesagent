"""generate_title task: turn a keyword + project context into SEO titles."""
import json
import re

SYSTEM = (
    "Kamu adalah pakar SEO dan content strategist berbahasa Indonesia. "
    "Kamu membuat judul artikel yang menarik diklik, ramah SEO, dan tidak clickbait berlebihan."
)


def _build_user_prompt(keyword, n, project):
    return (
        f'Buat {n} judul artikel SEO yang unik untuk keyword utama: "{keyword}".\n\n'
        f"Konteks project:\n"
        f"- Niche/topik: {project.get('niche') or '-'}\n"
        f"- Bahasa: {project.get('language') or 'Indonesia'}\n"
        f"- Gaya bahasa: {project.get('tone') or 'informatif'}\n"
        f"- Target pembaca: {project.get('target_audience') or 'umum'}\n\n"
        "Aturan:\n"
        f"- Setiap judul mengandung atau relevan dengan keyword \"{keyword}\".\n"
        "- Hindari judul yang saling duplikat.\n"
        "- Panjang wajar (maksimal ~70 karakter bila memungkinkan).\n"
        "- Kembalikan HANYA array JSON berisi string judul, tanpa penjelasan apa pun.\n"
        'Contoh format: ["Judul satu", "Judul dua"]'
    )


def parse_titles(content):
    """Robustly extract a list of titles from an LLM response (JSON or list)."""
    content = (content or "").strip()

    match = re.search(r"\[.*\]", content, re.S)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list):
                return [str(x).strip() for x in data if str(x).strip()]
        except json.JSONDecodeError:
            pass

    titles = []
    for line in content.splitlines():
        line = line.strip()
        # Strip only list markers ("1.", "2)", "-", "*"), not plain leading digits.
        line = re.sub(r"^\s*(?:\d+[\.\)]|[-*•])\s*", "", line)
        line = line.strip().strip('"').strip(",").strip().strip('"')
        if line and line not in ("[", "]"):
            titles.append(line)
    return titles


def run(payload, gateway):
    keyword = payload.get("keyword", "")
    n = int(payload.get("n_titles") or 25)
    project = payload.get("project") or {}

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": _build_user_prompt(keyword, n, project)},
    ]
    content = gateway.generate_text(messages, temperature=0.8)
    titles = parse_titles(content)
    return {"titles": titles[:n], "requested": n, "returned": len(titles[:n])}
