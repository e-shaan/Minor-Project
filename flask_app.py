#http://moveforward100.pythonanywhere.com


from flask import Flask, render_template, request
from ISS_Functions import *
import logging

#creating the webapp
app = Flask(__name__)


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

#main page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# '/about' URL is bound with about() function and so on

#about page
@app.route("/about")
def about():
    return render_template("about.html")

#astronauts page
@app.route("/astronauts")
def astronauts():
    #list of astronaut names
    astronaut_names = astronauts_in_ISS()
    return render_template("astronauts.html",astronaut_names = astronaut_names)

#location page
@app.route("/location")
def location():
    #ISS_location() returns a tuple : (latitude , longitude)
    coordinates = ISS_location()

    #extract latitude and longitude
    latitude =  coordinates[0]
    longitude = coordinates[1]

    #get_country_name() returns the name of the country or "Ocean" 
    country = get_country_name( latitude , longitude )

    return render_template("location.html", longitude = longitude , latitude = latitude , country = country)


   
if __name__ == "__main__":
    logging.basicConfig(filename = 'error.log' , level = logging.DEBUG )
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug = True)

    



 







