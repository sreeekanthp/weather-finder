import requests
import logging

from django.conf import settings

from api.v1.exceptions import ExternalAPIError
from api.v1.transformers import OpenWeatherMapCityResponseSchema
from api.v1.transformers import OpenWeatherMapWeatherResponseSchema

logger = logging.getLogger(__name__)


class BaseOpenWeatherMapClient:
    """ Base client class to communicate with openweathermap apis """

    def __init__(self, api_key, language='en'):
        self.api_key = api_key
        self.language = language

    def get_url(self, *args, **kwargs):
        raise NotImplementedError

    def get_serialized_data(self, data):
        raise NotImplementedError

    def get_data(self, *args, **kwargs):
        url = self.get_url(*args, **kwargs)
        response = requests.get(url, timeout=settings.OPEN_WEATHER_API_TIMEOUT)
        try:
            response.raise_for_status()
        except requests.Timeout:
            logger.exception('OpenWeatherMap request timed out')
            raise ExternalAPIError
        except requests.RequestException:
            logger.exception('OpenWeatherMap request failed')
            raise ExternalAPIError

        data = response.json()
        return self.get_serialized_data(data)


class OpenWeatherMapWeatherClient(BaseOpenWeatherMapClient):
    """ Client class to get the weather details of given city using openweathermap api """

    def get_url(self, *args, **kwargs):
        return f"{settings.OPEN_WEATHER_API_BASE_URL}weather?id={kwargs['city_id']}&lang={self.language}&appid={self.api_key}&units=metric"

    def get_serialized_data(self, data):
        # TODO: What if the expected response from external api changes changes
        return OpenWeatherMapWeatherResponseSchema().dump(data)


class OpenWeatherMapCityListClient(BaseOpenWeatherMapClient):
    """ Client class to get the list of cities using openweathermap api """

    def get_url(self, query):
        return f"{settings.OPEN_WEATHER_API_BASE_URL}find?q={query}&lang={self.language}&appid={self.api_key}"

    def get_serialized_data(self, data):
        return OpenWeatherMapCityResponseSchema().dump(data['list'], many=True)
