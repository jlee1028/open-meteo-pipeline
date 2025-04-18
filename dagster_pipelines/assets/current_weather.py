import dagster as dg
from ..resources import PostgresResource
from ..api_client.weather_forecast.schemas import (
    CurrentWeatherRecord,
    ForecastRunRecord,
    CurrentUnitConfigRecord
)

@dg.asset(
        group_name='weather',
        kinds={'postgres'},
        deps=['current_weather_model', 'forecast_run__current_weather']
        )
def current_weather(
    # context: dg.AssetExecutionContext,
    postgres: PostgresResource,
    current_weather_model
    ) -> None:
    """write to current_weather table in postgres"""
    postgres_session = postgres.session
    current_weather_dict = current_weather_model.current.model_dump()

    # add foreign keys
    current_weather_dict['unit_config_id'] = current_weather_model.current_units.unit_config_id
    current_weather_dict['forecast_run_id'] = current_weather_model.forecast_run_id
    current_weather_dict['location_id'] = current_weather_model.location_id
    current_weather_record = CurrentWeatherRecord(**current_weather_dict)

    # insert current_weather record
    postgres_session.add(current_weather_record)
    postgres_session.commit()

@dg.asset(
        group_name='weather',
        kinds={'postgres'},
        deps=['current_weather_model']
        )
def forecast_run__current_weather(
    # context: dg.AssetExecutionContext,
    postgres: PostgresResource,
    current_weather_model
    ) -> None:
    """write to forecast_run table in postgres"""

    postgres_session = postgres.session
    forecast_run_record = ForecastRunRecord(
        **current_weather_model.model_dump(
            exclude=[
                'current_units',
                'current'
                ]
            )
        )

    # insert forecast_run record
    postgres_session.add(forecast_run_record)
    postgres_session.commit()

@dg.asset(
        group_name='weather',
        kinds={'postgres'},
        deps=['current_weather_model']
        )
def current_unit_config(
    # context: dg.AssetExecutionContext,
    postgres: PostgresResource,
    current_weather_model
    ) -> None:
    """write to current_unit_config table in postgres"""

    postgres_session = postgres.session
    current_unit_config_record = CurrentUnitConfigRecord(**current_weather_model.current_units.model_dump())

    # upsert current_unit_config record
    postgres_session.merge(current_unit_config_record)
    postgres_session.commit()
