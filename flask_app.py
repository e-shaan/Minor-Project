'''
add comments for return rendertemplate() lines
'''



from flask import Flask, render_template, request

import logging

from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc
from datetime import date

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

#database model
class Passtimes(db.Model):

    current_time = db.Column(db.String(100), primary_key = True)
    passtime = db.Column(db.String(100) , nullable = False)
    latitude = db.Column(db.REAL , nullable = False)
    longitude = db.Column(db.REAL , nullable = False)
    location = db.Column(db.String(200) , nullable = False)

    def __repr__(self):
        return '<id %r>' %self.id

#database model
class Location(db.Model):
    passtime = db.Column(db.String(100) , primary_key = True)
    latitude = db.Column(db.REAL , nullable = False)
    longitude = db.Column(db.REAL , nullable = False)
    country = db.Column(db.String(200) , nullable = False)

    def __repr__(self):
        return '<passtime %r>' %self.passtime




# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

#main page
@app.route("/")


@app.route("/home")
def home():

    #clearing the Astronauts table from the database
    db.session.query(Astronauts).delete()
    db.session.commit()

    #gathering the astronaut names from the ISS Funtions
    astronaut_names = astronauts_in_ISS()
     
    #iterating through the name list 
    #adding all the names to the database ['Astronauts' table]
    for i in range(len(astronaut_names)) :

        #generating wikipedia url
        name = astronaut_names[i].replace(" ", "_")
        wiki_url = "https://en.wikipedia.org/wiki/" + name   

        #entering single record into the 'Astronauts' table
        new_entry = Astronauts(ID = i , astronaut_name = astronaut_names[i] , wiki_url = wiki_url)
        db.session.add(new_entry)
        db.session.commit()


    return render_template("home.html")


# '/about' URL is bound with about() function and so on
#about page
@app.route("/about")
def about():

    f = open("about.txt", "r")
    about = f.read()
    return render_template("about.html" , about = about)

#astronauts page
@app.route("/astronauts")
def astronauts():
    
    #retrieving data from 'Astronauts' table
    get_data = Astronauts.query.order_by(Astronauts.ID) 
    
    #initialising a list to temporarily store the astronaut names
    astronaut_names = []
    wiki_url = []

    #entering individual names into the list
    for i in get_data:
        astronaut_names.append(i.astronaut_name)
        wiki_url.append(i.wiki_url)

    return render_template("astronauts.html",astronaut_names = astronaut_names , wiki_url = wiki_url, date = date.today())

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

    #entering single record into the 'Location' table
    new_entry = Location(country =  country, latitude = float(latitude), longitude = float(longitude),  passtime = datetime.now())
    db.session.add(new_entry)
    db.session.commit()

    return render_template("location.html", longitude = longitude , latitude = latitude , country = country)

#passtime page
@app.route("/passtime",methods = ["POST","GET"])
def passtime():
    if request.method == "POST":
        location = request.form['location']
        
        data = ISS_passtimes(location)

        passtime = data[0]

        if data != "Invalid Location!":

            latitude = data[1]
            longitude = data[2]

            #entering single record into the 'Passtimes' table
            new_entry = Passtimes( current_time = datetime.now(), passtime = passtime, latitude = latitude , longitude = longitude, location =  location )
            db.session.add(new_entry)
            db.session.commit()


        return render_template("passtime.html", passtime = passtime)
    else:
        return render_template("passtime.html")
   
if __name__ == "__main__":
    logging.basicConfig(filename = 'error.log' , level = logging.DEBUG )
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug = True)

    



 







