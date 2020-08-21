from http import HTTPStatus

from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.clients import OpenWeatherMapClient
from api.v1.exceptions import ExternalAPIError


class WeatherDetailsView(APIView):
    """
    View to retrieve weather data for given city
    """

    @staticmethod
    def _get_cache_key(city_id):
        """ Generate cache key to store weather data for given city """
        return f'weather_data:{city_id}'

    def get(self, request, city_id):
        # TODO: Add serializer to validate input data
        cache_key = self._get_cache_key(city_id)
        response = cache.get(cache_key, version=settings.OPEN_WEATHER_API_CACHE_VERSION)
        if response:
            return Response(data=response, status=HTTPStatus.OK)

        client = OpenWeatherMapClient(settings.OPEN_WEATHER_API_KEY)
        try:
            response = client.get_weather_data(city_id)
        except ExternalAPIError:
            return Response(data={'error': 'Service Unavailable'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            cache.set(
                cache_key,
                response,
                timeout=settings.OPEN_WEATHER_RESPONSE_CACHE_TIMEOUT,
                version=settings.OPEN_WEATHER_API_CACHE_VERSION,
            )
        return Response(data=response, status=HTTPStatus.OK)
