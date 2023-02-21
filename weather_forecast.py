import requests
import json
import pprint

reqst_coordinates = requests.get('http://www.geoplugin.net/json.gp')

if (reqst_coordinates.status_code != 200):
    print('Não foi possível obter a localização')
else:
    localizacao = json.loads(reqst_coordinates.text)
    latitude = localizacao['geoplugin_latitude']
    longitude = localizacao['geoplugin_longitude']
    print('Latitude: ', latitude)
    print('Longitude: ', longitude)
