

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
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
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

    """Query the dates and temperature observations for the most active station for the last year"""


@app.route("/api/v1.0/precipitation")
def precipitation():
  
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation dates and measurements"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()


    prcp_all = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation"] = prcp
        
        prcp_all.append(precip_dict)

    return jsonify(prcp_all)


@app.route("/api/v1.0/stations")
def station():
  
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all passengers
    result = session.query(measurement.station).all()
    

    session.close()

    # Convert list of tuples into normal list
    station_all = list(np.unique(result))
    return jsonify(station_all)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures for prior year"""
    session = Session(engine)
    date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date > year).\
        order_by(measurement.date).all()

    session.close()
# Create a list of dicts with `date` and `tobs` as the keys and values
    temperature_totals = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temperature_totals.append(row)

    return jsonify(temperature_totals)


@app.route("/api/v1.0/<start>")
def start(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
    start= dt.datetime.strptime(start, '%Y-%m-%d')
    year = dt.timedelta(days=365)
    start = start-year
    end =  dt.date(2017, 8, 23)
    session = Session(engine)
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
        
    trip = list(np.ravel(trip_data))
    return jsonify(trip)
        



#########################################################################################
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    session = Session(engine)
  # go back one year from start/end date and get Min/Avg/Max temp     
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    year = dt.timedelta(days=365)
    start = start_date-year
    end = end_date-year
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()


    session.close()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)
        




if __name__ == '__main__':
    app.run(debug=True)
