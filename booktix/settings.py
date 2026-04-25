"""
Django settings for BookTix — Event Ticket Booking System.
"""

import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
IS_VERCEL = bool(os.environ.get('VERCEL'))

SECRET_KEY = config(
    'SECRET_KEY',
    default='booktix-demo-secret-key-change-this-in-vercel-environment-2026'
)

DEBUG = config('DEBUG', default=not IS_VERCEL, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1,testserver,.vercel.app,booktixs.vercel.app'
).split(',')
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://*.vercel.app,https://booktixs.vercel.app'
).split(',')
SITE_URL = config('SITE_URL', default='https://booktixs.vercel.app' if IS_VERCEL else 'http://localhost:8000')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'users',
    'events',
    'bookings',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'booktix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'booktix.wsgi.application'

DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    try:
        import dj_database_url

        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
        }
    except ImportError:
        raise RuntimeError('DATABASE_URL is set, but dj-database-url is not installed.')
else:
    sqlite_name = Path('/tmp/booktix.sqlite3') if IS_VERCEL else BASE_DIR / 'db.sqlite3'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': sqlite_name,
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=IS_VERCEL, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=IS_VERCEL, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=IS_VERCEL, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000 if IS_VERCEL else 0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=IS_VERCEL, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=IS_VERCEL, cast=bool)

# Razorpay credentials — replace with your actual keys in .env
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID', default='rzp_test_YOUR_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET', default='YOUR_KEY_SECRET')

# Email configuration (for ticket emails)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# For production, use:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_app_password'

DEFAULT_FROM_EMAIL = 'BookTix <noreply@booktix.in>'
