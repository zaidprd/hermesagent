"""Development settings."""
from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Print emails (verification, password reset) to the console.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
