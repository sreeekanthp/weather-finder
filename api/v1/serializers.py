from rest_framework import fields
from rest_framework import serializers


class CityInputSerializer(serializers.Serializer):
    """
    Serializer class to validate city id input
    Any additional validations can be added here
    """
    id = fields.IntegerField()


class CityNameQuerySerializer(serializers.Serializer):
    """
    Serializer class to validate city name query
    Any additional validations can be added here
    """
    query = fields.CharField()
