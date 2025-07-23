import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from config.logger import log


class WeatherClient:
    """Weather API client for current weather and forecasts."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('WEATHER_API_KEY')
        self.base_url = "http://api.weatherapi.com/v1"
        
        if not self.api_key:
            log.warning("Weather API key not found. Set WEATHER_API_KEY environment variable.")
        
        log.info("Weather client initialized")
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Make a request to the Weather API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            
            if not params:
                params = {}
            params['key'] = self.api_key
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            log.error(f"Weather API request failed: {e}")
            return None
        except Exception as e:
            log.error(f"Weather request error: {e}")
            return None
    
    def get_current_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """Get current weather for a location."""
        try:
            params = {'q': location}
            response = self._make_request('current.json', params)
            
            if response and 'current' in response:
                current = response['current']
                location_info = response['location']
                
                weather_data = {
                    'location': location_info['name'],
                    'country': location_info['country'],
                    'temperature_c': current['temp_c'],
                    'temperature_f': current['temp_f'],
                    'condition': current['condition']['text'],
                    'condition_icon': current['condition']['icon'],
                    'humidity': current['humidity'],
                    'wind_kph': current['wind_kph'],
                    'wind_mph': current['wind_mph'],
                    'wind_direction': current['wind_dir'],
                    'pressure_mb': current['pressure_mb'],
                    'feels_like_c': current['feelslike_c'],
                    'feels_like_f': current['feelslike_f'],
                    'uv': current['uv'],
                    'last_updated': current['last_updated']
                }
                
                log.info(f"Retrieved current weather for {location}: {weather_data['temperature_c']}°C, {weather_data['condition']}")
                return weather_data
            else:
                log.error(f"Failed to get current weather for {location}")
                return None
                
        except Exception as e:
            log.error(f"Get current weather error: {e}")
            return None
    
    def get_forecast(self, location: str, days: int = 7) -> Optional[Dict[str, Any]]:
        """Get weather forecast for a location."""
        try:
            params = {
                'q': location,
                'days': days,
                'aqi': 'yes',
                'alerts': 'yes'
            }
            
            response = self._make_request('forecast.json', params)
            
            if response and 'forecast' in response:
                forecast = response['forecast']
                location_info = response['location']
                
                forecast_data = {
                    'location': location_info['name'],
                    'country': location_info['country'],
                    'forecast_days': []
                }
                
                for day in forecast['forecastday']:
                    day_data = {
                        'date': day['date'],
                        'max_temp_c': day['day']['maxtemp_c'],
                        'min_temp_c': day['day']['mintemp_c'],
                        'max_temp_f': day['day']['maxtemp_f'],
                        'min_temp_f': day['day']['mintemp_f'],
                        'condition': day['day']['condition']['text'],
                        'condition_icon': day['day']['condition']['icon'],
                        'max_wind_kph': day['day']['maxwind_kph'],
                        'total_precip_mm': day['day']['totalprecip_mm'],
                        'total_precip_in': day['day']['totalprecip_in'],
                        'avg_humidity': day['day']['avghumidity'],
                        'daily_chance_of_rain': day['day']['daily_chance_of_rain'],
                        'uv': day['day']['uv'],
                        'hourly': []
                    }
                    
                    # Add hourly data
                    for hour in day['hour']:
                        hour_data = {
                            'time': hour['time'],
                            'temp_c': hour['temp_c'],
                            'temp_f': hour['temp_f'],
                            'condition': hour['condition']['text'],
                            'condition_icon': hour['condition']['icon'],
                            'wind_kph': hour['wind_kph'],
                            'wind_mph': hour['wind_mph'],
                            'precip_mm': hour['precip_mm'],
                            'precip_in': hour['precip_in'],
                            'humidity': hour['humidity'],
                            'chance_of_rain': hour['chance_of_rain'],
                            'feels_like_c': hour['feelslike_c'],
                            'feels_like_f': hour['feelslike_f']
                        }
                        day_data['hourly'].append(hour_data)
                    
                    forecast_data['forecast_days'].append(day_data)
                
                log.info(f"Retrieved {days}-day forecast for {location}")
                return forecast_data
            else:
                log.error(f"Failed to get forecast for {location}")
                return None
                
        except Exception as e:
            log.error(f"Get forecast error: {e}")
            return None
    
    def get_weather_alerts(self, location: str) -> Optional[List[Dict[str, Any]]]:
        """Get weather alerts for a location."""
        try:
            params = {'q': location, 'alerts': 'yes'}
            response = self._make_request('forecast.json', params)
            
            if response and 'alerts' in response and response['alerts']['alert']:
                alerts = response['alerts']['alert']
                log.info(f"Retrieved {len(alerts)} weather alerts for {location}")
                return alerts
            else:
                log.info(f"No weather alerts for {location}")
                return []
                
        except Exception as e:
            log.error(f"Get weather alerts error: {e}")
            return None
    
    def get_air_quality(self, location: str) -> Optional[Dict[str, Any]]:
        """Get air quality data for a location."""
        try:
            params = {'q': location, 'aqi': 'yes'}
            response = self._make_request('current.json', params)
            
            if response and 'current' in response and 'air_quality' in response['current']:
                aqi = response['current']['air_quality']
                
                air_quality_data = {
                    'co': aqi.get('co', 0),
                    'no2': aqi.get('no2', 0),
                    'o3': aqi.get('o3', 0),
                    'so2': aqi.get('so2', 0),
                    'pm2_5': aqi.get('pm2_5', 0),
                    'pm10': aqi.get('pm10', 0),
                    'us_epa_index': aqi.get('us-epa-index', 0),
                    'gb_defra_index': aqi.get('gb-defra-index', 0)
                }
                
                log.info(f"Retrieved air quality data for {location}")
                return air_quality_data
            else:
                log.warning(f"No air quality data available for {location}")
                return None
                
        except Exception as e:
            log.error(f"Get air quality error: {e}")
            return None
    
    def get_astronomy(self, location: str, date: str = None) -> Optional[Dict[str, Any]]:
        """Get astronomy data (sunrise, sunset, moonrise, moonset) for a location."""
        try:
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')
            
            params = {'q': location, 'dt': date}
            response = self._make_request('astronomy.json', params)
            
            if response and 'astronomy' in response:
                astronomy = response['astronomy']['astro']
                
                astronomy_data = {
                    'date': date,
                    'sunrise': astronomy['sunrise'],
                    'sunset': astronomy['sunset'],
                    'moonrise': astronomy['moonrise'],
                    'moonset': astronomy['moonset'],
                    'moon_phase': astronomy['moon_phase'],
                    'moon_illumination': astronomy['moon_illumination']
                }
                
                log.info(f"Retrieved astronomy data for {location} on {date}")
                return astronomy_data
            else:
                log.error(f"Failed to get astronomy data for {location}")
                return None
                
        except Exception as e:
            log.error(f"Get astronomy error: {e}")
            return None
    
    def get_marine_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """Get marine weather data for coastal locations."""
        try:
            params = {'q': location}
            response = self._make_request('marine.json', params)
            
            if response and 'marine' in response:
                marine = response['marine']
                
                marine_data = {
                    'location': response['location']['name'],
                    'forecast': []
                }
                
                for day in marine:
                    day_data = {
                        'date': day['date'],
                        'hourly': []
                    }
                    
                    for hour in day['hour']:
                        hour_data = {
                            'time': hour['time'],
                            'temp_c': hour['temp_c'],
                            'temp_f': hour['temp_f'],
                            'wind_speed_kph': hour['wind_speed_kph'],
                            'wind_speed_mph': hour['wind_speed_mph'],
                            'wind_direction': hour['wind_direction'],
                            'wave_height_m': hour['wave_height_m'],
                            'wave_height_ft': hour['wave_height_ft'],
                            'wave_direction': hour['wave_direction'],
                            'wave_period_sec': hour['wave_period_sec'],
                            'water_temp_c': hour['water_temp_c'],
                            'water_temp_f': hour['water_temp_f']
                        }
                        day_data['hourly'].append(hour_data)
                    
                    marine_data['forecast'].append(day_data)
                
                log.info(f"Retrieved marine weather for {location}")
                return marine_data
            else:
                log.warning(f"No marine weather data available for {location}")
                return None
                
        except Exception as e:
            log.error(f"Get marine weather error: {e}")
            return None
    
    def get_historical_weather(self, location: str, date: str) -> Optional[Dict[str, Any]]:
        """Get historical weather data for a specific date."""
        try:
            params = {'q': location, 'dt': date}
            response = self._make_request('history.json', params)
            
            if response and 'forecast' in response:
                forecast = response['forecast']['forecastday'][0]
                
                historical_data = {
                    'date': date,
                    'location': response['location']['name'],
                    'max_temp_c': forecast['day']['maxtemp_c'],
                    'min_temp_c': forecast['day']['mintemp_c'],
                    'avg_temp_c': forecast['day']['avgtemp_c'],
                    'max_wind_kph': forecast['day']['maxwind_kph'],
                    'total_precip_mm': forecast['day']['totalprecip_mm'],
                    'avg_humidity': forecast['day']['avghumidity'],
                    'condition': forecast['day']['condition']['text'],
                    'sunrise': forecast['astro']['sunrise'],
                    'sunset': forecast['astro']['sunset']
                }
                
                log.info(f"Retrieved historical weather for {location} on {date}")
                return historical_data
            else:
                log.error(f"Failed to get historical weather for {location}")
                return None
                
        except Exception as e:
            log.error(f"Get historical weather error: {e}")
            return None
    
    def search_location(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Search for locations by name."""
        try:
            params = {'q': query}
            response = self._make_request('search.json', params)
            
            if response and 'id' in response:
                # Single location result
                return [response]
            elif response and isinstance(response, list):
                # Multiple location results
                log.info(f"Found {len(response)} locations matching '{query}'")
                return response
            else:
                log.warning(f"No locations found for '{query}'")
                return []
                
        except Exception as e:
            log.error(f"Location search error: {e}")
            return None 