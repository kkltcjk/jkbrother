"""
Django settings for new_printer project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ip_address
# from easy_thumbnails.conf import Settings as thumbnail_settings
in_test_server = ip_address.in_test_server()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's!-u9ym5-^m)sf-3ecaw3o2u7%vd5ln_@hn^qu0vd(8^e3d1e9'

# SECURITY WARNING: don't run with debug turned on in production!
if not in_test_server:
    DEBUG = False 
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'designer',
    'adminer',
    'configuration',
    'social',
    'vender',
    'account',
    'payment',
    'utility',
    'compressor'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'new_printer.urls'

#session is unable when one minute is over
SESSION_COOKIE_AGE= 60*180

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

WSGI_APPLICATION = 'new_printer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if not in_test_server:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'jkbrother',
            'USER': 'root',
            'PASSWORD': 'passw0rd',
            'HOST': '120.26.38.125',
            'PORT': '3306',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'jkbrother',
            'USER': 'root',
            'HOST': '192.168.1.101',
            'PASSWORD': '1',
            'PORT': '3306',
            }
        }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh_cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

'''STATIC_URL = '/static/'

# static setting:important
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)'''


STATIC_URL = '/static/'
New_s=('/').join(os.getcwd().split('/')[0:3]) + '/static'
if not os.path.exists(New_s):
    os.mkdir(New_s)
print New_s
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    New_s,
)

LOGIN_URL = '/shop/login_register'
#AUTH_PROFILE_MODULE = 'configutation.TestUser'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

COMPRESS_ROOT = os.path.join(BASE_DIR, 'static')
COMPRESS_ENABLE = True
