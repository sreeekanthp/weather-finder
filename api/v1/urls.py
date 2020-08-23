from django.urls import path

from api.v1.views import CityListView
from api.v1.views import WeatherDetailsView

urlpatterns = [
    path('weather/<int:city_id>/', WeatherDetailsView.as_view(), name='weather'),
    path('cities/', CityListView.as_view(), name='city_list'),
]
