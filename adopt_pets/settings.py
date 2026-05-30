import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure--5qs*iwgzrj(_74tr^@bpa7_lsu&55_1j39@zno7cu4n0sr)(6')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'adoptpets-python-production.up.railway.app',
    '.railway.app'  # El punto al inicio funciona como comodín para cualquier subdominio
]
CSRF_TRUSTED_ORIGINS = [
    'https://adoptpets-python-production.up.railway.app',
    'https://*.railway.app',
]

# 2. Permitir que Django reconozca HTTPS a través del proxy de Railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 3. Forzar a que las cookies de CSRF viajen solo por conexiones seguras (HTTPS)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
# Application definition
INSTALLED_APPS = [
    'usuarios',
    'mascotas',
    'refugios',
    'adopciones',
    'blog',
    'reportes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'adopt_pets.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adopt_pets.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'adopcion_mascotas',
        'USER': 'root',
        'PASSWORD': 'fabian123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

_database_url = os.environ.get('DATABASE_URL') or os.environ.get('MYSQL_URL')
if _database_url:
    DATABASES['default'] = dj_database_url.config(default=_database_url)

# Custom User & Auth
AUTH_USER_MODEL = 'usuarios.Usuario'
LOGIN_REDIRECT_URL = '/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Reemplaza la línea anterior por esta:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'soporte@adoptpets.com'
