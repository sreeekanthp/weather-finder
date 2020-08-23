from weather_finder.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

OPEN_WEATHER_API_BASE_URL = 'http://api.openweathermap.org/data/2.5/'
WEATHER_API_CACHE_VERSION = 1
WEATHER_RESPONSE_CACHE_TIMEOUT = 600
CITY_RESPONSE_CACHE_TIMEOUT = 600
CITY_API_CACHE_VERSION = 1
LANGUAGES = [('en', 'English')]
