from .base import *

DEBUG = False  # 수정
ALLOWED_HOSTS = ['*']  # 추후 배포할 호스트 주소 입력 예정
WSGI_APPLICATION = 'config.wsgi.prod.application'  # 수정
INSTALLED_APPS += []

# DATABASES = {}  추후 실제 배포시 사용할 DB 정보 입력 예정

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PROD_DB_NAME'),
        'USER': config('PROD_DB_USER'),
        'PASSWORD': config('PROD_DB_PASSWORD'),
        'HOST': config('PROD_DB_HOST'),
        'PORT': config('PROD_DB_PORT'),
    }
}