import requests

reqst_coordinates = requests.get('http://www.geoplugin.net/json.gp')
if (reqst_coordinates.status_code != 200):
    print('Não foi possível obter a localização')
else:
    print(reqst_coordinates.text)
