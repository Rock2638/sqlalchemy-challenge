# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

from datetime import datetime as dt
from datetime import timedelta

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
# engine = create_engine("sqlite:///hawaii.sqlite")
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Rock's API:<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/specify a start date with format yyyy-mm-dd<br/>"
        f"/api/v1.0/specify a start date with format yyyy-mm-dd/specify a end date with format yyyy-mm-dd<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary by using date as the key and prcp as the value."""
    # Query to retrieve the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()

    session.close()

    # Convert the query results to a dictionary by using date as the key and prcp as the value.
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_results = session.query(Station.station,Station.name).all()

    session.close()

    # Convert the query results to a dictionary by using date as the key and prcp as the value.
    all_stations = []
    for station, name in station_results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)


# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set.
    most_recent_date_result = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Extract the date from the result
    most_recent_date = most_recent_date_result[0]
    most_recent_date_dt = (dt.strptime(most_recent_date, '%Y-%m-%d'))

    most_active_station = session.query(Measurement.station,func.count(Measurement.id).label('row_count')). \
        group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
    
    most_active_station_id = most_active_station[0].station

    # Use 12 months from last date in the data
    twelve_months_ago = (most_recent_date_dt- timedelta(days=365)).date()

    # Query to get the last 12 months of temperature data for the most active station
    tobs_results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == most_active_station_id). \
        filter(Measurement.date >= twelve_months_ago).all()

    session.close()

    # Convert the query results to a dictionary by using date as the key and prcp as the value.
    all_tobs = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start.
@app.get('/api/v1.0/<start_date>')
def start(start_date):
 
    # Convert the string to a date 
    start_date_dt = (dt.strptime(start_date, '%Y-%m-%d'))

    session = Session(engine)

    # Do a query to get the minimum temperature, the average temperature, and the maximum temperature for the start_date
    temperature_info_results = session.query(func.min(Measurement.tobs).label('min_temperature'),func.max(Measurement.tobs).label('max_temperature'), \
    func.avg(Measurement.tobs).label('avg_temperature')).filter(Measurement.date >= start_date_dt.date()).one()

    session.close()

    # Convert the query results to a dictionary by using date as the key and temperature as the value.  No need to loop as only one result is returned from query
    temperature_info_dict = {}
    temperature_info_dict["Min Temp"] = temperature_info_results.min_temperature
    temperature_info_dict["Max Temp"] = temperature_info_results.max_temperature
    temperature_info_dict["Avg Temp"] = temperature_info_results.avg_temperature

    return jsonify(temperature_info_dict)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start.
@app.get('/api/v1.0/<start_date>/<end_date>')
def start_end(start_date,end_date):

     # Convert the string to a date 
    start_date_dt = (dt.strptime(start_date, '%Y-%m-%d'))
    end_date_dt = (dt.strptime(end_date, '%Y-%m-%d'))

    session = Session(engine)

    # Do a query to get the minimum temperature, the average temperature, and the maximum temperature for the start_date and end_date
    temperature_info_results = session.query(func.min(Measurement.tobs).label('min_temperature'),func.max(Measurement.tobs).label('max_temperature'), \
    func.avg(Measurement.tobs).label('avg_temperature')).filter(Measurement.date.between(start_date_dt, end_date_dt)).one()
    
    session.close()

    # Convert the query results to a dictionary by using date as the key and temperature as the value.  No need to loop as only one result is returned from query
    temperature_info_dict = {}
    temperature_info_dict["Min Temp"] = temperature_info_results.min_temperature
    temperature_info_dict["Max Temp"] = temperature_info_results.max_temperature
    temperature_info_dict["Avg Temp"] = temperature_info_results.avg_temperature

    return jsonify(temperature_info_dict)

  

if __name__ == '__main__':
    app.run(debug=True)










