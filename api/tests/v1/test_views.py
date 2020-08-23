from http import HTTPStatus
from unittest import mock
from unittest.mock import Mock

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from api.v1.exceptions import ExternalAPIError
from api.v1.serializers import CityAPIInputySerializer
from api.v1.serializers import WeatherAPIInputSerializer
from api.v1.views import CityListView
from api.v1.views import WeatherDetailsView


class WeatherDetailsViewTestCase(SimpleTestCase):
    """ Tests for WeatherDetailsView """

    def setUp(self):
        self.url = reverse('api:v1:weather', kwargs={'city_id': 1})
        self.view = WeatherDetailsView()

    def test_get_cache_key_return_cache_key(self):
        """get_cache_key: return cache key to store weather data"""
        # given
        expected = "weather_data:en:1"
        # when
        actual = self.view.get_cache_key(language='en', city_id=1)
        # then
        self.assertEqual(actual, expected)

    def test_get_input_serializer_class_return_input_serializer_class(self):
        """get_input_serializer_class: return serializer class for input data"""
        # when/then
        self.assertEqual(self.view.get_input_serializer_class(), WeatherAPIInputSerializer)

    @mock.patch.object(WeatherDetailsView, 'get_input_serializer_class')
    @mock.patch.object(WeatherDetailsView, 'get_request_data')
    def test_get_return_validation_error_for_invalid_city(
        self, mock_get_request_data, mock_get_input_serializer_class
    ):
        """get: return validation error if the city id is not valid"""
        # given
        mock_get_request_data.return_value = {'city_id': 'invalid', 'language': 'en'}
        mock_serializer_class = Mock()
        mock_serializer_class().is_valid.return_value = False
        mock_serializer_class().errors = 'error'
        mock_get_input_serializer_class.return_value = mock_serializer_class
        # when
        response = self.client.get(self.url)
        # then
        self.assertTrue(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertTrue(response.data['error'], 'error')

    @mock.patch('api.v1.views.cache')
    @mock.patch.object(WeatherDetailsView, 'get_input_serializer_class')
    @mock.patch.object(WeatherDetailsView, 'get_request_data')
    @mock.patch.object(WeatherDetailsView, 'get_cache_key')
    def test_get_return_data_from_cache(
        self, mock_get_cache_key, mock_get_request_data, mock_get_input_serializer_class, mock_cache
    ):
        """get: return weather data from cache if available"""
        # given
        expected = {'name': 'Dubai'}
        mock_cache.get.return_value = expected
        mock_get_cache_key.return_value = 'cache-key'
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data, expected)
        self.assertTrue(response.status_code, HTTPStatus.OK)

    @mock.patch.object(WeatherDetailsView, 'get_api_client')
    @mock.patch('api.v1.views.cache')
    @mock.patch.object(WeatherDetailsView, 'get_input_serializer_class')
    @mock.patch.object(WeatherDetailsView, 'get_cache_key')
    def test_get_return_error_message_if_external_api_fails(
        self, mock_get_cache_key, mock_get_input_serializer_class, mock_cache, mock_get_api_client
    ):
        """get: return 500 response with proper error message if external api fails"""
        # given
        mock_cache.get.return_value = None
        mock_get_cache_key.return_value = 'cache-key'
        mock_get_api_client().get_data.side_effect = ExternalAPIError
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data['error'], _('Something went wrong! Please try again later'))
        self.assertTrue(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    @mock.patch.object(WeatherDetailsView, 'get_api_client')
    @mock.patch('api.v1.views.cache')
    @mock.patch.object(WeatherDetailsView, 'get_input_serializer_class')
    @mock.patch.object(WeatherDetailsView, 'get_cache_key')
    def test_get_return_data_from_api_and_cache_result(
        self, mock_get_cache_key, mock_get_input_serializer_class, mock_cache, mock_get_api_client
    ):
        """get: return weather data hitting api and cache the result"""
        # given
        expected = {'name': 'Dubai'}
        cache_key = 'cache_key'
        mock_cache.get.return_value = None
        mock_get_api_client().get_data.return_value = expected
        mock_get_cache_key.return_value = cache_key
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data, expected)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        mock_cache.set.assert_called_once_with(
            cache_key,
            expected,
            timeout=settings.WEATHER_RESPONSE_CACHE_TIMEOUT,
            version=settings.WEATHER_API_CACHE_VERSION,
        )


