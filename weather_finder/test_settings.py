from weather_finder.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}


OPEN_WEATHER_RESPONSE_CACHE_TIMEOUT = 10
OPEN_WEATHER_API_CACHE_VERSION = 1