import os

from tdd_practice.settings.base import *
from tdd_practice.settings.base_swagger_utils import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^d*66-07r)+k7-rvvhc1c2!j*cyud&a)v69_8+d7*xg&q!5gk#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEST_ENV = True
# swagger utils

PRINT_REQUEST_RESPONSE_TO_CONSOLE = True

################# Databases ##################


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
import uuid

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'test.sqlite3'),
            'ENGINE': 'django.db.backends.sqlite3'
        }
    }
}

# ********************** Static Files *************************
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_IOT_REGION = os.environ.get('AWS_IOT_REGION', '')
