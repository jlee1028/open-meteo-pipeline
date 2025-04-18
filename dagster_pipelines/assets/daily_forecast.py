import dagster as dg
from ..resources import PostgresResource
from ..api_client.weather_forecast.schemas import (
    DailyForecastRecord,
    DailyUnitConfigRecord,
    ForecastRunRecord
)

@dg.asset(
        group_name='weather',
        kinds={'postgres'},
        deps=['daily_forecast_model', 'forecast_run__daily_forecast']
        )
def daily_forecast(
    # context: dg.AssetExecutionContext,
    postgres: PostgresResource,
    daily_forecast_model
    ) -> None:
    """write to daily_forecast table in postgres"""
    postgres_session = postgres.session
    daily_forecast_dict = daily_forecast_model.daily.model_dump()

    # add foreign keys
    daily_forecast_dict['unit_config_id'] = daily_forecast_model.daily_units.unit_config_id
    daily_forecast_dict['forecast_run_id'] = daily_forecast_model.forecast_run_id
    daily_forecast_dict['location_id'] = daily_forecast_model.location_id
    
    # insert daily_forecast record
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

@dg.asset(group_name='weather',
          kinds={'postgres'},
          deps=['daily_forecast_model']
          )
def forecast_run__daily_forecast(
    # context: dg.AssetExecutionContext,
    postgres: PostgresResource,
    daily_forecast_model
    ) -> None:
    """write to forecast_run table in postgres"""

    postgres_session = postgres.session
    forecast_run_record = ForecastRunRecord(
        **daily_forecast_model.model_dump(
            exclude=[
                'daily_units',
                'daily'
                ]
            )
        )

    # insert forecast_run record
    postgres_session.add(forecast_run_record)
    postgres_session.commit()

@dg.asset(group_name='weather',
          kinds={'postgres'},
          deps=['daily_forecast_model']
          )
def daily_unit_config(postgres: PostgresResource, daily_forecast_model):
    """write to daily_unit_config table in postgres"""
    postgres_session = postgres.session
    daily_unit_config_record = DailyUnitConfigRecord(**daily_forecast_model.daily_units.model_dump())
    
    # upsert daily_unit_config record
    postgres_session.merge(daily_unit_config_record)
    postgres_session.commit()
