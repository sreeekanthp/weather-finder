from unittest import mock
from unittest.mock import Mock

import requests
from django.test import SimpleTestCase

from api.v1.clients import OpenWeatherMapClient
from api.v1.exceptions import ExternalAPIError
from api.v1.transformers import OpenWeatherMapResponseSchema


class OpenWeatherMapClientTestCase(SimpleTestCase):
    """ Test OpenWeatherMapClient methods"""
    def setUp(self):
        self.client = OpenWeatherMapClient(api_key='testapikey')

    def test_get_serializer_class_return_serializer_class(self):
        """get_serializer_class: return serializer class for the client"""
        # when/then
        self.assertEqual(self.client.serializer_class, OpenWeatherMapResponseSchema)

    @mock.patch.object(OpenWeatherMapClient, 'get_serializer_class')
    def test_get_serialized_data_return_serialized_data(self, mock_get_serializer_class):
        """get_serialized_data: serialize data returned from openweather api"""
        # given
        expected = {'city': 'Dubai'}
        mock_serializer_class = Mock()
        mock_serializer_class().dump.return_value = expected
        mock_get_serializer_class.return_value = mock_serializer_class
        # when
        actual = self.client.get_serialized_data(data={'name': 'Dubai'})
        # then
        self.assertDictEqual(actual, expected)

    @mock.patch('api.v1.clients.requests')
    def test_get_weather_data_raise_exception_for_api_timeout(self, mock_requests):
        """get_weather_data: raise ExternalAPIError if api return timeout error"""
        # given
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.RequestException
        mock_requests.get.return_value = mock_response
        # when / then
        with self.assertRaises(ExternalAPIError):
            self.client.get_weather_data(city_id=1)

    @mock.patch.object(OpenWeatherMapClient, 'get_serialized_data')
    @mock.patch('api.v1.clients.requests')
    def test_get_weather_data_return_serialized_data(self, mock_requests, mock_get_serialized_data):
        """get_weather_data: fetch data from external api and return serialized data"""
        # given
        expected = {'city': 'Dubai'}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'name': 'Dubai'}
        mock_requests.get.return_value = mock_response
        mock_get_serialized_data.return_value = {'city': 'Dubai'}
        # when
        actual = self.client.get_weather_data(city_id=1)
        # then
        self.assertDictEqual(actual, expected)
