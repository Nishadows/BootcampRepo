# Import Dependencies
import numpy as np
import datetime as dt
from datetime import datetime

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from flask import Flask, jsonify

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect database model
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = scoped_session(sessionmaker(bind=engine))

# Create App
app = Flask(__name__)

# Create routes
# Root route
@app.route("/")
def welcome():
    """List of available routes."""
    return(
        f"Available routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start_date&gt;<br/>"
        f"/api/v1.0/&lt;start_date&gt;/&lt;end_date&gt;"
    )

# Precipitation route - for all stations, previous year from last data point
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Run Analysis 
    max_date = session.query(func.max(Measurement.date)).all()
    year_ago = dt.datetime.strptime(max_date[0][0], '%Y-%m-%d').date()-dt.timedelta(12*365/12)
    one_year_data = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= func.strftime("%Y-%m-%d",year_ago)).all()

    # Return Results
    prcp_data = []
    for mdate, prcp in one_year_data:
        prcp_dict = {}
        prcp_dict[mdate] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

# Stations route - list all stations
@app.route("/api/v1.0/stations")
def stations():
    # Run Analysis 
    stations = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    # Return Results
    stations_data = []
    for id, station, name, latitude, longitude, elevation in stations:
        stations_dict = {}
        stations_dict["id"] = id
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["latitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        stations_data.append(stations_dict)
    return jsonify(stations_data)   

# Temperatures route - for only active station, previous year
@app.route("/api/v1.0/tobs")
def tobs():
    # Run Analysis  
    station_temp_count = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).filter(Measurement.tobs.isnot(None)).\
        order_by(func.count(Measurement.tobs).desc()).first()
    station_max_date = session.query(func.max(Measurement.date)).filter(Measurement.station == station_temp_count[0]).all()
    station_year_ago = dt.datetime.strptime(station_max_date[0][0], '%Y-%m-%d').date()-dt.timedelta(12*365/12)
    station_one_year_data = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= func.strftime("%Y-%m-%d",station_year_ago)).\
        order_by(Measurement.date).all()
        
    # Return Results
    temp_data = []
    for tdate, tobs in station_one_year_data:
        temp_dict = {}
        temp_dict["date"] = tdate
        temp_dict["temperature"] = tobs
        temp_data.append(temp_dict)
    return jsonify(temp_data)    

# Temperatures route - for all stations, previous year data from latest data point
@app.route("/api/v1.0/temperatures")
def temperatures():
    # Run Analysis 
    max_date = session.query(func.max(Measurement.date)).all()
    year_ago = dt.datetime.strptime(max_date[0][0], '%Y-%m-%d').date()-dt.timedelta(12*365/12)
    tobs_one_year_data = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= func.strftime("%Y-%m-%d",year_ago)).\
        order_by(Measurement.date).all()
        
    # Return Results
    temp_data = []
    for tdate, tobs in tobs_one_year_data:
        temp_dict = {}
        temp_dict["date"] = tdate
        temp_dict["temperature"] = tobs
        temp_data.append(temp_dict)
    return jsonify(temp_data) 

# Temperature Stats by Date route - for dates greater than start date inclusive (not previous year)
@app.route("/api/v1.0/<start_date>")
def startstat(start_date):
    # Run Analysis 
    tobs_stats_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
        
    # Return Results
    tempstats_data = []
    for mintobs, avgtobs, maxtobs in tobs_stats_data:
        tempstats_dict = {}
        tempstats_dict["TMIN"] = mintobs
        tempstats_dict["TAVG"] = avgtobs
        tempstats_dict["TMAX"] = maxtobs
        tempstats_data.append(tempstats_dict)
    return jsonify(tempstats_data) 

# Temperature Stats by Date Range route - for dates between the start and end date inclusive (not previous year)
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_stat(start_date, end_date):
    # Run Analysis 
    tobs_stats_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        
    # Return Results
    tempstats_data = []
    for mintobs, avgtobs, maxtobs in tobs_stats_data:
        tempstats_dict = {}
        tempstats_dict["TMIN"] = mintobs
        tempstats_dict["TAVG"] = avgtobs
        tempstats_dict["TMAX"] = maxtobs
        tempstats_data.append(tempstats_dict)
    return jsonify(tempstats_data) 


if __name__ == '__main__':
    app.run(debug=True)

