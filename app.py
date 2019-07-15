import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup (SQLLITE)
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

################################################
# Database Setup (PostgreSQL)
################################################
engine_station = create_engine("postgresql://postgres:postgres@localhost/adv_sql_db")

# reflect an existing database into a new model
Base_station = automap_base()
# reflect the tables
Base_station.prepare(engine_station, reflect=True)

# Save reference to the table
Stations = Base_station.classes.weather_stations

# Create our session (link) from Python to the DB
session_station = Session(engine_station)


################################################
# Flask Setup
################################################
app = Flask(__name__)


################################################
# Flask Routes
################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs_prior_year <br/>"
        f"/api/v1.0/trip_date_temp_stats"
    )


@app.route("/api/v1.0/precipitation")
def prcp_values():
    """Return a list of date and percipitation values"""
    # Query all dates & percipation 
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into a dict, then list the dict for json
    all_prcp = dict(results)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations_names():
    """Return list of station names"""
    # Query all station names 
    results = session_station.query(Stations.station, Stations.name).all()
    
    # Convert list of tuples into normal list
    all_stations = dict(results)

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs_prior_year")
def tobs_prior_year_values():
    """Return a list of date and temperature values for prior year"""
    # Query all temp for prior year 
    results = session.query(Measurement.date, Measurement.tobs).\
      filter(Measurement.date.between('2015-01-01','2015-12-31') ).all()

    # Convert list of tuples into normal list
    all_tobs_prior_year = dict(results)

    return jsonify(all_tobs_prior_year)


@app.route("/api/v1.0/trip_date_temp_stats")
def trip_date_start():
    """Return a list of list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""

    # Query all min, max, and avg temp during trip
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
      filter(Measurement.date.between('2016-01-01','2016-01-31') ).all()

    # Create a dictionary from the row data and append to a list of temp stats
    trip_tobs_stats = []
    for min_temp, max_temp, avg_temp in results:
        temp_stats_dict = {}
        temp_stats_dict["Min Temp"] = min_temp
        temp_stats_dict["Max Temp"] = max_temp
        temp_stats_dict["Avg Temp"] = avg_temp
        trip_tobs_stats.append(temp_stats_dict)

    return jsonify(trip_tobs_stats)


if __name__ == '__main__':
    app.run(debug=True)
