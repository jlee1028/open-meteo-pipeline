from __future__ import annotations
from typing import TYPE_CHECKING
import time
from datetime import datetime, timezone
from api_client.geocoding.models import Location
from api_client.geocoding.schemas import LocationRecord
from api_client.weather_forecast.schemas import CurrentUnitConfigRecord, CurrentWeatherRecord, ForecastRunRecord
from api_client.weather_forecast.client import WeatherForecastClient

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from logging import Logger

def current_weather_pipeline(location: Location, postgres_session: Session, logger: Logger) -> None:
    '''shred and write current weather API response to postgres'''

    pipeline_start_time = time.time()
    current_utc = datetime.now(tz=timezone.utc)
    logger.info(f'current_weather_pipeline started at {current_utc}')

    # get current weather data for location
    weather_client = WeatherForecastClient()

    api_call_start_time = time.time()
    current_weather = weather_client.get_current_weather(location=location)
    api_call_end_time = time.time()
    logger.info(f'current weather data retrieved in {round(api_call_end_time - api_call_start_time, 2)} seconds')

    # shred API response and establish database object models for insert/upsert
    shredding_start_time = time.time()
    loc_record = LocationRecord(**location.model_dump(exclude='postcodes_list'))
    forecast_run_record = ForecastRunRecord(
        **current_weather.model_dump(
            exclude=[
                'current_units',
                'current'
                ]
            )
        )
    current_unit_config_record = CurrentUnitConfigRecord(**current_weather.current_units.model_dump())
    current_weather_dict = current_weather.current.model_dump()

    # add foreign keys
    current_weather_dict['unit_config_id'] = current_weather.current_units.unit_config_id
    current_weather_dict['forecast_run_id'] = current_weather.forecast_run_id
    current_weather_dict['location_id'] = current_weather.location_id
    current_weather_record = CurrentWeatherRecord(**current_weather_dict)

    shredding_end_time = time.time()
    logger.info(f'current weather data shredded into object models in {round(shredding_end_time - shredding_start_time, 2)} seconds')

    # upsert location record
    loc_start_time = time.time()
    postgres_session.merge(loc_record)
    postgres_session.commit()
    loc_end_time = time.time()
    logger.info(f'location record upserted in {round(loc_end_time - loc_start_time, 2)} seconds')

    # insert forecast_run record
    forecast_run_start_time = time.time()
    postgres_session.add(forecast_run_record)
    postgres_session.commit()
    forecast_run_end_time = time.time()
    logger.info(f'forecast_run record inserted in {round(forecast_run_end_time - forecast_run_start_time, 2)} seconds')

    # upsert current_unit_config record
    units_start_time = time.time()
    postgres_session.merge(current_unit_config_record)
    postgres_session.commit()
    units_end_time = time.time()
    logger.info(f'current_unit_config record upserted in {round(units_end_time - units_start_time, 2)} seconds')

    # insert current_weather record
    current_start_time = time.time()
    postgres_session.add(current_weather_record)
    postgres_session.commit()
    current_end_time = time.time()
    logger.info(f'current_weather record inserted in {round(current_end_time - current_start_time, 2)} seconds')

    pipeline_end_time = time.time()
    logger.info(f'current_weather_pipeline completed in {round(pipeline_end_time - pipeline_start_time, 2)} seconds')
