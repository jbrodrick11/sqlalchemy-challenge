#import dependancies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    return (
        f"**Surf's Up API Info**<br/>"
        f"Please see the available routes listed below;<br/>"
        f"<br/>"
        f"<br/>"
        f"-Precipitation Data<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"-Station Data<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"-Temperature Data<br/>"
        f"/api/v1.0/tobs<br/>"
        f'<br/>'
        f"-Temperature Data with Specified Start Date (Replace YYYY-MM-DD in URL with Date to Search)<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"(eg:/api/v1.0/2016-01-28)<br/>"
        f"<br/>"
        f"-Temperature Data with Specified Start and EndDate (Replace YYYY-MM-DD in URL with Dates to Search Between)<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"(eg:/api/v1.0/2015-01-20/2017-01-01)<br/>"
    )

#create route for precipitation data
@app.route("/api/v1.0/precipitation/")
def precipitation():
    #create session
    session = Session(engine)
    #query data using session to get past 12months of precipitation data
    last_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_date = session.query(measurement.date).filter(measurement.date>=last_date).all()
    prcp_pre = session.query(measurement.prcp).filter(measurement.date>=last_date).all()
    #close session
    session.close()
    #flatten lists
    dateinfo = np.ravel(prcp_date)
    prcpinfo = np.ravel(prcp_pre) 
   #convert response to dictionary
    prcp_json = dict(zip(dateinfo, prcpinfo))
    #convert dictionary to json
    return jsonify(prcp_json)

#create route for station data
@app.route("/api/v1.0/stations")
def stations():
    #create session
    session = Session(engine)
    #query data using session to get station data
    station_info = session.query(station.name, station.station).all()
    #close session
    session.close()
    #convert response to dictionary
    station_json = [dict(row) for row in station_info]
    #convert dictionary to json
    return jsonify(station_json)

#create route for temperature data
@app.route("/api/v1.0/tobs")
def tobs():
    #create session
    session = Session(engine)
    #query data using session to get past 12months of temperature data
    last_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_data = session.query(measurement.date, measurement.tobs).filter(measurement.date>=last_date,measurement.station=='USC00519281').all()
    #close session
    session.close()
    #convert response to dictionary
    tobs_json = [dict(row) for row in tobs_data]
    #convert dictionary to json
    return jsonify(tobs_json)

#create route for dynamic start date    
@app.route("/api/v1.0/<start>")
def startdate(start):
    #create session
    session = Session(engine)
    ##return min, avg and max temperatures
    start_info = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date>=start).all()
    #close session
    session.close()
    #return stats as dictionary
    start_json = {'min':start_info[0][0], 'avg':start_info[0][1], 'max':start_info[0][2]}
    #convert dictionary to json
    return jsonify(start_json)

#create route for dynamic start and end date 
@app.route("/api/v1.0/<start>/<end>")
def startenddate(start,end):
    #create session
    session = Session(engine)
    #return min, avg and max temperatures
    end_info = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date>=start).filter(measurement.date<=end).all()
    #close session
    session.close()
    #return stats as dictionary
    end_json = {'min':end_info[0][0], 'avg':end_info[0][1], 'max':end_info[0][2]}
    #convert dictionary to json
    return jsonify(end_json)

if __name__ == "__main__":
    app.run(debug=True)



 