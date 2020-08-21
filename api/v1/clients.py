import requests
import logging

from django.conf import settings

from api.v1.exceptions import ExternalAPIError
from api.v1.transformers import OpenWeatherMapResponseSchema

logger = logging.getLogger(__name__)


class OpenWeatherMapClient:
    """ Client class to retrieve weather data using openweathermap apis """

    BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
    serializer_class = OpenWeatherMapResponseSchema

    def __init__(self, api_key):
        self.api_key = api_key

    def get_serializer_class(self):
        return self.serializer_class

    def get_serialized_data(self, data):
        serializer_class = self.get_serializer_class()
        # TODO: What if the expected response from external api changes changes
        return serializer_class().dump(data)

    def get_weather_data(self, city_id):
        """
        Hit OpenWeatherMap api using api key to get weather data for given city and
        serialize the data returned from the api

        Args:
            city_id(int): city id

        Returns: Serialized response from OpenWeatherMap api
        """
        url = f'{self.BASE_URL}?id={city_id}&appid={self.api_key}&units=metric'
        response = requests.get(url, timeout=settings.OPEN_WEATHER_API_TIMEOUT)
        try:
            response.raise_for_status()
        except requests.RequestException:
            logger.exception('OpenWeatherMap api failed for city: %s', city_id)
            raise ExternalAPIError

        data = response.json()
        return self.get_serialized_data(data)
