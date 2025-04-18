from dagster import ConfigurableResource
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from .api_client.base_schema import Base

from .api_client.geocoding.client import GeocodingClient
from .api_client.weather_forecast.client import WeatherForecastClient

class OpenMeteoApiResource(ConfigurableResource):
    ...

    @property
    def geocoding_client(self) -> GeocodingClient:
        return GeocodingClient()
    
    @property
    def weather_forecast_client(self) -> WeatherForecastClient:
        return WeatherForecastClient()

class PostgresResource(ConfigurableResource):
    host: str
    port: int
    database: str
    drivername: str
    username: str
    password: str

    @property
    def session(self):
        postgres_connection_url = URL.create(
            host=self.host,
            port=self.port,
            database=self.database,
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            )
        engine = create_engine(url=postgres_connection_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()
    