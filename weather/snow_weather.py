"""
Warunek pogodowy: Śnieg
"""

from weather.weather_condition import WeatherCondition
import config


class SnowWeather(WeatherCondition):
    """
    Śnieg - znacznie utrudnione warunki dostawy
    
    Charakterystyka:
    - 40% wolniej
    - Średnie ryzyko wypadku
    - +60% cena
    """
    
    def get_name(self) -> str:
        return "snow"
    
    def get_display_name(self) -> str:
        return "Snieg"
    
    def get_speed_multiplier(self) -> float:
        return config.WEATHER_SPEED_MULTIPLIERS['snow']
    
    def get_accident_probability(self) -> float:
        return config.WEATHER_ACCIDENT_PROBABILITY['snow']
    
    def get_price_multiplier(self) -> float:
        return config.WEATHER_PRICE_MULTIPLIERS['snow']
    
    def get_background_color(self) -> tuple:
        """Białe tło dla śniegu"""
        return (230, 235, 240)
