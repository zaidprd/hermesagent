# Hermes — AI Worker

Standalone worker. Polls the backend job API, runs the matching task, reports
the result. **Does not import Django** — communicates only over HTTP.

## Run

```bash
cd hermes
python -m venv .venv && . .venv/Scripts/activate   # Windows
pip install -r requirements.txt
cp .env.example .env                               # isi AI_API_KEY (SumoPod)
cd ..
python -m hermes.worker                            # jalankan dari root repo
```

## Tasks

| agent_type        | Tugas                                                  |
|-------------------|--------------------------------------------------------|
| `generate_title`  | Keyword + konteks project → judul SEO                  |
| `generate_article`  | Judul + konteks → artikel Markdown + meta description + image prompt (+ optional image) |
| `publish_wordpress` | Artikel → publish ke WordPress via REST API (Basic Auth + Application Password)          |

## Env

| Var               | Default                     | Keterangan                         |
|-------------------|-----------------------------|------------------------------------|
| `BACKEND_URL`     | `http://localhost:8000`     | URL backend Django                 |
| `HERMES_API_TOKEN`| `dev-hermes-token`          | Harus sama dengan backend          |
| `AI_BASE_URL`     | `https://ai.sumopod.com/v1` | Endpoint OpenAI-compatible         |
| `AI_API_KEY`      | —                           | API key SumoPod                    |
| `AI_TEXT_MODEL`   | `gpt-4o-mini`               | Nama model (cek tab Models SumoPod)|
| `POLL_INTERVAL`   | `3`                         | Jeda polling (detik)               |
| `AI_IMAGE_MODEL`  | —                           | Model image (mis. `dall-e-3`); kosong = skip |
