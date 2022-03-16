"""

Filename : ISS_Functions.py
- This file contains all the functions related to 
fetching the information of the ISS.

Contents of the file:

- def ISS_passtimes(location)
    returns :  (passtime , latitude , longitude)

- def get_country_name(latitude , longitude)
    returns : place

- def ISS_location():
    returns : (latitude ,longitude)

- def astronauts_in_ISS()
    returns : astronaut_names

"""


#importing "requests" library
import requests


#importing datetime functions from "datetime" library
from datetime import datetime


#function to generate the ISS passtimes for a location
def ISS_passtimes(location):

    """
    #converting location name to coordinates
    """

    #storing the API_KEY for locationiq API
    locationiq_key = "316aed2e9d379d"

    #url to convert location name to coordinates
    url_one = "https://us1.locationiq.com/v1/search.php?key=" + locationiq_key 

    #dictionary to store the location of ISS
    parameters_one = {
    "q" : location ,
    "format" : "json"
    }


    #making an API call to "url_one"
    #storing the response of the API
    response_one = requests.get(url_one , params = parameters_one)

    #if the response was a "success"
    if response_one.status_code == 200:

        #extracting the data in json format 
        data_one = response_one.json()

        #extracting latitude from "data_one" in float format
        latitude = float(data_one[0]["lat"])

        #extracting longitude from "data_one" in float format
        longitude = float(data_one[0]["lon"])


        #dictionary to store the latitude and longitude of the location
        #to be passed as "paratemeter_two"
        #"n" represents number of passtimes requires
        parameters_two = {"lat" :latitude , "lon":longitude , "n" : 1 }

        #url to generate passtimes from coordinates
        url_two = "http://api.open-notify.org/iss-pass.json"

        #making an API call to "url_two"
        #storing the response of the API
        response_two = requests.get(url_two , params = parameters_two)

        #extracting the data in json format
        data_two = response_two.json()

        #extracting passtime from "data_two" 
        #converting the passtime from timestamp format to "dd-mm-yyyy" format
        passtime = datetime.fromtimestamp(data_two["response"][0]["risetime"])

        #returning the ISS passtime, latitude and longitude
        return  str(passtime) , latitude , longitude
    

    #if the response was a "failure"
    else:

        #returning the message "Invalid Location!" 
        return "Invalid Location!" 


#function to generate country name from latitude and longitude 
def get_country_name(latitude , longitude):

    #dictionary to store the location of ISS
    parameters = {
    "key": "pk.d5417184e8ebdef6796c2cb7f335fabe" ,
    "lat": latitude ,
    "lon": longitude ,
    "format":"json"
    }

    #url to convert latitude and longitude to location
    url = "https://us1.locationiq.com/v1/reverse.php?"  

    #making an API call to "url"
    #storing the response of the API
    response = requests.get(url ,params = parameters)

    #extracting the data in json format
    data = response.json()

    #if the response was a "success"
    #(i.e. if the ISS is over land)
    if response.status_code == 200:  
        
        #extracting the country name
        country  = data["address"]["country"]
    
    #if the response was a "failure"
    #(i.e. if the ISS is over ocean)
    else:
        
        #setting the country name to "the Ocean"
        country = "the Ocean"
    
    #returning the name of the country
    return country


#function to generate the current location of the ISS 
def ISS_location(): 

    #url to convert generate the current location of the ISS 
    url = "http://api.open-notify.org/iss-now.json"

    #making an API call to "url"
    #storing the response of the API
    response = requests.get(url)

    #extracting the data in json format
    data = response.json()

    #extracting the latitude from "data"
    latitude = data["iss_position"]["latitude"]

    #extracting the longitude from "data"
    longitude = data["iss_position"]["longitude"]    

    #returning the laltitude and longitude the ISS
    return latitude , longitude

#function to generate the names of astronauts in the ISS
def astronauts_in_ISS(): 

    #url to convert generate the names of astronauts in the ISS
    url = "http://api.open-notify.org/astros.json"

    #making an API call to "url"
    #storing the response of the API
    response = requests.get(url)

    #extracting the data in json format
    data = response.json()

    #declaring an empty list to store the names of astronauts in the ISS
    astronaut_names = []

    #iterating through the data items
    for i in data["people"]:

        #if the name of the "craft" is "ISS"
        if i["craft"] == "ISS":

            #appending that astronaut's name into the list
            astronaut_names.append(i["name"])

    #returning the list containing the names of astronauts in the ISS
    return astronaut_names