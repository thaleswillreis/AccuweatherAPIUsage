import requests
import json
import pprint
import os
from dotenv import load_dotenv

load_dotenv()
accuweatherAPIKey = (os.environ["accuweatherAPIKey"])

reqst_coordinates = requests.get('http://www.geoplugin.net/json.gp')

if (reqst_coordinates.status_code != 200):
    print('Não foi possível obter as coordenadas')
else:
    localizacao = json.loads(reqst_coordinates.text)
    latitude = localizacao['geoplugin_latitude']
    longitude = localizacao['geoplugin_longitude']

    locationAPIUrl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=" + \
        accuweatherAPIKey + "&q=" + latitude + "%2C%20" + longitude + "&language=pt-br"

    reqst_location = requests.get(locationAPIUrl)
    if (reqst_location.status_code != 200):
        print('Não foi possível obter o código do local')
    else:
        locationResponse = json.loads(reqst_location.text)
        nomeLocal = locationResponse['LocalizedName'] + ', ' + \
            locationResponse['AdministrativeArea']['LocalizedName'] + \
            '. ' + locationResponse['Country']['LocalizedName']
        codigoLocal = locationResponse['Key']
        print('Obtendo clima do Local: ', nomeLocal)

        currentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/" + \
            codigoLocal + "?apikey=" + accuweatherAPIKey + "&language=pt-br"

        reqst_conditions = requests.get(currentConditionsAPIUrl)
    if (reqst_conditions.status_code != 200):
        print('Não foi possível obter as condições de tempo do local')
    else:
        currentConditionsResponse = json.loads(reqst_conditions.text)
        textoClima = currentConditionsResponse[0]['WeatherText']
        temperatura = currentConditionsResponse[0]['Temperature']['Metric']['Value']
        print('Clima no momento: ', textoClima)
        print('Temperatura: ' + str(temperatura) + ' graus Celsius')
