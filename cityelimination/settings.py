from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Environment mode
PROD = os.environ.get('prod') == 'true'

# Security keys
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key')

DEBUG = not PROD
ALLOWED_HOSTS = ["*"]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "minio_storage",
    "formtools"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cityelimination.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Ensure 'templates' folder exists
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cityelimination.wsgi.application"

# Database
if PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'ditto',
            'USER': 'postgres',
            'PASSWORD': 'Ashish8853@',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if PROD:
    # Production - MinIO storage
    DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
    STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"

    MINIO_STORAGE_ENDPOINT = os.environ.get('minio_endpoint')
    MINIO_STORAGE_ACCESS_KEY = os.environ.get('minio_access')
    MINIO_STORAGE_SECRET_KEY = os.environ.get('minio_secret')
    MINIO_STORAGE_USE_HTTPS = True

    MINIO_STORAGE_MEDIA_BUCKET_NAME = 'alcherce25media'
    MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
    MINIO_STORAGE_STATIC_BUCKET_NAME = 'alcherce25static'
    MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
else:
    # Development - local storage
    STATICFILES_DIRS = [BASE_DIR / "static"]
    STATIC_ROOT = BASE_DIR / "staticfiles"
    MEDIA_ROOT = BASE_DIR / "media"

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('email')
EMAIL_HOST_PASSWORD = os.environ.get('password')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

# CSRF Trusted Origins
if PROD:
    CSRF_TRUSTED_ORIGINS = [
        'https://prelims.alcheringa.in',
        'https://testprelims.alcheringa.in'
    ]
else:
    CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']
