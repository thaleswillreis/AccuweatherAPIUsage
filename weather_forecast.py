import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
accuweatherAPIKey = (os.environ["accuweatherAPIKey"])


def getCoordinates():
    """Get the geolocation of the host from the Geoplugin API

    Returns:
        __dict__: Returns a dictionary containing the Latitude and Longitude of the host
    """
    reqst_coordinates = requests.get('http://www.geoplugin.net/json.gp')

    if (reqst_coordinates.status_code != 200):
        print('Não foi possível obter as coordenadas')
    else:
        location = json.loads(reqst_coordinates.text)
        coordinates = {}
        coordinates['latitude'] = location['geoplugin_latitude']
        coordinates['longitude'] = location['geoplugin_longitude']
        return coordinates


def getLocationCode(latitude, longitude):
    """Get the location code and host location information from the Accuweather API.

    Args:
        latitude (__str__): Host latitude
        longitude (__str__): Host longitude

    Returns:
        __dict__: Returns a dictionary containing the Location Code and Location data (Location Name, Country, State, Province, etc).
    """
    locationAPIUrl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=" + \
        accuweatherAPIKey + "&q=" + latitude + "%2C%20" + longitude + "&language=pt-br"

    reqst_location = requests.get(locationAPIUrl)
    if (reqst_location.status_code != 200):
        print('Não foi possível obter o código do local')
    else:
        locationResponse = json.loads(reqst_location.text)
        locationInfo = {}
        locationInfo['localName'] = locationResponse['LocalizedName'] + ', ' + \
            locationResponse['AdministrativeArea']['LocalizedName'] + \
            '. ' + locationResponse['Country']['LocalizedName']
        locationInfo['localCode'] = locationResponse['Key']
        return locationInfo


def getWeatherForecast(localCode, localName):
    """Get current weather conditions for a location from the Accuweather API.

    Args:
        localCode (__str__): Location code acquired from Accuweather Geolocation API.
        localName (__str__): Location name acquired from Accuweather Geolocation API.

    Returns:
        __dict__: Returns a dictionary containing weather conditions for the location.
    """
    currentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/" + \
        localCode + "?apikey=" + accuweatherAPIKey + "&language=pt-br"

    reqst_weather_conditions = requests.get(currentConditionsAPIUrl)
    if (reqst_weather_conditions.status_code != 200):
        print('Não foi possível obter as condições de tempo do local')
    else:
        currentConditionsResponse = json.loads(reqst_weather_conditions.text)
        weatherConditions = {}
        weatherConditions['weatherText'] = currentConditionsResponse[0]['WeatherText']
        weatherConditions['temperature'] = currentConditionsResponse[0]['Temperature']['Metric']['Value']
        weatherConditions['localName'] = localName
        return weatherConditions


coordinates = getCoordinates()
local = getLocationCode(coordinates['latitude'], coordinates['longitude'])
currentWeather = getWeatherForecast(local['localCode'], local['localName'])

print('O clima neste momento em ' + currentWeather['localName'])
print(currentWeather['weatherText'])
print('Temperatura: ' + str(currentWeather['temperature']) + "\xb0" + "C")
