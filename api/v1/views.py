import logging
from http import HTTPStatus

from django.utils.translation import ugettext_lazy as _

from api.v1.clients import OpenWeatherMapCityListClient
from api.v1.clients import OpenWeatherMapWeatherClient
from api.v1.exceptions import ExternalAPIError
from api.v1.serializers import WeatherAPIInputSerializer
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import CityAPIInputySerializer

logger = logging.getLogger(__name__)


class WeatherDetailsView(APIView):
    """
    View to retrieve weather data for given city
    """

    @staticmethod
    def _get_cache_key(city_id, language):
        """ Generate cache key to store weather data for given city """
        return f'weather_data:{city_id}:{language}'

    def get(self, request, **kwargs):
        request_data = kwargs
        language = request.query_params.get('language')
        if language:
            request_data['language'] = language

        serializer = WeatherAPIInputSerializer(
            data=request_data
        )
        if not serializer.is_valid():
            logger.error('Request received with invalid data')
            return Response(data={'error': serializer.errors}, status=HTTPStatus.BAD_REQUEST,)

        language = serializer.data['language']
        city_id = serializer.data['city_id']
        cache_key = self._get_cache_key(city_id, language)
        response = cache.get(cache_key, version=settings.OPEN_WEATHER_API_CACHE_VERSION)
        if response:
            return Response(data=response, status=HTTPStatus.OK)

        client = OpenWeatherMapWeatherClient(api_key=settings.OPEN_WEATHER_API_KEY, language=language)
        try:
            response = client.get_data(city_id=city_id, language=language)
        except ExternalAPIError:
            logger.error('External API returned invalid response for city %s', city_id)
            return Response(
                data={'error': _('Something went wrong! Please try again later')}, status=HTTPStatus.INTERNAL_SERVER_ERROR
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
        serializer = CityAPIInputySerializer(data=request.query_params)
        if not serializer.is_valid():
            logger.error('Request received with invalid city name query %s', request.query_params)
            return Response(data={'error': serializer.errors}, status=HTTPStatus.BAD_REQUEST,)

        language = serializer.data['language']
        city_query = serializer.data['query']
        cache_key = self._get_cache_key(city_query)
        response = cache.get(cache_key, version=settings.OPEN_WEATHER_API_CACHE_VERSION)
        if response:
            return Response(data=response, status=HTTPStatus.OK)

        client = OpenWeatherMapCityListClient(api_key=settings.OPEN_WEATHER_API_KEY, language=language)
        try:
            response = client.get_data(city_query)
        except ExternalAPIError:
            logger.error('External API returned invalid response for city query %s', city_query)
            return Response(
                data={'error': _('Something went wrong! Please try again later')}, status=HTTPStatus.INTERNAL_SERVER_ERROR
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
