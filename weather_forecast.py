import requests
import json
import os
from dotenv import load_dotenv
from datetime import date


load_dotenv()
accuweather_api_key = (os.environ["accuweatherAPIKey"])
"""Environment variable containing the accuWeather API key.
    Can be replaced by the API Key String directly.
    """
days_week = ['Domingo', 'Segunda-feira', 'Terça-feira',
             'Quarte-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']


def get_coordinates():
    """Get the geolocation of the host from the Geoplugin API

    Returns:
        __dict__: Returns a dictionary containing the Latitude and Longitude of the host
    """
    reqst_coordinates = requests.get('http://www.geoplugin.net/json.gp')

    if (reqst_coordinates.status_code != 200):
        print('ERRO: Não foi possível obter as coordenadas da sua localização.')
        return None
    else:
        try:
            location = json.loads(reqst_coordinates.text)
            coordinates = {}
            coordinates['latitude'] = location['geoplugin_latitude']
            coordinates['longitude'] = location['geoplugin_longitude']
            return coordinates
        except:
            return None


def get_location_code(latitude, longitude):
    """Get the location code and host location information from the Accuweather API.

    Args:
        latitude (__str__): Host latitude
        longitude (__str__): Host longitude

    Returns:
        __dict__: Returns a dictionary containing the Location Code and Location data 
        (Location Name, Country, State, Province, etc).
    """
    location_api_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=" + \
        accuweather_api_key + "&q=" + latitude + \
        "%2C%20" + longitude + "&language=pt-br"

    reqst_location = requests.get(location_api_url)
    if (reqst_location.status_code != 200):
        print('ERRO: Não foi possível obter o código do local.')
        return None
    else:
        try:
            location_response = json.loads(reqst_location.text)
            location_info = {}
            location_info['localName'] = location_response['LocalizedName'] + ', ' + \
                location_response['AdministrativeArea']['LocalizedName'] + \
                '. ' + location_response['Country']['LocalizedName']
            location_info['localCode'] = location_response['Key']
            return location_info
        except:
            return None


def get_weather_forecast(localCode, localName):
    """Get current weather conditions for a location from the Accuweather API.

    Args:
        localCode (__str__): Location code acquired from Accuweather Geolocation API.
        localName (__str__): Location name acquired from Accuweather Geolocation API.

    Returns:
        __dict__: Returns a dictionary containing weather conditions for the location.
    """
    current_conditions_api_url = "http://dataservice.accuweather.com/currentconditions/v1/" + \
        localCode + "?apikey=" + accuweather_api_key + "&language=pt-br"

    reqst_weather_conditions = requests.get(current_conditions_api_url)
    if (reqst_weather_conditions.status_code != 200):
        print('ERRO: Não foi possível obter as condições de tempo do local.')
        return None
    else:
        try:
            current_conditions_response = json.loads(
                reqst_weather_conditions.text)
            weather_conditions = {}
            weather_conditions['weatherText'] = current_conditions_response[0]['WeatherText']
            weather_conditions['temperature'] = current_conditions_response[0]['Temperature']['Metric']['Value']
            weather_conditions['localName'] = localName
            return weather_conditions
        except:
            return None


def get_5_day_weather_forecast(localCode):
    """Get daily weather forecast for the location for the next 5 days from the Accuweather API.

    Args:
        localCode (__str__): Location code acquired from Accuweather Geolocation API.

    Returns:
        __list__: Returns a list containing the daily weather forecast for the location for the next 5 days.
    """

    daily_forecast_api_url = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + \
        localCode + "?apikey=" + accuweather_api_key + "&language=pt-br&metric=true"

    reqst_daily_forecast_conditions = requests.get(daily_forecast_api_url)
    if (reqst_daily_forecast_conditions.status_code != 200):
        print('ERRO: Não foi possível obter as condições de tempo do local.')
        return None
    else:
        try:
            daily_conditions_response = json.loads(
                reqst_daily_forecast_conditions.text)
            info_5_day_weather = []
            for daily in daily_conditions_response['DailyForecasts']:
                day_weather = {}
                day_weather['max'] = daily['Temperature']['Maximum']['Value']
                day_weather['min'] = daily['Temperature']['Minimum']['Value']
                day_weather['weather'] = daily['Day']['IconPhrase']
                day_week = int(date.fromtimestamp(
                    daily['EpochDate']).strftime("%w"))
                day_weather['day'] = days_week[day_week]
                info_5_day_weather.append(day_weather)
            return info_5_day_weather
        except:
            return None

# -------Beginning of function calls and program execution-------


coordinates = get_coordinates()

try:
    local = get_location_code(
        coordinates['latitude'], coordinates['longitude'])
    current_weather = get_weather_forecast(
        local['localCode'], local['localName'])
    print('O clima neste momento em ' + current_weather['localName'])
    print(current_weather['weatherText'])
    print('Temperatura: ' + str(current_weather['temperature']) + "\xb0" + "C")
    print('-----------------------------------------------------------------')

    print('\nClima para os próximos cinco dias:\n')

    weather_forecast_five_day = get_5_day_weather_forecast(local['localCode'])
    for daily in weather_forecast_five_day:
        print(daily['day'])
        print('Mínima: ' + str(daily['min']) + "\xb0" + "C")
        print('Máxima: ' + str(daily['max']) + "\xb0" + "C")
        print('Clima: ' + daily['weather'])
        print('------------------------------------------------')
except:
    print('ATENÇÃO: Ocorreu um erro ao processar sua solicitação. Contacte o suporte.')
