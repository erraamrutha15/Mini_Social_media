"""
Django settings for the Mini Social Media Platform project.

This module contains all configuration settings for the Django application,
including database configuration, installed apps, middleware, authentication
backends, and CORS settings.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Base Directory
# ---------------------------------------------------------------------------
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Security Settings
# ---------------------------------------------------------------------------
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m1n1-s0c1al-m3d1a-pl4tf0rm-s3cr3t-k3y-2024'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts for development purposes.
ALLOWED_HOSTS = ['*']

# ---------------------------------------------------------------------------
# Application Definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',

    # Local apps
    'accounts',
    'posts',
]

# ---------------------------------------------------------------------------
# Middleware Configuration
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CorsMiddleware must be placed before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------------------------------
# URL Configuration
# ---------------------------------------------------------------------------
ROOT_URLCONF = 'socialmedia.urls'

# ---------------------------------------------------------------------------
# Templates Configuration
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# ---------------------------------------------------------------------------
# WSGI Configuration
# ---------------------------------------------------------------------------
WSGI_APPLICATION = 'socialmedia.wsgi.application'

# ---------------------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------------------
# Using SQLite for development. Switch to PostgreSQL for production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------------
# Password Validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ---------------------------------------------------------------------------
# Static Files (CSS, JavaScript, Images)
# ---------------------------------------------------------------------------
STATIC_URL = 'static/'

# ---------------------------------------------------------------------------
# Media Files (User Uploads — images, videos)
# ---------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Allow larger file uploads (50MB) for videos
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

# ---------------------------------------------------------------------------
# Default Primary Key Field Type
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------------------------
# Allow all origins for development. Restrict in production.
CORS_ALLOW_ALL_ORIGINS = True

# ---------------------------------------------------------------------------
# Django REST Framework Configuration
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
