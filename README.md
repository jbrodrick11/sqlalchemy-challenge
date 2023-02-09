# sqlalchemy-challenge

Initially used 

#create route for precipitation data
@app.route("/api/v1.0/precipitation/")
def precipitation():
    #create session
    session = Session(engine)
    #query data using session to get past 12months of precipitation data
    last_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_date = session.query(measurement.date, measurement.prcp).filter(measurement.date>=last_date).all()
    #close session
    session.close()
    #convert response to dictionary
    prcp_json = [dict(row) for row in prcp_date]
    #convert dictionary to json
    return jsonify(prcp_json)

But realised JSON output does not match task criteria 