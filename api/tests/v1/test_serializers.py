from django.conf import settings
from django.test import SimpleTestCase

from api.v1.serializers import CityAPIInputySerializer
from api.v1.serializers import WeatherAPIInputSerializer


class WeatherAPIInputSerializerTestCase(SimpleTestCase):
    """Tests for WeatherAPIInputSerializer"""

    def test_serialize_return_validation_error_for_invalid_data(self):
        """serialize: return validation error for invalid data"""
        # given
        serializer = WeatherAPIInputSerializer(data={})
        # when
        is_valid = serializer.is_valid()
        # then
        self.assertFalse(is_valid)
        self.assertTrue(serializer.errors.get('city_id')[0].code, 'required')

    def test_serialize_return_validation_error_for_invalid_city(self):
        """serialize: return validation error for invalid city"""
        # given
        serializer = WeatherAPIInputSerializer(data={'city_id': 'invalid'})
        # when
        is_valid = serializer.is_valid()
        # then
        self.assertFalse(is_valid)
        self.assertTrue(serializer.errors.get('city_id')[0].code, 'invalid')

    def test_serialize_return_validation_error_for_invalid_language(self):
        """serialize: return validation error for invalid language"""
        # given
        serializer = WeatherAPIInputSerializer(data={'city_id': 1, 'language': 'invalid'})
        # when
        is_valid = serializer.is_valid()
        # then
        self.assertFalse(is_valid)
        self.assertTrue(serializer.errors.get('language')[0].code, 'invalid_choice')

    def test_serialize_return_default_language(self):
        """serialize: return default language if language is not given"""
        # given
        serializer = WeatherAPIInputSerializer(data={'city_id': 1})
        # when
        is_valid = serializer.is_valid()
        # then
        self.assertTrue(is_valid)
        self.assertTrue(serializer.data['language'], settings.LANGUAGE_CODE)


class CityAPIInputySerializerTestCase(SimpleTestCase):
    """Tests for CityAPIInputySerializer"""

    def test_serialize_return_validation_error_for_invalid_data(self):
        """serialize: return validation error for invalid data"""
        # given
        serializer = CityAPIInputySerializer(data={})
        # when
        is_valid = serializer.is_valid()
        # then
        self.assertFalse(is_valid)
        self.assertTrue(serializer.errors.get('query')[0].code, 'required')

    def test_serialize_return_validation_error_for_invalid_language(self):
        """serialize: return validation error for invalid language"""
        # given
        serializer = CityAPIInputySerializer(data={'query': 'Berlin', 'language': 'invalid'})
        # when
        is_valid = serializer.is_valid()
        # then
        self.assertFalse(is_valid)
        self.assertTrue(serializer.errors.get('language')[0].code, 'invalid_choice')

    def test_serialize_return_default_language(self):
        """serialize: return default language if language is not given"""
        # given
        serializer = CityAPIInputySerializer(data={'query': 'Berlin'})
        # when
        is_valid = serializer.is_valid()
        # then
        self.assertTrue(is_valid)
        self.assertTrue(serializer.data['language'], settings.LANGUAGE_CODE)
