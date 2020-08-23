from weather_finder.settings import *  # noqa: F403

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db_test.sqlite3'}}  # noqa: F405

WEATHER_API_CACHE_VERSION = 1
WEATHER_RESPONSE_CACHE_TIMEOUT = 600
CITY_API_CACHE_VERSION = 1
CITY_RESPONSE_CACHE_TIMEOUT = 600
LANGUAGES = [('en', 'English')]
