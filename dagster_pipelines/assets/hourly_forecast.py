import dagster as dg
from ..resources import PostgresResource
from ..api_client.weather_forecast.schemas import (
    HourlyForecastRecord,
    HourlyUnitConfigRecord,
    ForecastRunRecord
)

@dg.asset(
        group_name='weather',
        kinds={'postgres'},
        deps=['hourly_forecast_model', 'forecast_run__hourly_forecast']
        )
def hourly_forecast(
    # context: dg.AssetExecutionContext,
    postgres: PostgresResource,
    hourly_forecast_model
    ) -> None:
    """write to hourly_forecast table in postgres"""
    postgres_session = postgres.session
    hourly_forecast_dict = hourly_forecast_model.hourly.model_dump()

    # add foreign keys
    hourly_forecast_dict['unit_config_id'] = hourly_forecast_model.hourly_units.unit_config_id
    hourly_forecast_dict['forecast_run_id'] = hourly_forecast_model.forecast_run_id
    hourly_forecast_dict['location_id'] = hourly_forecast_model.location_id
    
    # insert hourly_forecast record
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

@dg.asset(group_name='weather',
          kinds={'postgres'},
          deps=['hourly_forecast_model']
          )
def forecast_run__hourly_forecast(
    # context: dg.AssetExecutionContext,
    postgres: PostgresResource,
    hourly_forecast_model
    ) -> None:
    """write to forecast_run table in postgres"""

    postgres_session = postgres.session
    forecast_run_record = ForecastRunRecord(
        **hourly_forecast_model.model_dump(
            exclude=[
                'hourly_units',
                'hourly'
                ]
            )
        )

    # insert forecast_run record
    postgres_session.add(forecast_run_record)
    postgres_session.commit()

@dg.asset(group_name='weather',
          kinds={'postgres'},
          deps=['hourly_forecast_model']
          )
def hourly_unit_config(postgres: PostgresResource, hourly_forecast_model):
    """write to hourly_unit_config table in postgres"""
    postgres_session = postgres.session
    hourly_unit_config_record = HourlyUnitConfigRecord(**hourly_forecast_model.hourly_units.model_dump())
    
    # upsert hourly_unit_config record
    postgres_session.merge(hourly_unit_config_record)
    postgres_session.commit()
