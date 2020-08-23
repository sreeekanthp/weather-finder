from unittest import mock
from unittest.mock import Mock

import requests
from django.test import SimpleTestCase

from api.v1.clients import OpenWeatherMapCityClient
from api.v1.clients import OpenWeatherMapWeatherClient
from api.v1.exceptions import ExternalAPIError


class OpenWeatherMapWeatherClientTestCase(SimpleTestCase):
    """Test OpenWeatherMapWeatherClient methods"""

    def setUp(self):
        self.api_key = 'test-api-key'
        self.language = 'en'
        self.client = OpenWeatherMapWeatherClient(api_key=self.api_key, language=self.language)

    def test_get_url(self):
        """get_url: return api url to hit openweathermap"""
        # given
        expected = (
            f'http://api.openweathermap.org/data/2.5/weather?id=1'
            f'&lang={self.language}&appid={self.api_key}&units=metric'
        )
        # when
        actual = self.client.get_url(city_id=1)
        # then
        self.assertEqual(actual, expected)

    @mock.patch('api.v1.clients.WeatherResponseSchema')
    def test_get_serialized_data_return_serialized_data(self, mock_serializer_class):
        """get_serialized_data: serialize data returned from openweather api"""
        # given
        expected = {'city': 'Dubai'}
        mock_serializer_class().dump.return_value = expected
        # when
        actual = self.client.get_serialized_data(data={'name': 'Dubai'})
        # then
        self.assertDictEqual(actual, expected)

    @mock.patch.object(OpenWeatherMapWeatherClient, 'get_url')
    @mock.patch('api.v1.clients.requests')
    def test_get_data_raise_exception_for_api_error(self, mock_requests, mock_get_url):
        """get_data: raise ExternalAPIError if api return non-200 response"""
        # given
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.RequestException
        mock_requests.get.return_value = mock_response
        mock_get_url.return_value = 'http://testurl'
        # when / then
        with self.assertRaises(ExternalAPIError):
            self.client.get_data(city_id=1)

    @mock.patch.object(OpenWeatherMapWeatherClient, 'get_serialized_data')
    @mock.patch.object(OpenWeatherMapWeatherClient, 'get_url')
    @mock.patch('api.v1.clients.requests')
    def test_get_data_return_serialized_data(self, mock_requests, mock_get_url, mock_get_serialized_data):
        """get_data: fetch data from external api and return serialized data"""
        # given
        expected = {'city': 'Dubai'}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'name': 'Dubai'}
        mock_requests.get.return_value = mock_response
        mock_get_url.return_value = 'http://testurl'
        mock_get_serialized_data.return_value = {'city': 'Dubai'}
        # when
        actual = self.client.get_data(city_id=1)
        # then
        self.assertDictEqual(actual, expected)


class OpenWeatherMapCityClientTestCase(SimpleTestCase):
    """Test OpenWeatherMapCityClient methods"""

    def setUp(self):
        self.api_key = 'test-api-key'
        self.language = 'en'
        self.client = OpenWeatherMapCityClient(api_key=self.api_key, language=self.language)

    def test_get_url(self):
        """get_url: return api url to hit openweathermap"""
        # given
        expected = (
            f'http://api.openweathermap.org/data/2.5/find?q=Berlin' f'&lang={self.language}&appid={self.api_key}'
        )
        # when
        actual = self.client.get_url(query='Berlin')
        # then
        self.assertEqual(actual, expected)

    @mock.patch('api.v1.clients.CityListResponseSchema')
    def test_get_serialized_data_return_serialized_data(self, mock_serializer_class):
        """get_serialized_data: serialize data returned from openweather api"""
        # given
        expected = {'city': 'Dubai'}
        mock_serializer_class().dump.return_value = expected
        # when
        actual = self.client.get_serialized_data(data={'list': [{'name': 'Dubai'}]})
        # then
        self.assertDictEqual(actual, expected)

    @mock.patch.object(OpenWeatherMapCityClient, 'get_url')
    @mock.patch('api.v1.clients.requests')
    def test_get_data_raise_exception_for_api_error(self, mock_requests, mock_get_url):
        """get_data: raise ExternalAPIError if api return non-200 response"""
        # given
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.RequestException
        mock_requests.get.return_value = mock_response
        mock_get_url.return_value = 'http://testurl'
        # when / then
        with self.assertRaises(ExternalAPIError):
            self.client.get_data(city_id=1)

    @mock.patch.object(OpenWeatherMapCityClient, 'get_serialized_data')
    @mock.patch.object(OpenWeatherMapCityClient, 'get_url')
    @mock.patch('api.v1.clients.requests')
    def test_get_data_return_serialized_data(self, mock_requests, mock_get_url, mock_get_serialized_data):
        """get_data: fetch data from external api and return serialized data"""
        # given
        expected = [(100, 'Berlin, DE')]
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'list': [{'name': 'Berlin', 'id': 100, 'country': 'DE'}]}
        mock_requests.get.return_value = mock_response
        mock_get_url.return_value = 'http://testurl'
        mock_get_serialized_data.return_value = expected
        # when
        actual = self.client.get_data(query='Berlin')
        # then
        self.assertListEqual(actual, expected)
