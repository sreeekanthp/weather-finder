from unittest import mock

from django.test import SimpleTestCase

from api.v1.transformers import OpenWeatherMapResponseSchema


class OpenWeatherMapResponseSchemaTestCase(SimpleTestCase):
    """ Tests for OpenWeatherMapResponseSchema """

    @mock.patch('api.v1.transformers.get_wind_direction')
    def test_serialize_return_serialized_data(self, mock_get_wind_direction):
        """test that the data is serialized to defined format"""
        # given
        mock_direction = 'NE'
        mock_get_wind_direction.return_value = mock_direction
        data = {
            "weather": [{"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02n"}],
            "main": {"temp": 32, "feels_like": 38.18, "temp_min": 32, "temp_max": 33, "pressure": 997, "humidity": 79},
            "wind": {"speed": 3.1, "deg": 150},
            "name": "Dubai",
        }
        expected = {
            'city': 'Dubai',
            'temperature': {
                'min': '32°C',
                'max': '33°C',
            },
            'pressure': '997 mb',
            'humidity': '79%',
            'wind': {'speed': '3.1 m/s', 'direction': mock_direction},
            'description': 'few clouds',
        }
        # when
        actual = OpenWeatherMapResponseSchema().dump(data)
        # then
        self.assertDictEqual(actual, expected)