from flask import Flask, render_template, request

import logging

from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc
from datetime import datetime

from ISS_Functions import *



#creating the webapp
app = Flask(__name__)


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.


#initialising the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ISS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#database model
class Astronauts(db.Model):
    ID = db.Column(db.Integer , primary_key = True)
    astronaut_name = db.Column(db.String(100) , nullable = False)
    wiki_url = db.Column(db.String(200) , nullable = False)

    def __repr__(self):
        return '<ID %r>' %self.ID





# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

#main page
@app.route("/")


@app.route("/home")
def home():
    
    #get_entries = Astrounauts.query.order_by(Astrounauts.ID)
    #for i in get_entries:
    #        print(i.name)

    ID = 3
    astronaut_name = "astronaut_name" 
    wiki_url = "Test url"

    #new_entry = Astronauts(ID = ID , astronaut_name = astronaut_name , wiki_url = wiki_url)

        

    #db.session.add(new_entry)

    #db.session.commit()

    print("DONE")
  
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

#passtime page
@app.route("/passtime",methods = ["POST","GET"])
def passtime():
    if request.method == "POST":
        location = request.form['location']
        passtime = ISS_passtimes(location)
        return render_template("passtime.html",passtime = passtime)
    else:
        return render_template("passtime.html")
   
if __name__ == "__main__":
    logging.basicConfig(filename = 'error.log' , level = logging.DEBUG )
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug = True)

    



 







