# Python SQL toolkit and Object Relational Mapper
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

database_path = "Resources/hawaii.sqlite"

engine = create_engine(f"sqlite:///{database_path}",connect_args={"check_same_thread": False})
conn = engine.connect()

# reflect an existing database into a new model
base = automap_base()
base.prepare(engine, reflect=True)

base.classes.keys()

session = Session(engine)

ms=base.classes.measurement
st=base.classes.station

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
        f"/api/v1.0/stats<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# Enter the dates fro the start and start/end routes in the format "YYYMMDD"
# Exmaple /api/v1.0/20160823/20170823

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return a list of all precipitation measurements"""
    # Query all measurements
    results = session.query(ms.date, ms.prcp).filter(ms.date >= dt.date(2016,8,23) ).all()

    # Dictionary comprehension
    all_prcp = {date:prcp for date, prcp in results}

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    """Return a list of stations"""
    # Query all measurements
    results = session.query(st.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    """Return a list of temperature measurements"""
    # Query all measurement

    results = session.query(ms.date, ms.tobs).filter(ms.date >= dt.date(2016,8,23) ).all()

    # Convert list of tuples into normal list
    all_tobs = {date:tobs for date, tobs in results}
    
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def stats(start=None,end=None):

    start = dt.datetime(year=int(start[0:4]), month=int(start[4:6]), day=int(start[6:8]))

    if not end:
        results = session.query(func.min(ms.tobs),func.avg(ms.tobs),func.max(ms.tobs))\
        .filter(ms.date >= start).all()
    else:
        end = dt.datetime(year=int(end[0:4]), month=int(end[4:6]), day=int(end[6:8]))
        results = session.query(func.min(ms.tobs),func.avg(ms.tobs),func.max(ms.tobs))\
        .filter(ms.date >= start)\
        .filter(ms.date <= end).all()

    all_stats = list(np.ravel(results))

    return jsonify(all_stats)

if __name__ == '__main__':
    app.run(debug=True,threaded=True)
