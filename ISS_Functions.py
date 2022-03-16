import requests
from datetime import datetime




def ISS_passtimes(location): #function to find the ISS passtimes for a location


    #convert location name to coordinates
    url_one = 'https://us1.locationiq.com/v1/search.php?key=316aed2e9d379d' #url to convert location name to coordinates

    parameters_one = {'q' : location , 'format' : 'json'}

    response_one = requests.get(url_one , params = parameters_one)

    if response_one.status_code == 200: #if the location was invalid
        data_one = response_one.json()

        latitude = float(data_one[0]['lat'])
        longitude = float(data_one[0]['lon'])



        #get ISS passtime for the coordinates
        parameters_two = {'lat' :latitude , 'lon':longitude , 'n' : 1 }

        url_two = 'http://api.open-notify.org/iss-pass.json'

        response_two = requests.get(url_two , params = parameters_two)

        data_two = response_two.json()

        passtime = datetime.fromtimestamp(data_two['response'][0]['risetime'])
        #return the ISS passtimes
        return  str(passtime) , latitude , longitude
    
    else:
       return "Invalid Location!" 



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

    return latitude , longitude


def astronauts_in_ISS(): #function to find the names of astronauts in the ISS
    url = 'http://api.open-notify.org/astros.json'
    response = requests.get(url)
    data = response.json()

    astronaut_names = []

    for i in data['people']:
        if i['craft'] == "ISS":
            astronaut_names.append(i['name'])

    return astronaut_names

