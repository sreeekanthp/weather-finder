import logging
from http import HTTPStatus

from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.clients import OpenWeatherMapCityClient
from api.v1.clients import OpenWeatherMapWeatherClient
from api.v1.exceptions import ExternalAPIError
from api.v1.serializers import CityAPIInputySerializer
from api.v1.serializers import WeatherAPIInputSerializer

logger = logging.getLogger(__name__)


class BaseWeatherAPIView(APIView):
    """
    Base view for external api requests to openweathermap
    """

    CACHE_VERSION = 1
    CACHE_TIMEOUT = 100

    def get_cache_key(self, **kwargs):
        """Generate cache key to store response"""
        raise NotImplementedError

    def get_request_data(self, request, **kwargs):
        """Get request data from url and/or query params"""
        raise NotImplementedError

    def get_input_serializer_class(self):
        """Get serializer class to validate api input"""
        raise NotImplementedError

    def get_api_client(self, **kwargs):
        """Get openweathermap api client class"""
        raise NotImplementedError

    def get(self, request, **kwargs):
        request_data = self.get_request_data(request, **kwargs)
        serializer_class = self.get_input_serializer_class()
        serializer = serializer_class(data=request_data)
        if not serializer.is_valid():
            logger.error('Weather API request received with invalid data %s', kwargs)
            return Response(data={'error': serializer.errors}, status=HTTPStatus.BAD_REQUEST)

        input_data = serializer.data
        cache_key = self.get_cache_key(**input_data)
        response = cache.get(cache_key, version=self.CACHE_VERSION)
        if response:
            return Response(data=response, status=HTTPStatus.OK)

        client = self.get_api_client(**input_data)
        try:
            response = client.get_data(**input_data)
        except ExternalAPIError:
            logger.error('External API returned invalid response for params %s', input_data)
            return Response(
                data={'error': _('Something went wrong! Please try again later')},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        else:
            cache.set(
                cache_key, response, timeout=int(self.CACHE_TIMEOUT), version=int(self.CACHE_VERSION),
            )
        return Response(data=response, status=HTTPStatus.OK)


class WeatherDetailsView(BaseWeatherAPIView):
    """
    View to retrieve weather data for given city and language using openweathermap weather api
    """

    CACHE_VERSION = settings.WEATHER_API_CACHE_VERSION
    CACHE_TIMEOUT = settings.WEATHER_RESPONSE_CACHE_TIMEOUT

    def get_cache_key(self, *args, **kwargs):
        """Generate cache key to store response"""
        return f"weather_data:{kwargs['language']}:{kwargs['city_id']}"

    def get_request_data(self, request, **kwargs):
        """Get request data from url and/or query params"""
        request_data = kwargs
        language = request.query_params.get('language')
        if language:
            request_data['language'] = language
        return request_data

    def get_input_serializer_class(self):
        """Get serializer class to validate api input"""
        return WeatherAPIInputSerializer

    def get_api_client(self, **kwargs):
        """Get openweathermap api client clas"""
        return OpenWeatherMapWeatherClient(api_key=settings.OPEN_WEATHER_API_KEY, language=kwargs['language'])


class CityListView(BaseWeatherAPIView):
    """
    View to retrieve city lists for given query using openweathermap bulk api
    """

    CACHE_VERSION = settings.CITY_API_CACHE_VERSION
    CACHE_TIMEOUT = settings.CITY_RESPONSE_CACHE_TIMEOUT

    def get_cache_key(self, *args, **kwargs):
        """Generate cache key to store response"""
        return f"city_list:{kwargs['language']}:{kwargs['query'].lower()}"

    def get_request_data(self, request, **kwargs):
        """Get request data from url and/or query params"""
        return request.query_params

    def get_input_serializer_class(self):
        """Get serializer class to validate api input"""
        return CityAPIInputySerializer

    def get_api_client(self, **kwargs):
        """Get openweathermap api client class"""
        return OpenWeatherMapCityClient(api_key=settings.OPEN_WEATHER_API_KEY, language=kwargs['language'])
