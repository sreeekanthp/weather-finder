from django.test import TestCase
from rest_framework import serializers

from api.v1.serializers import CityInputSerializer
from core.tests.factories import CityFactory


class CityInputSerializerTestCase(TestCase):
    """Tests for CityInputSerializer"""

    def setUp(self):
        self.city_id = 1
        self.serializer = CityInputSerializer(data={'id': self.city_id})

    def test_validate_id_raise_validation_error(self):
        """validate_id: return validation error if city id is invalid"""
        # when/then
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate_id(self.city_id)

    def test_validate_id_return_city_external_id(self):
        """validate_id: return city external id if given city id is valid"""
        # given
        city = CityFactory(id=self.city_id)
        # when
        actual = self.serializer.validate_id(self.city_id)
        # then
        self.assertEqual(actual, city.external_id)
