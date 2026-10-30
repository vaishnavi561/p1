import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# P1-01: Dynamically load allowed hosts from environment variables (comma-separated)
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    'api',
]
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'medlife_db'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'MedlifeAi@123'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# P1-01: Restrict CORS origins in production instead of trusting all websites
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() in ('true', 't', '1')
cors_origins_env = os.getenv('CORS_ALLOWED_ORIGINS', '')
if cors_origins_env:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(',') if origin.strip()]
else:
    CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173']
CORS_ALLOW_CREDENTIALS = True    

# P1-01: Production Security & HTTPS Hardening Headers (Active only when DEBUG = False)
# --- P1-11: PRODUCTION SECURITY HEADERS & HTTPS ENFORCEMENT ---
if not DEBUG:
    # Force HTTPS redirect
    SECURE_SSL_REDIRECT = True
    
    # HTTP Strict Transport Security (HSTS)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Browser security filters
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Secure cookies in production
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ---------------------------------------------------------
# SMTP Email Configuration (IONOS, loaded from .env)
# ---------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('SMTP_HOST') or os.environ.get('EMAIL_HOST', 'smtp.ionos.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', 't', '1')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
EMAIL_TIMEOUT = 20  # seconds, so a bad SMTP setup fails fast instead of hanging

# Used to build the reset link sent in emails
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.CookieJWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'auth': '5/minute',
    }
    
}

# --- P1-13: SESSION & CSRF COOKIE HARDENING ---
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # False so frontend JS can read the csrftoken cookie for request headers
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Enforce secure cookies in production (HTTPS only)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True