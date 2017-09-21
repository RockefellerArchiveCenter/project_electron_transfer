"""
Django settings for project_electron project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from project_electron import config as CF

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=*+t-qchu_$#hhf9m-n45s7p=@n46(zmf^mof$+cdaa0t6h8pq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CF.DEBUG

ALLOWED_HOSTS = CF.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rac_user',
    'transfer_app',
    'orgs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_electron.urls'

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

LOGIN_REDIRECT_URL = 'app_home'

WSGI_APPLICATION = 'project_electron.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': CF.db_configs,
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'orgs.User'
LOGIN_REDIRECT_URL = '/app'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = CF.TIME_ZONE

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = CF.STATIC_ROOT

ORG_ROOT_DIR = CF.ORG_ROOT_DIR


import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

#-----------------------------------------------------------------------------#
#
#   LDAP Settings
#
#-----------------------------------------------------------------------------#

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT:    CF.LDAP_OPTIONS_X_TLS_REQUIRE_CERT,
    ldap.OPT_REFERRALS:             CF.LDAP_OPTIONS_REFERRALS,
}
AUTH_LDAP_SERVER_URI =          CF.AUTH_LDAP_SERVER_URI
AUTH_LDAP_BIND_DN =             CF.AUTH_LDAP_BIND_DN
AUTH_LDAP_BIND_PASSWORD =       CF.AUTH_LDAP_BIND_PASSWORD
AUTH_LDAP_ALWAYS_UPDATE_USER =  CF.AUTH_LDAP_ALWAYS_UPDATE_USER
AUTH_LDAP_USER_SEARCH =     LDAPSearch(CF.LDAP_SEARCH_DN, ldap.SCOPE_SUBTREE, CF.LDAP_SEARCH_REGEX)



#django CRON
INSTALLED_APPS += [
    'django_cron'
]

CRON_CLASSES = [
    "transfer_app.cron.MyCronJob",
]

UPLOAD_LOG_FILE = CF.UPLOAD_LOG_FILE