"""
Weather information integration
"""
import python_weather
import asyncio
from typing import Optional
from zeno.core.config import config


class WeatherIntegration:
    """Weather information integration"""
    
    def __init__(self):
        self.default_city = config.DEFAULT_CITY
    
    async def _get_weather_async(self, city: str) -> python_weather.Weather:
        """
        Get weather information asynchronously
        
        Args:
            city: City name to get weather for
            
        Returns:
            Weather object
        """
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get(city)
            return weather
    
    def get_weather(self, city: Optional[str] = None) -> str:
        """
        Get weather information for a city
        
        Args:
            city: City name (uses default if not provided)
            
        Returns:
            Weather description string
        """
        city = city or self.default_city
        
        try:
            weather = asyncio.run(self._get_weather_async(city))
            return str(weather)
        except Exception as e:
            return f"Error getting weather: {str(e)}"
