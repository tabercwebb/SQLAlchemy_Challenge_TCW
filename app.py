# Import Flask
from flask import Flask, jsonify

# Import Dependencies and Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool


##################################################
# Database Setup
##################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an Existing Database Into a New Model
Base = automap_base()

# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station


##################################################
# Flask Setup
##################################################

app = Flask(__name__)

##################################################
# Flask Routes
##################################################

# Welcome Route
@app.route("/")
def welcome():
    return (

        f"Hawaii Climate API<br/><br/>"
        f"Precipitation Analysis: /api/v1.0/precipitation<br/><br/>"
        f"Station Analysis: /api/v1.0/stations<br/><br/>"
        f"Temperature Analysis: /api/v1.0/tobs<br/><br/>"
        f"Start Day Analysis: /api/v1.0/<start><br/><br/>"
        f"Start & End Day Analysis: /api/v1.0/<start><end>"
    )


# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():

        session = Session(engine)
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        prcp_data_one_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
        session.close()

        prcp_data_one_year_list = dict(prcp_data_one_year)
        return jsonify(prcp_data_one_year_list)


# Station Route
@app.route("/api/v1.0/stations")
def station():

        session = Session(engine)
        all_stations = session.query(Station.station, Station.name).all()
        session.close()

        station_list = list(all_stations)
        return jsonify(station_list)

    
# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():

        session = Session(engine)
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs_data_one_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
        session.close()

        tobs_data_list = list(tobs_data_one_year)
        return jsonify(tobs_data_list)


# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):

        session = Session(engine)
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
        session.close()

        start_day_list = list(start_day)
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start><end>")
def start_end_day(start, end):

        session = Session(engine)
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
        session.close()

        start_end_day_list = list(start_end_day)
        return jsonify(start_end_day_list)


if __name__ == '__main__':
    app.run(debug=True)