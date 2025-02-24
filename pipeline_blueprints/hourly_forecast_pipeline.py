from __future__ import annotations
from typing import TYPE_CHECKING
import time
from datetime import datetime, timezone
from api_client.geocoding.models import Location
from api_client.geocoding.schemas import LocationRecord
from api_client.weather_forecast.schemas import HourlyUnitConfigRecord, HourlyForecastRecord, ForecastRunRecord
from api_client.weather_forecast.client import WeatherForecastClient

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from logging import Logger

def hourly_forecast_pipeline(location: Location, postgres_session: Session, logger: Logger) -> None:
    '''shred and write hourly weather API response to postgres'''

    pipeline_start_time = time.time()
    current_utc = datetime.now(tz=timezone.utc)
    logger.info(f'hourly_forecast_pipeline started at {current_utc}')

    # get hourly forecast data for location
    weather_client = WeatherForecastClient()

    api_call_start_time = time.time()
    hourly_forecast = weather_client.get_hourly_forecast(location=location)
    api_call_end_time = time.time()
    logger.info(f'hourly forecast data retrieved in {round(api_call_end_time - api_call_start_time, 2)} seconds')

    # shred API response and establish database object models for insert/upsert
    shredding_start_time = time.time()
    loc_record = LocationRecord(**location.model_dump(exclude='postcodes_list'))

    forecast_run_record = ForecastRunRecord(
        **hourly_forecast.model_dump(
            exclude=[
                'hourly_units',
                'hourly'
                ]
            )
        )

    hourly_unit_config_record = HourlyUnitConfigRecord(
        **hourly_forecast.hourly_units.model_dump()
        )
    
    hourly_forecast_dict = hourly_forecast.hourly.model_dump()
    
    # add foreign keys
    hourly_forecast_dict['unit_config_id'] = hourly_forecast.hourly_units.unit_config_id
    hourly_forecast_dict['forecast_run_id'] = hourly_forecast.forecast_run_id
    hourly_forecast_dict['location_id'] = hourly_forecast.location_id
    shredding_end_time = time.time()
    logger.info(f'hourly forecast data shredded into object models in {round(shredding_end_time - shredding_start_time, 2)} seconds')

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

    # upsert hourly_unit_config record
    units_start_time = time.time()
    postgres_session.merge(hourly_unit_config_record)
    postgres_session.commit()
    units_end_time = time.time()
    logger.info(f'hourly_unit_config record upserted in {round(units_end_time - units_start_time, 2)} seconds')

    # insert hourly_forecast record
    hourly_start_time = time.time()
    keys = [k for k, v in hourly_forecast_dict.items() if type(v) == list]
    hourly_weather_records = []

    for i in range(len(hourly_forecast_dict['time'])):
        row = {}
        for k in keys:
            row[k] = hourly_forecast_dict[k][i]
        row['unit_config_id'] = hourly_forecast_dict['unit_config_id']
        row['forecast_run_id'] = hourly_forecast_dict['forecast_run_id']
        row['location_id'] = hourly_forecast_dict['location_id']
        hourly_weather_records.append(row)

    postgres_session.bulk_insert_mappings(HourlyForecastRecord, hourly_weather_records)
    postgres_session.commit()
    hourly_end_time = time.time()
    logger.info(f'hourly_forecast records bulk inserted in {round(hourly_end_time - hourly_start_time, 2)} seconds')

    pipeline_end_time = time.time()
    logger.info(f'hourly_forecast_pipeline completed in {round(pipeline_end_time - pipeline_start_time, 2)} seconds')
