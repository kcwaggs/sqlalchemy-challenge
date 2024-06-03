# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
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
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;'>/api/v1.0/&lt;start&gt;</a><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;/&lt;end&gt;'>/api/v1.0/&lt;start&gt;/&lt;end&gt;</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of your dictionary."""
    # Calculate the date 1 year ago from the last data point in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Perform a query to retrieve all stations
    results = session.query(Station.station).all()

    # Convert the query results to a list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""
    # Calculate the date 1 year ago from the last data point in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the temperature observations
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()

    # Convert the query results to a list of dictionaries
    temperature_observation_list = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temperature_observation_list.append(temp_dict)

    return jsonify(temperature_observation_list)

@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start."""
    # Perform a query to calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Convert the query results to a list
    temperature_stats = list(np.ravel(results))

    return jsonify(temperature_stats)

@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_range(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range."""
    # Perform a query to calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert the query results to a list
    temperature_stats = list(np.ravel(results))

    return jsonify(temperature_stats)

if __name__ == '__main__':
    app.run(debug=True)