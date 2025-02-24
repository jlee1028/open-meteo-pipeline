from ..rest_adapter import RestAdapter
from ..exceptions import ApiDataException
from json.decoder import JSONDecodeError
from .models import CurrentWeather, HourlyForecast, DailyForecast
from api_client.geocoding.models import Location

class WeatherForecastClient:
    def __init__(self):
        self._rest_adapter = RestAdapter(api='api')
        self.endpoint = '/v1/forecast'

    def _get_forecast(
            self,
            location: Location,
            forecast_days: int=7,
            past_days: int=0,
            temperature_unit: str='fahrenheit',
            wind_speed_unit: str='mph',
            precipitation_unit: str='inch',
            hourly_weather_vars: list=[],
            current_weather_vars: list=[],
            daily_weather_vars: list=[],
            ):
        latitude = location.latitude
        longitude = location.longitude
        timezone = location.timezone
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'timezone': timezone,
            'forecast_days': forecast_days,
            'past_days': past_days,
            'temperature_unit': temperature_unit,
            'wind_speed_unit': wind_speed_unit,
            'precipitation_unit': precipitation_unit,
            'hourly': hourly_weather_vars,
            'current': current_weather_vars,
            'daily': daily_weather_vars
            }
        return self._rest_adapter.get(endpoint=self.endpoint, params=params)
    

    def get_current_weather(
            self,
            location: Location,
            forecast_days: int=7,
            past_days: int=0,
            temperature_unit: str='fahrenheit',
            wind_speed_unit: str='mph',
            precipitation_unit: str='inch',
            current_weather_vars: list=[]
            ) -> CurrentWeather:
        
        current = list(set([
            'temperature_2m',
            'relative_humidity_2m',
            'apparent_temperature',
            'cloud_cover',
            'precipitation_probability',
            'precipitation',
            'rain',
            'showers',
            'snowfall',
            'snow_depth',
            'weather_code',
            'wind_speed_10m',
            'is_day'
            ] + current_weather_vars))
            
        resp = self._get_forecast(
            location=location,
            forecast_days=forecast_days,
            past_days=past_days,
            temperature_unit=temperature_unit,
            wind_speed_unit=wind_speed_unit,
            precipitation_unit=precipitation_unit,
            current_weather_vars=current
        )
        try:
            data = resp.json()
            data['location_id'] = location.id
            return CurrentWeather(**data)
        except (ValueError, JSONDecodeError) as e:
            raise ApiDataException('Bad JSON in response') from e

    def get_hourly_forecast(
            self,
            location: Location,
            forecast_days: int=7,
            past_days: int=0,
            temperature_unit: str='fahrenheit',
            wind_speed_unit: str='mph',
            precipitation_unit: str='inch',
            hourly_weather_vars: list=[]
            ) -> HourlyForecast:
        
        hourly = list(set([
            'temperature_2m',
            'relative_humidity_2m',
            'apparent_temperature',
            'cloud_cover',
            'precipitation_probability',
            'precipitation',
            'rain',
            'showers',
            'snowfall',
            'snow_depth',
            'weather_code',
            'wind_speed_10m'
            ] + hourly_weather_vars))
            
        resp = self._get_forecast(
            location=location,
            forecast_days=forecast_days,
            past_days=past_days,
            temperature_unit=temperature_unit,
            wind_speed_unit=wind_speed_unit,
            precipitation_unit=precipitation_unit,
            hourly_weather_vars=hourly
        )
        try:
            data = resp.json()
            data['location_id'] = location.id
            return HourlyForecast(**data)
        except (ValueError, JSONDecodeError) as e:
            raise ApiDataException('Bad JSON in response') from e

    def get_daily_forecast(
            self,
            location: Location,
            forecast_days: int=7,
            past_days: int=0,
            temperature_unit: str='fahrenheit',
            wind_speed_unit: str='mph',
            precipitation_unit: str='inch',
            daily_weather_vars: list=[]
            ) -> DailyForecast:
        
        daily = list(set(['weather_code',
                'temperature_2m_max',
                'temperature_2m_min',
                'apparent_temperature_max',
                'apparent_temperature_min',
                'sunrise',
                'sunset',
                'daylight_duration',
                'sunshine_duration',
                'precipitation_sum',
                'rain_sum',
                'showers_sum',
                'snowfall_sum',
                'precipitation_hours',
                'precipitation_probability_max',
                'wind_speed_10m_max'] + daily_weather_vars))
            
        resp = self._get_forecast(
            location=location,
            forecast_days=forecast_days,
            past_days=past_days,
            temperature_unit=temperature_unit,
            wind_speed_unit=wind_speed_unit,
            precipitation_unit=precipitation_unit,
            daily_weather_vars=daily
        )
        try:
            data = resp.json()
            data['location_id'] = location.id
            return DailyForecast(**data)
        except (ValueError, JSONDecodeError) as e:
            raise ApiDataException('Bad JSON in response') from e
