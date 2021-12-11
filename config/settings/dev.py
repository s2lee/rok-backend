from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']  # 모든 호스트 허용
WSGI_APPLICATION = 'config.wsgi.dev.application'  # 수정
INSTALLED_APPS += [
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DEV_DB_NAME'),
        'USER': config('DEV_DB_USER'),
        'PASSWORD': config('DEV_DB_PASSWORD'),
        'HOST': config('DEV_DB_HOST'),
        'PORT': '',
    }
}