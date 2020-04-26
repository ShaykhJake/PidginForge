DEVMODE = False
"""
Django settings for pidginforge project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
if not DEVMODE:
    import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if not DEVMODE:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['pidginforge-1.eba-q824jzfn.us-west-2.elasticbeanstalk.com',
                 'pidginforge.herokuapp.com',
                 'pidginforge.org', 
                 '127.0.0.1',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'rest_framework',
    'rest_framework.authtoken',

    'django_registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # TODO Implement Social Media Login
    # 'allauth.socialaccount.providers.facebook'
    # 'allauth.socialaccount.providers.twitter'
    
    'crispy_forms',
    'webpack_loader',

    'rest_auth',
    'rest_auth.registration',

    'corsheaders',

    'users',
    'questions',
    'storages',
    'categories',
    'elements',
    'malapropos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://localhost:8080',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8080',
)

ROOT_URLCONF = 'pidginforge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(FRONTEND_DIR, 'dist')],
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
WSGI_APPLICATION = 'pidginforge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# If in development mode, connect to the test database on Amazon RDS; otherwise connect to production on Heroku
if DEVMODE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('RDS_NAME'),
            'USER': os.environ.get('RDS_USER'),
            'PASSWORD': os.environ.get('RDS_PASSWORD'),
            'HOST': os.environ.get('RDS_HOST'),
            'PORT': os.environ.get('RDS_PORT'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#### Custom User Authentication
# Custom User Model
AUTH_USER_MODEL = "users.CustomUser"

# Django-Crispy-Forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

# django.contrib.sites
SITE_ID = 1

# django-allauth
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# if the following is set "NONE", then no username is actually allowed, if not, it is optional with ACCOUNT Username Required = False
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 # 1 day in seconds
#  ACCOUNT_LOGOUT_REDIRECT_URL ='/accounts/login/'
# LOGIN_REDIRECT_URL = '/accounts/email/' # default to /accounts/profile
# LOGIN_URL = "accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


#### AWS STORAGE SERVICES
AWS_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# Development

####### For Serving Static Files
# Testing & Dev
# STATIC_URL = '/staticfiles/'
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticfiles")
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static") # This will be the absolute path.

# Production:
AWS_STATIC_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
STATICFILES_STORAGE = 'pidginforge.storage_backends.StaticStorage'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    # os.path.join(BASE_DIR, "frontend/dist"),
    # os.path.join(FRONTEND_DIR, "dist"),
    # os.path.join(FRONTEND_DIR, "dist/static"),
)

AWS_DEFAULT_ACL = None
AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'pidginforge.storage_backends.PublicMediaStorage'
AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'pidginforge.storage_backends.PrivateMediaStorage'

####### Email Services ########
###### SES #######
EMAIL_BACKEND = 'django_ses.SESBackend'
SES_SENDER_EMAIL = os.environ.get('SES_FROM_EMAIL')

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('S3_ACCESS_KEY_ID')
EMAIL_HOST_PASSWORD = os.environ.get('S3_SECRET_ACCESS_KEY')
DEFAULT_FROM_EMAIL = os.environ.get('SES_FROM_EMAIL')
#########



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 4
}

# https://django-rest-auth.readthedocs.io/en/latest/configuration.html
# REST_AUTH_SERIALIZERS = {
#     'LOGIN_SERIALIZER': 'path.to.custom.LoginSerializer',
#     'TOKEN_SERIALIZER': 'path.to.custom.TokenSerializer',
#     ...
# }

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(FRONTEND_DIR, 'webpack-stats.json'),
    }
}

# Activate Django-Heroku
if not DEVMODE:
    django_heroku.settings(locals(), staticfiles=False)