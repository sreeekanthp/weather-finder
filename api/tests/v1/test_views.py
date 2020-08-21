from http import HTTPStatus
from unittest import mock

from django.test import SimpleTestCase
from django.urls import reverse

from api.v1.exceptions import ExternalAPIError
from api.v1.views import WeatherDetailsView


class WeatherDetailsViewTestCase(SimpleTestCase):
    """ Tests for WeatherDetailsView class """

    def setUp(self):
        self.url = reverse('api:v1:weather', kwargs={'city_id': 1})

    @mock.patch('api.v1.views.cache')
    @mock.patch.object(WeatherDetailsView, '_get_cache_key')
    def test_get_return_cached_weather_data(self, mock_get_cache_key, mock_cache):
        """get: return response from cache if available"""
        # given
        expected = {'city': 'Dubai'}
        mock_get_cache_key.return_value = 'cache_key'
        mock_cache.get.return_value = expected
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertDictEqual(response.data, expected)

    @mock.patch('api.v1.views.cache')
    @mock.patch.object(WeatherDetailsView, '_get_cache_key')
    @mock.patch('api.v1.views.OpenWeatherMapClient')
    def test_get_return_error_response(self, mock_api_client, mock_get_cache_key, mock_cache):
        """get: return 500 response with error details if external api fails"""
        # given
        mock_get_cache_key.return_value = 'cache_key'
        mock_cache.get.return_value = None
        mock_api_client().get_weather_data.side_effect = ExternalAPIError
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertDictEqual(response.data, {'error': 'Service Unavailable'})

    @mock.patch('api.v1.views.cache')
    @mock.patch.object(WeatherDetailsView, '_get_cache_key')
    @mock.patch('api.v1.views.OpenWeatherMapClient')
    def test_get_return_weather_data(self, mock_api_client, mock_get_cache_key, mock_cache):
        """get: return 500 response with error details if external api fails"""
        # given
        expected = {'city': 'Dubai'}
        mock_get_cache_key.return_value = 'cache_key'
        mock_cache.get.return_value = None
        mock_api_client().get_weather_data.return_value = expected
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertDictEqual(response.data, expected)
        mock_cache.set.assert_called_once_with('cache_key', expected, timeout=10, version=1)
