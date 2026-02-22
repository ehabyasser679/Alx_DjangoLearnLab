"""
Production settings for social_media_api.

Load this instead of settings.py by setting:
    DJANGO_SETTINGS_MODULE=social_media_api.settings_production

All sensitive values come from environment variables (see .env.example).
"""

import os
from .settings import *   # noqa: F401, F403 – inherit everything from base

# ──────────────────────────────────────────────────────────────────────────────
# Security
# ──────────────────────────────────────────────────────────────────────────────
DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# HTTPS / security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ──────────────────────────────────────────────────────────────────────────────
# Database  (PostgreSQL via DATABASE_URL)
# ──────────────────────────────────────────────────────────────────────────────
import dj_database_url   # pip install dj-database-url psycopg2-binary

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}

# ──────────────────────────────────────────────────────────────────────────────
# Static files  (WhiteNoise serves static files without a separate web server)
# ──────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE   # noqa: F405

STATIC_ROOT = BASE_DIR / 'staticfiles'   # noqa: F405
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ──────────────────────────────────────────────────────────────────────────────
# Media files  (use cloud storage like S3 in production)
# ──────────────────────────────────────────────────────────────────────────────
# Uncomment and configure if using django-storages + S3:
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
