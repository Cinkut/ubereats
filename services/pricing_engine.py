"""
Silnik cenowy - oblicza ceny dostaw

Wykorzystuje wzorzec Strategy dla różnych strategii cenowych
"""

from typing import List
from strategies.pricing_strategy import PricingStrategy, PricingContext
from strategies.base_pricing import BasePricing
from strategies.surge_pricing import SurgePricing
from strategies.weather_pricing import WeatherPricing


class PricingEngine:
    """
    Silnik obliczający ceny dostaw
    
    Wzorce projektowe:
    - Strategy Pattern: używa różnych strategii cenowych
    - Composite: łączy wiele strategii
    
    Zasady SOLID:
    - Single Responsibility: tylko obliczanie cen
    - Open/Closed: łatwo dodać nowe strategie
    - Dependency Inversion: zależy od abstrakcji PricingStrategy
    """
    
    def __init__(self):
        """Inicjalizuje silnik cenowy"""
        # Lista strategii cenowych
        self.strategies: List[PricingStrategy] = [
            BasePricing(),
            SurgePricing(),
            WeatherPricing()
        ]
        
        # Instancja SurgePricing dla obliczania mnożnika
        self._surge_strategy = SurgePricing()
    
    def calculate_price(
        self,
        distance: float,
        num_available_couriers: int,
        num_active_orders: int,
        weather_condition
    ) -> tuple:
        """
        Oblicza całkowitą cenę dostawy
        
        Cena składa się z:
        - Opłaty bazowej (stała + dystans)
        - Surge pricing (popyt vs podaż) - NIELINIOWY!
        - Opłaty pogodowej (trudne warunki)
        
        Args:
            distance: Dystans dostawy
            num_available_couriers: Liczba dostępnych kurierów
            num_active_orders: Liczba aktywnych zamówień
            weather_condition: Aktualny warunek pogodowy
            
        Returns:
            tuple: (total_price, surge_multiplier)
        """
        # Utwórz kontekst cenowy
        context = PricingContext(
            distance=distance,
            num_available_couriers=num_available_couriers,
            num_active_orders=num_active_orders,
            weather_condition=weather_condition
        )
        
        # Oblicz cenę jako sumę wszystkich strategii
        total_price = 0.0
        
        for strategy in self.strategies:
            price_component = strategy.calculate(context)
            total_price += price_component
        
        # Oblicz surge multiplier (do statystyk)
        surge_multiplier = self._surge_strategy.get_surge_multiplier(context)
        
        return (total_price, surge_multiplier)
    
    def add_strategy(self, strategy: PricingStrategy):
        """
        Dodaje nową strategię cenową
        
        Args:
            strategy: Strategia do dodania
        """
        if strategy not in self.strategies:
            self.strategies.append(strategy)
    
    def remove_strategy(self, strategy: PricingStrategy):
        """
        Usuwa strategię cenową
        
        Args:
            strategy: Strategia do usunięcia
        """
        if strategy in self.strategies:
            self.strategies.remove(strategy)
