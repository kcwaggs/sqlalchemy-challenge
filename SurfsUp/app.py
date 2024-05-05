# Import the dependencies.
import numpy as np
import datetime as dt
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
def one_year_data ():
    '''Getting the last year's data'''
    with Session(engine) as session: 
        
        most_recent_date = session.query(func.max(measurement.date)).scalar()
        most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
        last_year_data = most_recent_date - dt.timedelta(days = 365)
        precipitation_data = session.query(measurement.date, measurement.prcp).\
            filter(measurement.date >= last_year_data).all()
        precipitation_df = pd.DataFrame(precipitation_data, columns = ['date', 'precipitation'])
        precipitation_df = precipitation_df.sort_values('date', ascending = True)
        
        return most_recent_date, last_year_data
    

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
