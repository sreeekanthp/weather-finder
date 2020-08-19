import requests
import logging

from api.v1.exceptions import ExternalAPIError
from api.v1.serializers import OpenWeatherMapResponseSchema

logger = logging.getLogger(__name__)


class OpenWeatherMapClient:
    """ Client class to communicate with openweathermap apis """

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
        print('inside weather')
        url = f'{self.BASE_URL}?id={city_id}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.Timeout:
            logger.exception('OpenWeatherMap request timed out for city: %s', city_id)
            raise ExternalAPIError
        except requests.RequestException:
            logger.exception('OpenWeatherMap failed for city: %s', city_id)
            raise ExternalAPIError

        data = response.json()
        return self.get_serialized_data(data)
