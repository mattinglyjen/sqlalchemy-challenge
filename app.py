

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

    """Query the dates and temperature observations for the most active station for the last year"""


@app.route("/api/v1.0/precipitation")
def precipitation():
  
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation dates and measurements"""
    # Query all passengers
    results = session.query(measurement.prcp, measurement.date).all()
    

    session.close()

    # Convert list of tuples into normal list
    precip_all = list(np.ravel(results))
    return jsonify(precip_all)


@app.route("/api/v1.0/stations")
def station():
  
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all passengers
    result = session.query(measurement.station).all()
    

    session.close()

    # Convert list of tuples into normal list
    station_all = list(np.ravel(result))
    return jsonify(station_all)

