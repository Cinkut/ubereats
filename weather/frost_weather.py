"""
Warunek pogodowy: Mróz
"""

from weather.weather_condition import WeatherCondition
import config


class FrostWeather(WeatherCondition):
    """
    Mróz - trudne warunki dostawy
    
    Charakterystyka:
    - 30% wolniej
    - Podwyższone ryzyko wypadku
    - +50% cena
    """
    
    def get_name(self) -> str:
        return "frost"
    
    def get_display_name(self) -> str:
        return "Mroz"
    
    def get_speed_multiplier(self) -> float:
        return config.WEATHER_SPEED_MULTIPLIERS['frost']
    
    def get_accident_probability(self) -> float:
        return config.WEATHER_ACCIDENT_PROBABILITY['frost']
    
    def get_price_multiplier(self) -> float:
        return config.WEATHER_PRICE_MULTIPLIERS['frost']
    
    def get_background_color(self) -> tuple:
        """Jasno-niebieskie tło dla mrozu"""
        return (220, 230, 245)
