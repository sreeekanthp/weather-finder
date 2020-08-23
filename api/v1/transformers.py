from marshmallow import Schema
from marshmallow import fields

from api.v1.helpers import get_wind_direction


class WeatherResponseSchema(Schema):
    """ Schema class to format openweathermap weather response """
    city = fields.String(attribute='name')
    description = fields.Method('get_description')
    temperature = fields.Method('get_temperature')
    pressure = fields.Method('get_pressure')
    humidity = fields.Method('get_humidity')
    wind = fields.Method('get_wind')

    def get_description(self, data):
        return data['weather'][0]['description']

    def get_temperature(self, data):
        return {
            'average': f"{int(data['main']['temp'])}°C",
            'min': f"{int(data['main']['temp_min'])}°C",
            'max': f"{int(data['main']['temp_max'])}°C"
        }

    def get_pressure(self, data):
        return f"{data['main']['pressure']} mb"

    def get_humidity(self, data):
        return f"{data['main']['humidity']}%"

    def get_wind(self, data):
        return {
            'speed': f"{data['wind']['speed']} m/s",
            'direction': get_wind_direction(data['wind']['deg'])
        }


class CityListResponseSchema(Schema):
    """ Schema class to format openweathermap city list response """
    id = fields.Integer()
    name = fields.Method('get_name')

    def get_name(self, data):
        return f"{data['name']}, {data['sys']['country']}"
