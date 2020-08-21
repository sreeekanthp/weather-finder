from http import HTTPStatus
from unittest import mock

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import reverse

from api.v1.clients import OpenWeatherMapClient
from api.v1.views import WeatherDetailsView


class WeatherDetailsViewTestCase(SimpleTestCase):
    """ Tests for WeatherDetailsView """

    def setUp(self):
        self.url = reverse('api:v1:weather', kwargs={'city_id': 1})

    @mock.patch('api.v1.views.CityInputSerializer')
    def test_get_return_validation_error_for_invalid_city(self, mock_serializer_class):
        """get: return validation error if the city id is not valid"""
        # given
        expected = {}
        mock_serializer = mock_serializer_class()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = expected
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data, expected)
        self.assertTrue(response.status_code, HTTPStatus.BAD_REQUEST)

    @mock.patch('api.v1.views.cache')
    @mock.patch('api.v1.views.CityInputSerializer')
    def test_get_return_data_from_cache(self, mock_serializer_class, mock_cache):
        """get: return weather data from cache if available"""
        # given
        expected = {'name': 'Dubai'}
        mock_serializer = mock_serializer_class()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {'id': 1}
        mock_cache.get.return_value = expected
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data, expected)
        self.assertTrue(response.status_code, HTTPStatus.OK)

    @mock.patch.object(WeatherDetailsView, '_get_cache_key')
    @mock.patch.object(OpenWeatherMapClient, 'get_weather_data')
    @mock.patch('api.v1.views.cache')
    @mock.patch('api.v1.views.CityInputSerializer')
    def test_get_return_data_from_api_and_cache_result(
        self, mock_serializer_class, mock_cache, mock_get_weather_data, mock_get_cache_key
    ):
        """get: return weather data hitting api and cache the result"""
        # given
        expected = {'name': 'Dubai'}
        cache_key = 'cache_key'
        mock_serializer = mock_serializer_class()
        mock_serializer.is_valid.return_value = True
        mock_serializer.data = {'id': 1}
        mock_cache.get.return_value = None
        mock_get_weather_data.return_value = expected
        mock_get_cache_key.return_value = cache_key
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data, expected)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        mock_cache.set.assert_called_once_with(
            cache_key,
            expected,
            timeout=settings.OPEN_WEATHER_RESPONSE_CACHE_TIMEOUT,
            version=settings.OPEN_WEATHER_API_CACHE_VERSION,
        )
