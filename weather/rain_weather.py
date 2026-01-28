"""
Warunek pogodowy: Deszcz
"""

from weather.weather_condition import WeatherCondition
import config


class RainWeather(WeatherCondition):
    """
    Deszcz - utrudnione warunki dostawy
    
    Charakterystyka:
    - 20% wolniej
    - Niskie ryzyko wypadku
    - +30% cena
    """
    
    def get_name(self) -> str:
        return "rain"
    
    def get_display_name(self) -> str:
        return "Deszcz"
    
    def get_speed_multiplier(self) -> float:
        return config.WEATHER_SPEED_MULTIPLIERS['rain']
    
    def get_accident_probability(self) -> float:
        return config.WEATHER_ACCIDENT_PROBABILITY['rain']
    
    def get_price_multiplier(self) -> float:
        return config.WEATHER_PRICE_MULTIPLIERS['rain']
    
    def get_background_color(self) -> tuple:
        """Niebiesko-szare tło dla deszczu"""
        return (200, 210, 220)
