from pydantic import BaseModel, Field, computed_field
from typing import Optional
from datetime import datetime
import uuid
from utils import make_guid
import json

class HourlyWeatherVar(BaseModel):
    time: list[datetime]
    precipitation: Optional[list[float]] = None
    weather_code: Optional[list[int]] = None
    cloud_cover: Optional[list[int]] = None
    precipitation_probability: Optional[list[int]] = None
    rain: Optional[list[float]] = None
    temperature_2m: Optional[list[float]] = None
    snowfall: Optional[list[float]] = None
    snow_depth: Optional[list[float]] = None
    wind_speed_10m: Optional[list[float]] = None
    apparent_temperature: Optional[list[float]] = None
    showers: Optional[list[float]] = None
    relative_humidity_2m: Optional[list[int]] = None

class CurrentWeatherVar(BaseModel):
    time: datetime
    interval: Optional[int] = None
    precipitation: Optional[float] = None
    weather_code: Optional[int] = None
    cloud_cover: Optional[int] = None
    precipitation_probability: Optional[int] = None
    rain: Optional[float] = None
    temperature_2m: Optional[float] = None
    snowfall: Optional[float] = None
    snow_depth: Optional[float] = None
    wind_speed_10m: Optional[float] = None
    apparent_temperature: Optional[float] = None
    showers: Optional[float] = None
    is_day: Optional[int] = None
    relative_humidity_2m: Optional[int] = None

class DailyWeatherVar(BaseModel):
    time: list[datetime]
    sunshine_duration: Optional[list[float]] = None
    sunrise: Optional[list[str]] = None
    weather_code: Optional[list[int]] = None
    apparent_temperature_max: Optional[list[float]] = None
    rain_sum: Optional[list[float]] = None
    precipitation_sum: Optional[list[float]] = None
    wind_speed_10m_max: Optional[list[float]] = None
    snowfall_sum: Optional[list[float]] = None
    temperature_2m_min: Optional[list[float]] = None
    daylight_duration: Optional[list[float]] = None
    sunset: Optional[list[str]] = None
    temperature_2m_max: Optional[list[float]] = None
    precipitation_probability_max: Optional[list[int]] = None
    apparent_temperature_min: Optional[list[float]] = None
    showers_sum: Optional[list[float]] = None
    precipitation_hours: Optional[list[float]] = None

class BaseUnits(BaseModel):
    time: Optional[str] = None
    precipitation: Optional[str] = None
    weather_code: Optional[str] = None
    cloud_cover: Optional[str] = None
    precipitation_probability: Optional[str] = None
    rain: Optional[str] = None
    temperature_2m: Optional[str] = None
    snowfall: Optional[str] = None
    snow_depth: Optional[str] = None
    wind_speed_10m: Optional[str] = None
    apparent_temperature: Optional[str] = None
    showers: Optional[str] = None
    relative_humidity_2m: Optional[str] = None

    @computed_field
    def unit_config_id(self) -> uuid.UUID:
        units = [v for k, v in sorted(self.model_dump(exclude='unit_config_id').items())]
        return make_guid(units)

class HourlyUnits(BaseUnits):
    pass

class CurrentUnits(BaseUnits):
    interval: Optional[str] = None
    is_day: Optional[str] = None

class DailyUnits(BaseModel):
    time: Optional[str] = None
    sunshine_duration: Optional[str] = None
    sunrise: Optional[str] = None
    weather_code: Optional[str] = None
    apparent_temperature_max: Optional[str] = None
    rain_sum: Optional[str] = None
    precipitation_sum: Optional[str] = None
    wind_speed_10m_max: Optional[str] = None
    snowfall_sum: Optional[str] = None
    temperature_2m_min: Optional[str] = None
    daylight_duration: Optional[str] = None
    sunset: Optional[str] = None
    temperature_2m_max: Optional[str] = None
    precipitation_probability_max: Optional[str] = None
    apparent_temperature_min: Optional[str] = None
    showers_sum: Optional[str] = None
    precipitation_hours: Optional[str] = None

    @computed_field
    def unit_config_id(self) -> uuid.UUID:
        units = [v for k, v in sorted(self.model_dump(exclude='unit_config_id').items())]
        return make_guid(units)
  
class BaseForecast(BaseModel):
    location_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    generationtime_ms: Optional[float] = None
    utc_offset_seconds: Optional[int] = None
    timezone: Optional[str] = None
    timezone_abbreviation: Optional[str] = None
    elevation: Optional[float] = None
    forecast_run_id: uuid.UUID = Field(default_factory=uuid.uuid4)

class CurrentWeather(BaseForecast):
    current_units: Optional[CurrentUnits] = None
    current: Optional[CurrentWeatherVar] = None

class HourlyForecast(BaseForecast):
    hourly_units: Optional[HourlyUnits] = None
    hourly: Optional[HourlyWeatherVar] = None

class DailyForecast(BaseForecast):
    daily_units: Optional[DailyUnits] = None
    daily: Optional[DailyWeatherVar] = None
