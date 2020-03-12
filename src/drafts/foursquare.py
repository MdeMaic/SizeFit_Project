import json
import requests
from IPython.display import Image
import os
from dotenv import load_dotenv

#COMANDO PARA OBTENER EL TOKEN del .env
#Si está en diferentes carpetas, dentro del paréntesis crear la estructura "../../"
load_dotenv()

#estraer tokens
tokenID = os.getenv("CLIENT_ID")
tokenSCRT = os.getenv("CLIENT_SECRET")

#Para ver que hay cerca
def exploreForesquare (query,limit,distance,latitude=40.7243,longitude=-74.0018):
    
    #configurar url y parámetros token
    url = 'https://api.foursquare.com/v2/venues/explore'
    tokenID = os.getenv("CLIENT_ID")
    tokenSCRT = os.getenv("CLIENT_SECRET")
    if not tokenID or not tokenSCRT:
        raise ValueError("Auth Fail. Check process please")

    #configurar parámetros de requests.
    params = dict(
    client_id=tokenID,
    client_secret=tokenSCRT,
    v='20200205',
    ll=f'{latitude},{longitude}',
    # Para especificar el nombre del sitio buscado
    query=query,
    limit=limit,
    radius=distance
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data


def searchForesquare (limit,distance,ID="party",latitude=37.772323,longitude=-122.214897):
    
    if ID == "party":
        category = "4d4b7105d754a06376d81259"
    elif ID == "niños":
        category = "4bf58dd8d48988d13b941735"
    elif ID == "vegano":
        category = "4bf58dd8d48988d1d3941735"
    else:
        raise ValueError ("Choose party, niños or vegano")

    #configurar url y parámetros token
    url = 'https://api.foursquare.com/v2/venues/search'
    tokenID = os.getenv("CLIENT_ID")
    tokenSCRT = os.getenv("CLIENT_SECRET")
    if not tokenID or not tokenSCRT:
        raise ValueError("Auth Fail. Check process please")

    #configurar parámetros de requests.
    params = dict(
    client_id=tokenID,
    client_secret=tokenSCRT,
    v='20200201',
    ll=f'{latitude},{longitude}',
    # Para especificar el nombre del sitio buscado
    limit=limit,
    radius=distance,
    categoryId=category
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data


def tiendaForesquare (limit,distance,name="Zara",latitude=37.772323,longitude=-122.214897):
    
    
    category = "4bf58dd8d48988d103951735"

    #configurar url y parámetros token
    url = 'https://api.foursquare.com/v2/venues/search'
    tokenID = os.getenv("CLIENT_ID")
    tokenSCRT = os.getenv("CLIENT_SECRET")
    if not tokenID or not tokenSCRT:
        raise ValueError("Auth Fail. Check process please")

    #configurar parámetros de requests.
    params = dict(
    client_id=tokenID,
    client_secret=tokenSCRT,
    v='20200201',
    ll=f'{latitude},{longitude}',
    # Para especificar el nombre del sitio buscado
    limit=limit,
    radius=distance,
    categoryId=category,
    name=name
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data