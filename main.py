import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from api_client.geocoding.client import GeocodingClient
from api_client.base_schema import Base
from pipeline_blueprints.current_weather_pipeline import current_weather_pipeline
from pipeline_blueprints.daily_forecast_pipeline import daily_forecast_pipeline
from pipeline_blueprints.hourly_forecast_pipeline import hourly_forecast_pipeline
from utils import get_logger

load_dotenv()

logger = get_logger('weather_pipeline_logger')

# get redmond Location
geo_client = GeocodingClient()
results = geo_client.search('Redmond')
redmond = [r for r in results if r.admin1 == 'Washington'].pop()

# get postgres session
postgres_connection_url = URL.create(
    host=os.getenv('POSTGRES_ENDPOINT'),
    port=5432,
    database=os.getenv('POSTGRES_DB'),
    drivername="postgresql",
    username=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
    )
engine = create_engine(url=postgres_connection_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# execute current weather pipeline
current_weather_pipeline(location=redmond, postgres_session=session, logger=logger)

# execute daily forecast pipeline
daily_forecast_pipeline(location=redmond, postgres_session=session, logger=logger)

# execute hourly forecast pipeline
hourly_forecast_pipeline(location=redmond, postgres_session=session, logger=logger)
