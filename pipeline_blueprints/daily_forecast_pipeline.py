from __future__ import annotations
from typing import TYPE_CHECKING
import time
from datetime import datetime, timezone
from api_client.geocoding.models import Location
from api_client.geocoding.schemas import LocationRecord
from api_client.weather_forecast.schemas import DailyUnitConfigRecord, DailyForecastRecord, ForecastRunRecord
from api_client.weather_forecast.client import WeatherForecastClient

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from logging import Logger

def daily_forecast_pipeline(location: Location, postgres_session: Session, logger: Logger) -> None:
    '''shred and write daily weather API response to postgres'''

    pipeline_start_time = time.time()
    current_utc = datetime.now(tz=timezone.utc)
    logger.info(f'daily_forecast_pipeline started at {current_utc}')

    # get daily forecast data for location
    weather_client = WeatherForecastClient()

    api_call_start_time = time.time()
    daily_forecast = weather_client.get_daily_forecast(location=location)
    api_call_end_time = time.time()
    logger.info(f'daily forecast data retrieved in {round(api_call_end_time - api_call_start_time, 2)} seconds')

    # shred API response and establish database object models for insert/upsert
    shredding_start_time = time.time()
    loc_record = LocationRecord(**location.model_dump(exclude='postcodes_list'))

    forecast_run_record = ForecastRunRecord(
        **daily_forecast.model_dump(
            exclude=[
                'daily_units',
                'daily'
                ]
            )
        )

    daily_unit_config_record = DailyUnitConfigRecord(
        **daily_forecast.daily_units.model_dump()
        )
    
    daily_forecast_dict = daily_forecast.daily.model_dump()

    # add foreign keys
    daily_forecast_dict['unit_config_id'] = daily_forecast.daily_units.unit_config_id
    daily_forecast_dict['forecast_run_id'] = daily_forecast.forecast_run_id
    daily_forecast_dict['location_id'] = daily_forecast.location_id
    shredding_end_time = time.time()
    logger.info(f'daily forecast data shredded into object models in {round(shredding_end_time - shredding_start_time, 2)} seconds')

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

    # upsert daily_unit_config record
    units_start_time = time.time()
    postgres_session.merge(daily_unit_config_record)
    postgres_session.commit()
    units_end_time = time.time()
    logger.info(f'daily_unit_config record upserted in {round(units_end_time - units_start_time, 2)} seconds')

    # insert daily_forecast record
    daily_start_time = time.time()
    keys = [k for k, v in daily_forecast_dict.items() if type(v) == list]
    daily_weather_records = []

    for i in range(len(daily_forecast_dict['time'])):
        row = {}
        for k in keys:
            row[k] = daily_forecast_dict[k][i]
        row['unit_config_id'] = daily_forecast_dict['unit_config_id']
        row['forecast_run_id'] = daily_forecast_dict['forecast_run_id']
        row['location_id'] = daily_forecast_dict['location_id']
        daily_weather_records.append(row)

    postgres_session.bulk_insert_mappings(DailyForecastRecord, daily_weather_records)
    postgres_session.commit()
    daily_end_time = time.time()
    logger.info(f'daily_forecast records bulk inserted in {round(daily_end_time - daily_start_time, 2)} seconds')

    pipeline_end_time = time.time()
    logger.info(f'daily_forecast_pipeline completed in {round(pipeline_end_time - pipeline_start_time, 2)} seconds')
