# SEO.ZAIDLY AI

MVP: AI yang otomatis membuat artikel SEO, mempublikasikannya ke WordPress, lalu auto-post ke Threads.

Prinsip pengembangan: **Build, validate, then optimize.** Bangun hal paling sederhana yang berfungsi; generalisasi hanya saat terbukti perlu dari penggunaan nyata.

## Arsitektur

```
backend/   Django — SaaS layer (auth, dashboard, project, billing, API)
hermes/    AI worker — eksekusi tugas (menyusul, Fase 2)
docker/    Dockerfile & konfigurasi container
```

- `backend` = pusat aplikasi (state, billing, API).
- `hermes` = AI worker yang poll job dari backend API, eksekusi, kirim hasil. **Tidak boleh `import django`** — komunikasi hanya via HTTP API.

## Status

**Fase 1 — Foundation (selesai):** monorepo + Docker, auth (email + Google), tenant per user, project, dashboard shell.

**Fase 2 — Generate Judul SEO (selesai):** keyword → 25 judul SEO via Hermes worker, approve/reject per judul, HTMX polling.

**Fase 3 — Generate Artikel + Gambar (selesai):** judul yang disetujui → artikel Markdown ~1200 kata + meta description + optional featured image (DALL-E).

**Fase 4 — Publish WordPress (selesai):** WP credentials per project (Application Password), tombol "Publish ke WordPress" di halaman artikel, Hermes konvert Markdown → HTML dan POST ke WP REST API.

Fase berikutnya: 5) billing (Mayar.id) + launch.

## Menjalankan (Docker)

```bash
cp .env.example .env        # sesuaikan SECRET_KEY dll
docker compose up --build
# buka http://localhost:8000
```

## Menjalankan (lokal, tanpa Docker)

```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Tanpa `DATABASE_URL`, backend memakai SQLite untuk dev cepat. Dengan Docker, memakai PostgreSQL.
