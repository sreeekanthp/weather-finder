from django.urls import path

from api.v1.views import WeatherDetailsView

urlpatterns = [
    path('weather/(?P<city_id>\d+)/', WeatherDetailsView.as_view(), name='weather'),
]
