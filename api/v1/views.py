import logging
from http import HTTPStatus

from api.v1.clients import OpenWeatherMapCityListClient
from api.v1.clients import OpenWeatherMapWeatherClient
from api.v1.exceptions import ExternalAPIError
from api.v1.serializers import CityInputSerializer
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import CityNameQuerySerializer

logger = logging.getLogger(__name__)


class WeatherDetailsView(APIView):
    """
    View to retrieve weather data for given city
    """

    @staticmethod
    def _get_cache_key(city_id):
        """ Generate cache key to store weather data for given city """
        return f'weather_data:{city_id}'

    def get(self, request, city_id):
        serializer = CityInputSerializer(data={'id': city_id})
        if not serializer.is_valid():
            logger.error('Request received with invalid city id %s', city_id)
            return Response(data={'error': serializer.errors}, status=HTTPStatus.BAD_REQUEST,)

        cache_key = self._get_cache_key(city_id)
        response = cache.get(cache_key, version=settings.OPEN_WEATHER_API_CACHE_VERSION)
        if response:
            return Response(data=response, status=HTTPStatus.OK)

        client = OpenWeatherMapWeatherClient(settings.OPEN_WEATHER_API_KEY)
        try:
            response = client.get_data(city_id)
        except ExternalAPIError:
            logger.error('External API returned invalid response for city %s', city_id)
            return Response(
                data={'error': 'Something went wrong! Please try again later'}, status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        else:
            cache.set(
                cache_key,
                response,
                timeout=settings.OPEN_WEATHER_RESPONSE_CACHE_TIMEOUT,
                version=settings.OPEN_WEATHER_API_CACHE_VERSION,
            )
        return Response(data=response, status=HTTPStatus.OK)


class CityListView(APIView):

    def _get_cache_key(self, city_query):
        return f'city_query:{city_query}'

    def get(self, request):
        serializer = CityNameQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            logger.error('Request received with invalid city name query %s', request.query_params)
            return Response(data={'error': serializer.errors}, status=HTTPStatus.BAD_REQUEST,)

        city_query = serializer.data['query']
        cache_key = self._get_cache_key(city_query)
        response = cache.get(cache_key, version=settings.OPEN_WEATHER_API_CACHE_VERSION)
        if response:
            return Response(data=response, status=HTTPStatus.OK)

        client = OpenWeatherMapCityListClient(settings.OPEN_WEATHER_API_KEY)
        try:
            response = client.get_data(city_query)
        except ExternalAPIError:
            logger.error('External API returned invalid response for city query %s', city_query)
            return Response(
                data={'error': 'Something went wrong! Please try again later'}, status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        else:
            if response:
                cache.set(
                    cache_key,
                    response,
                    timeout=settings.OPEN_WEATHER_RESPONSE_CACHE_TIMEOUT,
                    version=settings.OPEN_WEATHER_API_CACHE_VERSION,
                )
        return Response(data=response, status=HTTPStatus.OK)
