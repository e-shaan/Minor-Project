import requests
from datetime import datetime

def get_country_name(latitude , longitude):
    parameters = {
    'key': 'pk.d5417184e8ebdef6796c2cb7f335fabe' ,
    'lat': latitude ,
    'lon': longitude ,
    'format':'json'
    }

    url = 'https://us1.locationiq.com/v1/reverse.php?'   #url to get address from latitude and longitude
    response = requests.get(url ,params = parameters)
    data = response.json()

    if response.status_code == 200:  #if it is over the land
        place  = data['address']['country']
    else:
        place = 'the Ocean'
    return place

#get_country_name()
def ISS_location(): #function to find the current location of the ISS

    url = 'http://api.open-notify.org/iss-now.json'
    response = requests.get(url)
    data = response.json()

    latitude = data['iss_position']['latitude']
    longitude = data['iss_position']['longitude']    
    #print(latitude , longitude)
    return latitude , longitude


def astronauts_in_ISS(): #function to find the names of astronauts in the ISS
    url = 'http://api.open-notify.org/astros.json'
    response = requests.get(url)
    data = response.json()

    astronaut_names = []

    for i in data['people']:
        astronaut_names.append(i['name'])

    return astronaut_names

