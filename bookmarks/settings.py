"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pem7+_&do=%r39$j$p7si)2i%p$pd7u*te9bn9mno4ywt7@^_4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# THUMBNAIL_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'smafy.com', '0.0.0.0', 'smaffy.com']

SITE_ID = 1


# Application definition

INSTALLED_APPS = [
    'sslserver',            # runsslserver smaffy.com:8888, 0.0.0.0:8888
    'pytils',               # russian

    'account.apps.AccountConfig',
    'images.apps.ImagesConfig',
    'actions.apps.ActionsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',      # follow
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'phonenumber_field',
    'social_django',
    'sorl.thumbnail',
    'redis',
    'taggit',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'bookmarks.middleware.MySocialAuthExceptionMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'accounts',
        'USER': 'smafy',
        'PASSWORD': 'Pb53402505*',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# auth

LOGIN_REDIRECT_URL = 'profile'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'rudakovapraha@gmail.com'
EMAIL_HOST_PASSWORD = 'aa987654'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

"""
send_mail('Django mail', 'This e-mail was sent with Django.', 'rudakovacz@gmail.com', ['kate@itpeople.ee'], fail_silently=False)
"""

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',

    'account.authentication.EmailAuthBackend',
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    # 'django.contrib.auth.backends.ModelBackend',

]


SOCIAL_AUTH_FACEBOOK_KEY = '1231471283677887'                       # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'fd25cb7aacb45c58538e4963bd9bba3b'    # Facebook App Secret

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, picture'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
    ('name', 'name'),
    ('email', 'email'),
    ('photo', 'picture'),
    ('link', 'profile_url'),
]


SOCIAL_AUTH_TWITTER_KEY = 'MuwxaFEU05NNeemTpYiBW1P5c'               # Twitter Consumer Key
SOCIAL_AUTH_TWITTER_SECRET = 'Ffw6UxxemIViI9LhP71QUOMR2CehTfoRLARrMEG8es9FDBttr3'    # Twitter Consumer Secret

SOCIAL_AUTH_TWITTER_SCOPE = ['email']
SOCIAL_AUTH_TWITTER_PROFILE_EXTRA_PARAMS = {
    'fields': 'email',
}
TWITTER_EXTENDED_PERMISSIONS = ['email']
TWITTER_EXTRA_DATA = [('email', 'email'), ]


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '783394098930-osgm0hvf6a58doshb12ppv0r98senrcu.apps.googleusercontent.com'  # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'jWxcAyTlvG42Zx1oaEfSx0SQ'       # Google Consumer Secret

SOCIAL_AUTH_LOGIN_ERROR_URL = '/account/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/account/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'account.social.get_or_create_profile',
    'account.social.save_profile_picture',
)

from django.urls import reverse_lazy

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1


TAGGIT_CASE_INSENSITIVE = True
