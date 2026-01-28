"""
Warunek pogodowy: Gołoledź (szklanka)
"""

from weather.weather_condition import WeatherCondition
import config


class IceWeather(WeatherCondition):
    """
    Gołoledź (szklanka) - ekstremalnie niebezpieczne warunki
    
    Charakterystyka:
    - 60% wolniej
    - NAJWYŻSZE ryzyko wypadku (1.5%)
    - +150% cena
    
    To jest najgorszy warunek pogodowy w systemie!
    """
    
    def get_name(self) -> str:
        return "ice"
    
    def get_display_name(self) -> str:
        return "Gololedz"
    
    def get_speed_multiplier(self) -> float:
        return config.WEATHER_SPEED_MULTIPLIERS['ice']
    
    def get_accident_probability(self) -> float:
        return config.WEATHER_ACCIDENT_PROBABILITY['ice']
    
    def get_price_multiplier(self) -> float:
        return config.WEATHER_PRICE_MULTIPLIERS['ice']
    
    def get_background_color(self) -> tuple:
        """Ciemnoniebieskie tło dla gołoledzi"""
        return (180, 200, 220)
