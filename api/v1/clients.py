import requests
import logging

from django.conf import settings
from requests import RequestException

from api.v1.exceptions import ExternalAPIError
from api.v1.transformers import CityListResponseSchema
from api.v1.transformers import WeatherResponseSchema

logger = logging.getLogger(__name__)


class BaseOpenWeatherMapClient:
    """Base client class to communicate with openweathermap apis"""

    def __init__(self, api_key, language=settings.LANGUAGE_CODE):
        self.api_key = api_key
        self.language = language

    def get_url(self, *args, **kwargs):
        """Return url to hit openweathermap api"""
        raise NotImplementedError

    def get_serialized_data(self, data):
        """Serialize data returned from the openweathermap api"""
        raise NotImplementedError

    def get_data(self, *args, **kwargs):
        """Get data from openweather api"""
        url = self.get_url(*args, **kwargs)
        response = requests.get(url, timeout=settings.OPEN_WEATHER_API_TIMEOUT)
        try:
            response.raise_for_status()
        except RequestException:
            logger.exception('OpenWeatherMap request failed')
            raise ExternalAPIError

        data = response.json()
        return self.get_serialized_data(data)


class OpenWeatherMapWeatherClient(BaseOpenWeatherMapClient):
    """Client class to get the weather details for given city using openweathermap api"""

    def get_url(self, *args, **kwargs):
        return f"{settings.OPEN_WEATHER_API_BASE_URL}weather?id={kwargs['city_id']}" \
               f"&lang={self.language}&appid={self.api_key}&units=metric"

    def get_serialized_data(self, data):
        return WeatherResponseSchema().dump(data)


class OpenWeatherMapCityClient(BaseOpenWeatherMapClient):
    """Client class to get the list of cities using openweathermap api"""

    def get_url(self, *args, **kwargs):
        return f"{settings.OPEN_WEATHER_API_BASE_URL}find?q={kwargs['query']}&lang={self.language}&appid={self.api_key}"

    def get_serialized_data(self, data):
        return CityListResponseSchema().dump(data['list'], many=True)
