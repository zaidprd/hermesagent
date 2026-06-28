FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/

EXPOSE 8000

# Production default; docker-compose overrides command for dev (runserver).
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
