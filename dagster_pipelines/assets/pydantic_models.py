from ..api_client.geocoding.models import Location
from ..api_client.weather_forecast.models import (
    CurrentWeather,
    HourlyForecast,
    DailyForecast
)

from ..resources import OpenMeteoApiResource
import dagster as dg

@dg.asset(group_name='weather', kinds={'pydantic'})
def location_model(open_meteo: OpenMeteoApiResource) -> Location:
    # replace with config for locations
    geo_client = open_meteo.geocoding_client
    results = geo_client.search('Westbrook')
    redmond = [r for r in results if r.admin1 == 'Connecticut'].pop()
    return redmond

@dg.asset(group_name='weather', kinds={'pydantic'})
def current_weather_model(location_model, open_meteo: OpenMeteoApiResource) -> CurrentWeather:
    forecast_client = open_meteo.weather_forecast_client
    return forecast_client.get_current_weather(location=location_model)

@dg.asset(group_name='weather', kinds={'pydantic'})
def hourly_forecast_model(location_model, open_meteo: OpenMeteoApiResource) -> HourlyForecast:
    forecast_client = open_meteo.weather_forecast_client
    return forecast_client.get_hourly_forecast(location=location_model)

@dg.asset(group_name='weather', kinds={'pydantic'})
def daily_forecast_model(location_model, open_meteo: OpenMeteoApiResource) -> DailyForecast:
    forecast_client = open_meteo.weather_forecast_client
    return forecast_client.get_daily_forecast(location=location_model)
