from ..base_schema import Base, TimestampMixin
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class CurrentUnitConfigRecord(Base, TimestampMixin):
    __tablename__ = 'weather__current_unit_config'

    time = Column(String)
    precipitation = Column(String)
    weather_code = Column(String)
    cloud_cover = Column(String)
    precipitation_probability = Column(String)
    rain = Column(String)
    temperature_2m = Column(String)
    snowfall = Column(String)
    snow_depth = Column(String)
    wind_speed_10m = Column(String)
    apparent_temperature = Column(String)
    showers = Column(String)
    relative_humidity_2m = Column(String)
    interval = Column(String)
    is_day = Column(String)
    unit_config_id = Column(UUID, primary_key=True)

class CurrentWeatherRecord(Base, TimestampMixin):
    __tablename__ = 'weather__current_weather'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime)
    interval = Column(Integer)
    precipitation = Column(Float)
    weather_code = Column(Integer)
    cloud_cover = Column(Integer)
    precipitation_probability = Column(Integer)
    rain = Column(Float)
    temperature_2m = Column(Float)
    snowfall = Column(Float)
    snow_depth = Column(Float)
    wind_speed_10m = Column(Float)
    apparent_temperature = Column(Float)
    showers = Column(Float)
    is_day = Column(Integer)
    relative_humidity_2m = Column(Integer)

    # foreign keys
    unit_config_id = Column(
        UUID,
        ForeignKey('weather__current_unit_config.unit_config_id')
        )
    forecast_run_id = Column(
        UUID,
        ForeignKey('weather__forecast_run.forecast_run_id')
        )
    location_id = Column(Integer, ForeignKey('weather__location.id'))

class HourlyUnitConfigRecord(Base, TimestampMixin):
    __tablename__ = 'weather__hourly_unit_config'

    time = Column(String)
    precipitation = Column(String)
    weather_code = Column(String)
    cloud_cover = Column(String)
    precipitation_probability = Column(String)
    rain = Column(String)
    temperature_2m = Column(String)
    snowfall = Column(String)
    snow_depth = Column(String)
    wind_speed_10m = Column(String)
    apparent_temperature = Column(String)
    showers = Column(String)
    relative_humidity_2m = Column(String)
    unit_config_id = Column(UUID, primary_key=True)

class HourlyForecastRecord(Base, TimestampMixin):
    __tablename__ = 'weather__hourly_forecast'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime)
    precipitation = Column(Float)
    weather_code = Column(Integer)
    cloud_cover = Column(Integer)
    precipitation_probability = Column(Integer)
    rain = Column(Float)
    temperature_2m = Column(Float)
    snowfall = Column(Float)
    snow_depth = Column(Float)
    wind_speed_10m = Column(Float)
    apparent_temperature = Column(Float)
    showers = Column(Float)
    relative_humidity_2m = Column(Integer)

    # foreign keys
    unit_config_id = Column(
        UUID,
        ForeignKey('weather__hourly_unit_config.unit_config_id')
        )
    forecast_run_id = Column(
        UUID,
        ForeignKey('weather__forecast_run.forecast_run_id')
        )
    location_id = Column(Integer, ForeignKey('weather__location.id'))

class DailyUnitConfigRecord(Base, TimestampMixin):
    __tablename__ = 'weather__daily_unit_config'

    time = Column(String)
    sunshine_duration = Column(String)
    sunrise = Column(String)
    weather_code = Column(String)
    apparent_temperature_max = Column(String)
    rain_sum = Column(String)
    precipitation_sum = Column(String)
    wind_speed_10m_max = Column(String)
    snowfall_sum = Column(String)
    temperature_2m_min = Column(String)
    daylight_duration = Column(String)
    sunset = Column(String)
    temperature_2m_max = Column(String)
    precipitation_probability_max = Column(String)
    apparent_temperature_min = Column(String)
    showers_sum = Column(String)
    precipitation_hours = Column(String)
    unit_config_id = Column(UUID, primary_key=True)

class DailyForecastRecord(Base, TimestampMixin):
    __tablename__ = 'weather__daily_forecast'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime)
    sunshine_duration = Column(Float)
    sunrise = Column(String)
    weather_code = Column(Integer)
    apparent_temperature_max = Column(Float)
    rain_sum = Column(Float)
    precipitation_sum = Column(Float)
    wind_speed_10m_max = Column(Float)
    snowfall_sum = Column(Float)
    temperature_2m_min = Column(Float)
    daylight_duration = Column(Float)
    sunset = Column(String)
    temperature_2m_max = Column(Float)
    precipitation_probability_max = Column(Integer)
    apparent_temperature_min = Column(Float)
    showers_sum = Column(Float)
    precipitation_hours = Column(Float)

    # foreign keys
    unit_config_id = Column(
        UUID,
        ForeignKey('weather__daily_unit_config.unit_config_id')
        )
    forecast_run_id = Column(
        UUID,
        ForeignKey('weather__forecast_run.forecast_run_id')
        )
    location_id = Column(Integer, ForeignKey('weather__location.id'))

class ForecastRunRecord(Base, TimestampMixin):
    __tablename__ = 'weather__forecast_run'

    location_id = Column(Integer, ForeignKey('weather__location.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    generationtime_ms = Column(Float)
    utc_offset_seconds = Column(Integer)
    timezone = Column(String)
    timezone_abbreviation = Column(String)
    elevation = Column(Float)
    forecast_run_id = Column(UUID, primary_key=True)
