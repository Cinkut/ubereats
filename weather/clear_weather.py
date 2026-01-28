"""
Warunek pogodowy: Czyste niebo
"""

from weather.weather_condition import WeatherCondition
import config


class ClearWeather(WeatherCondition):
    """
    Czyste niebo - optymalne warunki dostawy
    
    Charakterystyka:
    - Normalna prędkość
    - Minimalne ryzyko wypadku
    - Normalna cena
    """
    
    def get_name(self) -> str:
        return "clear"
    
    def get_display_name(self) -> str:
        return "Czyste niebo"
    
    def get_speed_multiplier(self) -> float:
        return config.WEATHER_SPEED_MULTIPLIERS['clear']
    
    def get_accident_probability(self) -> float:
        return config.WEATHER_ACCIDENT_PROBABILITY['clear']
    
    def get_price_multiplier(self) -> float:
        return config.WEATHER_PRICE_MULTIPLIERS['clear']
    
    def get_background_color(self) -> tuple:
        """Jasne tło dla czystego nieba"""
        return (240, 240, 245)  # Prawie biały z lekkim odcieniem błękitu
