""" Django settings for hadassah project. """

import os

from envparse import Env

env = Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o3@)bpsxg1@wjt6jczcbl$v%4tkgfw+5h)x=#f%g@f9bx&bcr8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
        '.petrushkagroup.com',
        'petrushkagroup.com',
        'lk-doctor.petrushkagroup.com',
        '.petrushkagroup.ru',
        'petrushkagroup.ru',
        '158.160.15.85',
        '127.0.0.1',
        'localhost',
        'https://2a3d-178-89-129-243.ngrok-free.app',
        '2a3d-178-89-129-243.ngrok-free.app',
        '130.193.55.25'
]


CORS_ALLOWED_ORIGINS = [
    "https://sk.petrushkagroup.com",
    "https://sk.petrushkagroup.ru",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "https://b467-146-120-93-183.eu.ngrok.io",
    "http://130.193.55.25",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'nutritionist',
    'doctor',
    'patient',
    'report',
    'rest_framework',
    'djoser',
    'corsheaders',
    'django_apscheduler',
    # 'django_celery_beat',
    'widget_tweaks',
    'django_extensions',
    'drf_spectacular',
    # 'pwa',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'hadassah.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'hadassah.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str("DB_NAME", default="hadassah1"),
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
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

DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/


TIME_ZONE = 'Europe/Moscow'
# TIME_ZONE = 'Europe/Berlin' # минус 1 часа от московского
# TIME_ZONE  = 'Europe/London'  # минус 2 часа от московского

# TIME_ZONE = 'America/Sao_Paulo'
# TIME_ZONE = 'America/Noronha' # минус 5 часа от московского
# TIME_ZONE = 'America/Miquelon' # минус 6 часа от московского
# TIME_ZONE = 'America/New_York' # минус 7 часа от московского

# TIME_ZONE = 'America/Los_Angeles' # минус 10 часа от московского
# TIME_ZONE = 'Australia/Sydney'
# TIME_ZONE = 'Europe/Samara' # плюс 1 часов от московского
# TIME_ZONE = 'Asia/Shanghai' # плюс 5 часов от московского
# TIME_ZONE = 'Asia/Tokyo' # плюс 6 часов от московского
# TIME_ZONE = 'Asia/Kamchatka' # плюс 9 часов от московского
USE_I18N = True
USE_L10N = False

LANGUAGE_CODE = 'ru-RU'
DATE_FORMAT = 'd E Y'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "doctor", "static"),
    os.path.join(BASE_DIR, "nutritionist", "static"),
]

# Основной url для управления медиафайлами
MEDIA_URL = '/media/'

# Путь хранения картинок
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer', # отключить отображение в браузере
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Skolkovo PetrushkaGroup API',
    'DESCRIPTION': 'API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'info@petrushkagroup.ru'
EMAIL_HOST_PASSWORD = 'sswmlhpfnbooozkb'

AUTH_USER_MODEL = 'nutritionist.CustomUser'
# PWA_APP_DEBUG_MODE = True

PWA_APP_NAME = 'ЛК врача'
PWA_APP_DESCRIPTION = "Личный кабинет врача"
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'fullscreen'
PWA_APP_SCOPE = '/login'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/login'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': 'static/images/icons/icon-192x192.png',
        'sizes': '192x192'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/images/icons/icon-192x192.png',
        'sizes': '192x192'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/images/icons/icon.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {'class': 'logging.StreamHandler'}
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG'
#         }
#     }
# }

LOGGING = {
    'version': 1,

    'formatters': {
        'main': {
            'format': "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s - %(pathname)s"
        },
    },

    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'main',
            'filename': 'doctor/nutrition_logging.log',
            'encoding': 'utf-8'
        }
    },

    'loggers': {
        'main_logger': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

######################
# CORS HEADERS
######################

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False

# основной сервер
BOT_ID_EMERGEBCY_FOOD = '-1001913194437'

# dev-сервер
# BOT_ID_EMERGEBCY_FOOD = '-916594793'