# import dependencies 
import datetime as dt 
import numpy as np 
import pandas as pd 

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func 

from flask import Flask, jsonify

# create a variable to hold the sqlite database so we can access it and query from our database files 
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes 
Base = automap_base() 

# reflect the tables into sqlalchemy, you want to reflect the holdings of the sqlite database 
Base.prepare(engine, reflect = True)

# save references to each table
# create a variable for each of the classes so that we can reference them later 
Measurement = Base.classes.measurement 
Station = Base.classes.station
 
# create a session link from python to our database
session = Session(engine)

# set up flask, define our flask app 
app = Flask(__name__)
# __name__ variable is a special type of variable and its values depend on where and how the code is run 
# if we wanted to import the app.py file into another python file named example.py the variable __name__ would be set to example 

# creating the welcome route = "the root" which is essentially the home page 
# think of it like a google search for surfer, google homepage will provide you with images, videos, news, maps and more
# all of the routes should go after the app = Flask(__name__) 
# define the welcome route using this code 
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# follow the naming convention /api/v1.0

# create a route for the precipitation analysis 
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all() 
    #create a dictionary with date as key and precipitation as the value 
   return