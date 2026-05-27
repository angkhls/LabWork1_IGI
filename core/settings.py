import os
from pathlib import Path
import cloudinary


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-@factory-key-for-lab5-development-only')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if _csrf:
    CSRF_TRUSTED_ORIGINS = [x.strip() for x in _csrf.split(',') if x.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    'cloudinary_storage', 
    'django.contrib.staticfiles',
    'cloudinary',          # ← добавь
    'factory',
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

ROOT_URLCONF = 'core.urls'

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
        'factory.context_processors.factory_global_context',
    ],
},
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Указываем, где Django искать статику локально
STATICFILES_DIRS = [BASE_DIR / 'static']

# Куда собирать все файлы перед отправкой на сервер (для Render)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# URL для доступа к статике
STATIC_URL = '/static/'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

def _build_database_config():
    """
    Локально (без переменных Postgres) — SQLite.
    На хостинге — PostgreSQL через POSTGRES_* или DATABASE_URL (Render, Railway).
    """
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': parsed.path.lstrip('/'),
                'USER': parsed.username,
                'PASSWORD': parsed.password,
                'HOST': parsed.hostname,
                'PORT': str(parsed.port or 5432),
            }
        }

    if os.environ.get('POSTGRES_DB'):
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('POSTGRES_DB', 'furniture_db'),
                'USER': os.environ.get('POSTGRES_USER', 'furniture_user'),
                'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'furniture_pass'),
                'HOST': os.environ.get('POSTGRES_HOST', 'db'),
                'PORT': os.environ.get('POSTGRES_PORT', '5432'),
            }
        }

    return {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


DATABASES = _build_database_config()

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Уровень логов задаётся переменной окружения DJANGO_LOG_LEVEL (DEBUG, INFO, WARNING, ERROR).
LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} — {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'factory.log',
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'factory': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
