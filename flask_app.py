"""

A space themed webapp that uses Python’s Flask framework 
in the backend and HTML, CSS and JavaScript on the client
side to bring to the users an out of the world experience,
literally. The application provides information about his ISS,
it’s live current location, live updates about astronauts
living on the ISS. This information is gathered from an 
open-source webservice open-notify.org though APIs. 
Furthermore, the same is hosted on a PaaS cloud platform.

"""


#importing Flask functions from "flask" library
from flask import Flask, render_template, request


#importing Flask SQLAlchemy functions from "flask_sqlalchemy" library
from flask_sqlalchemy import SQLAlchemy 


#importing desc functions from "sqlalchemy" library
from sqlalchemy import desc


#importing date function from "datetime" library
from datetime import date


#importing all functions from "ISS_Functions" file
from ISS_Functions import *


#importing "logging" library
import logging


#initializing the "Flask" webapp
app = Flask(__name__)


#initialising the "SQLAlchemy" database

#setting path to the database file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ISS.db"

#disabling the warning for modifications in the "SQLAlchemy" library
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#creating the "SQLAlchemy" database instance called "db"
db = SQLAlchemy(app)

#declaring the database models of "ISS.db"

#creating the db model for the table "Astronauts"
class Astronauts(db.Model):

    #"ID" column to act as the primary key
    ID = db.Column(db.Integer , primary_key = True)
   
    #"astronaut_name" column to store the names of the astronauts
    astronaut_name = db.Column(db.String(100) , nullable = False)

    #"wiki_url" column to store the Wikipedia urls of the astronauts
    wiki_url = db.Column(db.String(200) , nullable = False)

    #function to represent the objects of class Astronauts
    def __repr__(self):
        
        #generating the object in readable format
        rep = "Astronauts("
        + str(self.ID) 
        + ","
        + str(self.astronaut_name) 
        + "," 
        + str(self.wiki_url) 
        + ")"
        
        #return the readable format of the current object
        return rep


#creating the db model for the table "Passtimes"
class Passtimes(db.Model):

    #"current_time" column to act as the primary key and log the entry time
    current_time = db.Column(db.String(100), primary_key = True)

    #"passtime" column to store the passtime of the ISS
    passtime = db.Column(db.String(100) , nullable = False)

    #"latitude" column to store the latitude of the ISS
    latitude = db.Column(db.REAL , nullable = False)

    #"longitude" column to store the longitude of the ISS
    longitude = db.Column(db.REAL , nullable = False)

    #"location" column to store the location of the ISS
    location = db.Column(db.String(200) , nullable = False)

    #function to represent the objects of class Passtimes
    def __repr__(self):
        
        #generating the object in readable format
        rep = "Passtimes("
        + str(self.current_time) 
        + ","
        + str(self.passtime) 
        + "," 
        + str(self.latitude)
        + "," 
        + str(self.longitude)
        + "," 
        + str(self.location) 
        + ")"
        
        #return the readable format of the current object
        return rep


#creating the db model for the table "Location"
class Location(db.Model):

    #"passtime" column to act as the primary key and log the entry time
    passtime = db.Column(db.String(100), primary_key = True)

    #"latitude" column to store the latitude of the ISS
    latitude = db.Column(db.REAL , nullable = False)

    #"longitude" column to store the longitude of the ISS
    longitude = db.Column(db.REAL , nullable = False)

    #"country" column to store the country of the ISS
    country = db.Column(db.String(200) , nullable = False)

    #function to represent the objects of class Location
    def __repr__(self):
        
        #generating the object in readable format
        rep = "Location("
        + str(self.passtime) 
        + "," 
        + str(self.latitude)
        + "," 
        + str(self.longitude)
        + "," 
        + str(self.country) 
        + ")"
        
        #return the readable format of the current object
        return rep

"""

The route() function of the Flask class is a decorator, 
which tells the application which URL should call 
the associated function.

"""

#declaring paths for webpages

#path to main page
@app.route("/")

#path to home page
@app.route("/home")

