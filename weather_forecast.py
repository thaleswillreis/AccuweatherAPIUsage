import requests
import json
import pprint

accuweatherAPIKey = '	IGB5xYr0Y6YXQfmBA2CROn5dQMcF105T'

reqst_coordinates = requests.get('http://www.geoplugin.net/json.gp')

if (reqst_coordinates.status_code != 200):
    print('Não foi possível obter as coordenadas')
else:
    localizacao = json.loads(reqst_coordinates.text)
    latitude = localizacao['geoplugin_latitude']
    longitude = localizacao['geoplugin_longitude']
    # print('Latitude: ', latitude)
    # print('Longitude: ', longitude)

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
        # print(pprint.pprint(json.loads(reqst_location.text)))
        print('Local: ', nomeLocal)
        print('Código do Local: ', codigoLocal)
