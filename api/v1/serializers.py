from django.conf import settings
from rest_framework import fields
from rest_framework import serializers


class BaseAPIInputSerializer(serializers.Serializer):
    """Base API input serializer with common fields"""

    language = fields.ChoiceField(choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, allow_null=True)


class WeatherAPIInputSerializer(BaseAPIInputSerializer):
    """
    Serializer class to validate city id input
    Any additional validations can be added here
    """

    city_id = fields.IntegerField()


class CityAPIInputySerializer(BaseAPIInputSerializer):
    """
    Serializer class to validate city name query
    Any additional validations can be added here
    """

    query = fields.CharField()
