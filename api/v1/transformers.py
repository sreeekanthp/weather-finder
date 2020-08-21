from marshmallow import Schema
from marshmallow import fields

from api.v1.helpers import get_wind_direction


class OpenWeatherMapResponseSchema(Schema):
    """ Schema class to format openweathermap response """
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
            'min': f"{data['main']['temp_min']}°C",
            'max': f"{data['main']['temp_max']}°C"
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