#function to call when "/" or "/home" path is accessed
def home():

    """
    
    - Calling the astronauts_in_ISS() function
    - Fetching details of the astronauts
    - Storing the details in a database for later use

    """

    #clearing the Astronauts table from the database
    db.session.query(Astronauts).delete()

    #commiting the changes made
    db.session.commit()

    #gathering the astronaut names from the ISS Funtions
    astronaut_names = astronauts_in_ISS()
     
    #adding all the names to the database ["Astronauts" table]
    
    #iterating through the name list 
    for i in range(len(astronaut_names)) :

        #generating wikipedia url for each astronaut

        #replacing blank spaces " " with an underscore "_"
        name = astronaut_names[i].replace(" ", "_")

        #appending the name of the astronaut to the wikipedia url template
        wiki_url = "https://en.wikipedia.org/wiki/" + name   

        #creating new record for the "Astronauts" table
        new_entry = Astronauts(ID = i , astronaut_name = astronaut_names[i] , wiki_url = wiki_url)

        #entering new record into the "Astronauts" table
        db.session.add(new_entry)

        #commiting the changes made
        db.session.commit()

    #returning "home.html" page to be rendered on the browser
    return render_template("home.html")


#path to about page
@app.route("/about")

#function to call when "/about" path is accessed
def about():

    #opening file containing contents of the about page
    f = open("about.txt", "r")

    #reading the contents of the file
    about = f.read()

    #returning "about.html" page to be rendered on the browser
    #passing the parameters required by the html page
    return render_template("about.html" , about = about)


#path to astronauts page
@app.route("/astronauts")

#function to call when "/astronauts" path is accessed
def astronauts():
    
    #retrieving data from "Astronauts" table
    #sorting the data is ascending order
    get_data = Astronauts.query.order_by(Astronauts.ID) 
    
    #initializing a list to temporarily store the astronaut names
    astronaut_names = []

    #initializing a list to temporarily store the wikipedia urls
    wiki_url = []

    #iterating through the database records
    for i in get_data:

        #entering individual names into the list
        astronaut_names.append(i.astronaut_name)

        #entering wikipedia urls into the list
        wiki_url.append(i.wiki_url)

    #returning "astronauts.html" page to be rendered on the browser
    #passing the parameters required by the html page
    return render_template("astronauts.html", astronaut_names = astronaut_names ,wiki_url = wiki_url, date = date.today())

#path to location page
@app.route("/location")

#function to call when "/location" path is accessed
def location():

    #generating the current coordinates of the ISS
    #ISS_location() returns a tuple : (latitude , longitude)
    coordinates = ISS_location()

    #extracting latitude from the coordinates  
    latitude =  coordinates[0]

    #extracting longitude from the coordinates 
    longitude = coordinates[1]

    #generating the current country of the ISS's location
    #get_country_name() returns the name of the country or "the Ocean" 
    country = get_country_name( latitude , longitude )

    #creating new record for the "Location" table
    new_entry = Location(country =  country, latitude = float(latitude), longitude = float(longitude),  passtime = datetime.now())
    
    #entering new record into the "Location" table
    db.session.add(new_entry)

    #commiting the changes made
    db.session.commit()

    #returning "location.html" page to be rendered on the browser
    #passing the parameters required by the html page
    return render_template("location.html", longitude = longitude , latitude = latitude , country = country)

#path to about page
@app.route("/passtime", methods = ["POST","GET"])

#function to call when or "/passtime" path is accessed
def passtime():

    #if the form is submitted
    if request.method == "POST":

        #extracting location from the "location" form
        location = request.form["location"]
        
        #generating the passtime of the ISS over "location"
        #ISS_passtimes() returns a tuple : (passtime ,latitude ,longitude)
        data = ISS_passtimes(location)

        
        #if the "data" is a valid location
        if data != "Invalid Location!":

            #extracting the passtime from the data
            passtime = data[0]

            #extracting the latitude from the data
            latitude = data[1]

            #extracting the longitude from the data
            longitude = data[2]

            #creating new record for the "Passtimes" table
            new_entry = Passtimes( current_time = datetime.now(), passtime = passtime, latitude = latitude , longitude = longitude, location =  location )
            
            #entering new record into the "Passtimes" table
            db.session.add(new_entry)

            #commiting the changes made
            db.session.commit()

            #returning "passtime.html" page to be rendered on the browser
            #passing the parameters required by the html page
            return render_template("passtime.html", passtime = passtime)

        #inner else
        else:

            #returning "passtime.html" page to be rendered on the browser
            #passing the parameters required by the html page
            return render_template("passtime.html", passtime = data)
    
    #outer else
    else:
        
        #returning "passtime.html" page to be rendered on the browser
        return render_template("passtime.html")
   

#checking if the current file is a main program or an imported module
#if the current file is a main program
if __name__ == "__main__":

    #logging DEBUG level data into error.log file
    logging.basicConfig(filename = "error.log" , level = logging.DEBUG )

    # run() method of Flask class runs the application 
    # on the local development server.
    
    # starting the webapp
    app.run(debug = True)
