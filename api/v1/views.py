import logging
from http import HTTPStatus

from api.v1.clients import OpenWeatherMapClient
from api.v1.exceptions import ExternalAPIError
from api.v1.serializers import CityInputSerializer
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger(__name__)


class WeatherDetailsView(APIView):
    """
    View to retrieve weather data for given city
    """

    errors_messages = {
        'invalid_city': 'Something went wrong with the selected city! Please try a different city',
        'external_api_error': 'Something went wrong! Please try again later',
    }

    @staticmethod
    def _get_cache_key(city_id):
        """ Generate cache key to store weather data for given city """
        return f'weather_data:{city_id}'

    def get(self, request, city_id):
        serializer = CityInputSerializer(data={'id': city_id})
        if not serializer.is_valid():
            logger.error('Request received with invalid city id %s', city_id)
            return Response(
                data={'error': self.errors_messages['invalid_city']}, status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        city_external_id = serializer.data['id']
        cache_key = self._get_cache_key(city_id)
        response = cache.get(cache_key, version=settings.OPEN_WEATHER_API_CACHE_VERSION)
        if response:
            return Response(data=response, status=HTTPStatus.OK)

        client = OpenWeatherMapClient(settings.OPEN_WEATHER_API_KEY)
        try:
            response = client.get_weather_data(city_external_id)
        except ExternalAPIError:
            logger.error('External API returned invalid response for city %s', city_id)
            return Response(
                data={'error': self.errors_messages['external_api_error']}, status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        else:
            cache.set(
                cache_key,
                response,
                timeout=settings.OPEN_WEATHER_RESPONSE_CACHE_TIMEOUT,
                version=settings.OPEN_WEATHER_API_CACHE_VERSION,
            )
        return Response(data=response, status=HTTPStatus.OK)
