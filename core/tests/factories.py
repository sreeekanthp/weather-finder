import factory

from core.models import City


class CityFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n + 1)
    external_id = factory.Sequence(lambda n: n + 1)

    class Meta:
        model = City
