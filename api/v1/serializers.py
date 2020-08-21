from rest_framework import fields
from rest_framework import serializers

from core.models import City


class CityInputSerializer(serializers.Serializer):
    """ Serializer class to validate city id input """

    id = fields.IntegerField()

    def validate_id(self, value):
        try:
            city = City.objects.get(id=value)
        except City.DoesNotExist:
            raise serializers.ValidationError("Invalid city")
        return city.external_id
