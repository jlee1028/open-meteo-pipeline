from dagster import (
    Definitions,
    # EnvVar,
    load_assets_from_modules
)
from .resources import PostgresResource, OpenMeteoApiResource
from .assets import (
    pydantic_models,
    location,
    current_weather,
    daily_forecast,
    hourly_forecast
)
from .utils import get_secret

postgres_credentials = get_secret(secret_name='jws_db_credentials', region_name='us-west-2')

defs = Definitions(
    assets=load_assets_from_modules([
        pydantic_models,
        location,
        current_weather,
        daily_forecast,
        hourly_forecast
        ]),
    resources={
        "postgres": PostgresResource(
            host=postgres_credentials['db_endpoint'],
            port=5432,
            database='jws_db_dev',
            drivername="postgresql",
            username=postgres_credentials['dev_user'],
            password=postgres_credentials['dev_password']
        ),
        "open_meteo": OpenMeteoApiResource()
    }
)