class CityListViewTestCase(SimpleTestCase):
    """ Tests for WeatherDetailsView """

    def setUp(self):
        self.url = reverse('api:v1:city_list')
        self.view = CityListView()

    def test_get_cache_key_return_cache_key(self):
        """get_cache_key: return cache key to store weather data"""
        # given
        expected = "city_list:en:berlin"
        # when
        actual = self.view.get_cache_key(language='en', query='Berlin')
        # then
        self.assertEqual(actual, expected)

    def test_get_input_serializer_class_return_input_serializer_class(self):
        """get_input_serializer_class: return serializer class for input data"""
        # when/then
        self.assertEqual(self.view.get_input_serializer_class(), CityAPIInputySerializer)

    @mock.patch.object(CityListView, 'get_input_serializer_class')
    @mock.patch.object(CityListView, 'get_request_data')
    def test_get_return_validation_error_for_invalid_city(
        self, mock_get_request_data, mock_get_input_serializer_class
    ):
        """get: return validation error if the city id is not valid"""
        # given
        mock_get_request_data.return_value = {}
        mock_serializer_class = Mock()
        mock_serializer_class().is_valid.return_value = False
        mock_serializer_class().errors = 'error'
        mock_get_input_serializer_class.return_value = mock_serializer_class
        # when
        response = self.client.get(self.url)
        # then
        self.assertTrue(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertTrue(response.data['error'], 'error')

    @mock.patch('api.v1.views.cache')
    @mock.patch.object(CityListView, 'get_input_serializer_class')
    @mock.patch.object(CityListView, 'get_request_data')
    @mock.patch.object(CityListView, 'get_cache_key')
    def test_get_return_data_from_cache(
        self, mock_get_cache_key, mock_get_request_data, mock_get_input_serializer_class, mock_cache
    ):
        """get: return city list from cache if available"""
        # given
        expected = [(1, 'Berlin, DE')]
        mock_cache.get.return_value = expected
        mock_get_cache_key.return_value = 'cache-key'
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data, expected)
        self.assertTrue(response.status_code, HTTPStatus.OK)

    @mock.patch.object(CityListView, 'get_api_client')
    @mock.patch('api.v1.views.cache')
    @mock.patch.object(CityListView, 'get_input_serializer_class')
    @mock.patch.object(CityListView, 'get_cache_key')
    def test_get_return_error_message_if_external_api_fails(
        self, mock_get_cache_key, mock_get_input_serializer_class, mock_cache, mock_get_api_client
    ):
        """get: return 500 response with proper error message if external api fails"""
        # given
        mock_cache.get.return_value = None
        mock_get_cache_key.return_value = 'cache-key'
        mock_get_api_client().get_data.side_effect = ExternalAPIError
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data['error'], _('Something went wrong! Please try again later'))
        self.assertTrue(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    @mock.patch.object(CityListView, 'get_api_client')
    @mock.patch('api.v1.views.cache')
    @mock.patch.object(CityListView, 'get_input_serializer_class')
    @mock.patch.object(CityListView, 'get_cache_key')
    def test_get_return_data_from_api_and_cache_result(
        self, mock_get_cache_key, mock_get_input_serializer_class, mock_cache, mock_get_api_client
    ):
        """get: return city list hitting api and cache the result"""
        # given
        expected = [(1, 'Berlin, DE')]
        cache_key = 'cache_key'
        mock_cache.get.return_value = None
        mock_get_api_client().get_data.return_value = expected
        mock_get_cache_key.return_value = cache_key
        # when
        response = self.client.get(self.url)
        # then
        self.assertEqual(response.data, expected)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        mock_cache.set.assert_called_once_with(
            cache_key,
            expected,
            timeout=settings.CITY_RESPONSE_CACHE_TIMEOUT,
            version=settings.CITY_API_CACHE_VERSION,
        )
