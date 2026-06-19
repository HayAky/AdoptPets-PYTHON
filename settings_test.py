from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']  # tests más rápidos
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
DEBUG = False