"""
Wzorzec Strategy - abstrakcyjna klasa bazowa dla strategii cenowych

Demonstracja Strategy Pattern i Open/Closed Principle
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from weather.weather_condition import WeatherCondition


class PricingContext:
    """
    Kontekst przekazywany do strategii cenowych
    
    Zawiera wszystkie informacje potrzebne do obliczenia ceny
    """
    
    def __init__(
        self,
        distance: float,
        num_available_couriers: int,
        num_active_orders: int,
        weather_condition: 'WeatherCondition'
    ):
        self.distance = distance
        self.num_available_couriers = num_available_couriers
        self.num_active_orders = num_active_orders
        self.weather_condition = weather_condition


class PricingStrategy(ABC):
    """
    Abstrakcyjna klasa bazowa dla strategii cenowych
    
    Wzorce projektowe:
    - Strategy Pattern: różne algorytmy cenowe
    
    Zasady SOLID:
    - Open/Closed: nowe strategie bez modyfikacji tej klasy
    - Liskov Substitution: wszystkie strategie są wymienne
    - Single Responsibility: każda strategia odpowiada za jeden aspekt ceny
    """
    
    @abstractmethod
    def calculate(self, context: PricingContext) -> float:
        """
        Oblicza składową ceny
        
        Args:
            context: Kontekst z danymi do obliczenia ceny
            
        Returns:
            float: Składowa ceny w $
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Nazwa strategii
        
        Returns:
            str: Nazwa
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
