import os

try:
    from dotenv import load_dotenv

    # Load hermes/.env regardless of the current working directory.
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:  # python-dotenv optional at runtime
    pass

# Backend (Django) job API
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
HERMES_API_TOKEN = os.environ.get("HERMES_API_TOKEN", "dev-hermes-token")
POLL_INTERVAL = float(os.environ.get("POLL_INTERVAL", "3"))

# AI provider — OpenAI-compatible (default: SumoPod)
AI_BASE_URL = os.environ.get("AI_BASE_URL", "https://ai.sumopod.com/v1")
AI_API_KEY = os.environ.get("AI_API_KEY", "")
AI_TEXT_MODEL = os.environ.get("AI_TEXT_MODEL", "gpt-4o-mini")
# Set to e.g. "dall-e-3" to enable image generation; leave empty to skip.
AI_IMAGE_MODEL = os.environ.get("AI_IMAGE_MODEL", "")
