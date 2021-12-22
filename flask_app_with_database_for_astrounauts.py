#http://moveforward100.pythonanywhere.com


from flask import Flask, render_template, request

import logging

from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc
from datetime import datetime




#creating the webapp
app = Flask(__name__)


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.


#initialising the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#database model
class Users(db.Model):
    user_id  = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , nullable = False)
    email = db.Column(db.String(100), nullable = False )#, unique = True)
    #date_added =  db.Column(db.DateTime , default = datetime.utcnow)


    def __repr__(self):
        return '<Name %r>' %self.name


#main page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# '/about' URL is bound with about() function and so on

#db test page
@app.route("/test")
def test():

    print("Cqq")


    user_id =  1231222
    name = "Eshaan"
    email = "EshaanEmaiwdwl"

    #new_entry = Users(user_id = user_id , name = name , email = email)



    get_entries = Users.query.order_by(Users.user_id)

    
    #print( get_entries )

    for i in get_entries:
        print(i.name)


    if True:
    
            #db.session.add(new_entry)
            
            #db.session.commit()

            return "Done!"




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

    



 







