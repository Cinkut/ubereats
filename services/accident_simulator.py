"""
Symulator wypadków (opcjonalny - logika jest już w State Pattern)

Ten moduł jest rezerwowy - główna logika wypadków jest w ToRestaurantState i ToCustomerState
"""

import random
from models.courier import Courier


class AccidentSimulator:
    """
    Symulator wypadków kurierów
    
    UWAGA: W aktualnej implementacji logika wypadków jest już w State Pattern
    (ToRestaurantState i ToCustomerState). Ta klasa jest opcjonalna i może być
    użyta do dodatkowych funkcji lub statystyk.
    
    Zasady SOLID:
    - Single Responsibility: tylko symulacja wypadków
    """
    
    def __init__(self):
        """Inicjalizuje symulator"""
        self.total_accidents = 0
        self.accidents_per_weather = {}
    
    def check_accident(self, courier: Courier, weather_condition) -> bool:
        """
        Sprawdza czy kurier ma wypadek (dla manualnego użycia)
        
        Args:
            courier: Kurier
            weather_condition: Warunek pogodowy
            
        Returns:
            bool: True jeśli wypadek
        """
        accident_prob = weather_condition.get_accident_probability()
        
        if random.random() < accident_prob:
            self.register_accident(weather_condition.get_name())
            return True
        
        return False
    
    def register_accident(self, weather_name: str):
        """
        Rejestruje wypadek w statystykach
        
        Args:
            weather_name: Nazwa warunku pogodowego
        """
        self.total_accidents += 1
        self.accidents_per_weather[weather_name] = \
            self.accidents_per_weather.get(weather_name, 0) + 1
    
    def get_stats(self) -> dict:
        """
        Zwraca statystyki wypadków
        
        Returns:
            dict: Statystyki
        """
        return {
            'total_accidents': self.total_accidents,
            'accidents_per_weather': self.accidents_per_weather
        }
