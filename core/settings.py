"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from dotenv import load_dotenv


from pathlib import Path
from decouple import config
import cloudinary_storage

# load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7ambc$gr*q#fz_nqis$&6p)0r8e&-&&ai-h^*x$-abiq7@2bsl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [

    # 'social_django',
    'rest_framework_social_oauth2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    'users',
    'events',
    'drf_yasg',
    "corsheaders",
    'comments',

    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # drf-social-oauth2
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    'cloudinary',
    'cloudinary_storage',
    # 'notifications',
]

# drf-social-oauth2
ACTIVATE_JWT = True

# AUTH_USER_MODEL = 'users.UserSocialAuth'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.utils.CsrfExemptSessionAuthentication',

        # drf-social-oauth2
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        'drf_social_oauth2.authentication.SocialAuthentication',
    ),
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # )
}

AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.google.GoogleOAuth2',

    # drf-social-oauth2
    'social_core.backends.google.GoogleOAuth2',
    'drf_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
# localhost
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '188658735176-jhpmkjvo54mhdd0pqdnkcqvtc22oqidk.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '188658735176-jhpmkjvo54mhdd0pqdnkcqvtc22oqidk.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
# development
#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '552452171826-cmqllqfietp2rmie1er2oj063b1p5cil.apps.googleusercontent.com'
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'


# drf-social-oauth2
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


SESSION_COOKIE_SAMESITE = None
# LOGIN_URL = 'login'
#LOGIN_REDIRECT_URL = 'https://zuri-events-app.vercel.app/timeline'
LOGIN_REDIRECT_URL = 'https://zuri-events-app.vercel.app/timeline'

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


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "https://zuri-events-app.vercel.app",
    "http://localhost:3000",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS"
]

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

                # drf-social-oauth2
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': config('PGDATABASE'),
    #     'USER': config('PGUSER'),
    #     'PASSWORD': config('PGPASSWORD'),
    #     'HOST': config('PGHOST'),
    #    'PORT': '5432',
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'neondb',
    #     'USER': 'oluwatimileyin0518',
    #     'PASSWORD': 'j6m8DUgQMiuR',
    #     'HOST': 'ep-dawn-resonance-23183028.us-east-2.aws.neon.tech',
    #     'PORT': '5432',
    # }
}


# DB_PW = os.getenv('DB_PW')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'events',
#         'USER': 'root',
#         'PASSWORD': DB_PW,
#         'HOST':'localhost',
#         'PORT':'3306',
#         'OPTIONS':{
#             'autocommit':True
#         }
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "relative_paths": False,
    "DISPLAY_OPERATION_ID": False,
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
}




MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dy2kqg5by',
    'API_KEY': '961195596386852',
    'API_SECRET': '9zsRt1gqO3nQhE_XEzteg1dwFCU'
}


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

NOTIFICATIONS_SOFT_DELETE = False
NOTIFICATIONS_USE_JSONFIELD = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'