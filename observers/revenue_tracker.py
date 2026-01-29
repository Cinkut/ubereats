"""
Observer: Śledzi przychody i metryki finansowe
"""

from observers.observer import Observer
from typing import Dict, Any, List


class RevenueTracker(Observer):
    """
    Obserwator śledzący przychody i metryki finansowe
    
    Zbiera:
    - Całkowity przychód
    - Średnia cena zamówienia
    - Surge multiplier (średni, max)
    - Dystrybucja przychodów per kurier
    
    Zasady SOLID:
    - Single Responsibility: tylko śledzenie przychodów
    """
    
    def __init__(self):
        """Inicjalizuje tracker"""
        self.total_revenue = 0.0
        self.order_prices: List[float] = []
        self.surge_multipliers: List[float] = []
        
        # Przychody per kurier
        self.courier_earnings: Dict[str, float] = {}
        
        # Liczniki per warunek pogodowy
        self.revenue_per_weather: Dict[str, float] = {}
    
    def update(self, event: Dict[str, Any]):
        """
        Aktualizuje statystyki przychodów
        
        Args:
            event: Informacje o zdarzeniu
        """
        event_type = event.get('type')
        
        if event_type == 'order_created':
            self._handle_order_created(event)
        
        elif event_type == 'order_delivered':
            self._handle_order_delivered(event)
        
        elif event_type == 'surge_pricing':
            self._handle_surge_pricing(event)
    
    def _handle_order_created(self, event: Dict[str, Any]):
        """Obsługuje utworzenie zamówienia"""
        price = event.get('price', 0.0)
        surge = event.get('surge_multiplier', 1.0)
        weather = event.get('weather', 'unknown')
        
        self.order_prices.append(price)
        self.surge_multipliers.append(surge)  # NOWE - zapisz surge!
        
        # Zapisz przychód per warunek pogodowy
        self.revenue_per_weather[weather] = \
            self.revenue_per_weather.get(weather, 0.0) + price
    
    def _handle_order_delivered(self, event: Dict[str, Any]):
        """Obsługuje dostarczenie zamówienia"""
        earnings = event.get('earnings', 0.0)
        # Pobieramy price (jeśli dostępne, w starszej wersji to było to samo co earnings)
        price = event.get('price', earnings)
        courier_name = event.get('courier_name', 'Unknown')
        
        # Dodaj do całkowitego przychodu (pełna kwota)
        self.total_revenue += price
        
        # Zapisz zarobek kuriera (tylko prowizja)
        self.courier_earnings[courier_name] = \
            self.courier_earnings.get(courier_name, 0.0) + earnings
    
    def _handle_surge_pricing(self, event: Dict[str, Any]):
        """Obsługuje informację o surge pricingu"""
        multiplier = event.get('multiplier', 1.0)
        self.surge_multipliers.append(multiplier)
    
    def get_average_price(self) -> float:
        """
        Oblicza średnią cenę zamówienia
        
        Returns:
            float: Średnia cena
        """
        if not self.order_prices:
            return 0.0
        
        return sum(self.order_prices) / len(self.order_prices)
    
    def get_average_surge(self) -> float:
        """
        Oblicza średni surge multiplier
        
        Returns:
            float: Średni surge
        """
        if not self.surge_multipliers:
            return 1.0
        
        return sum(self.surge_multipliers) / len(self.surge_multipliers)
    
    def get_max_surge(self) -> float:
        """
        Zwraca maksymalny surge multiplier
        
        Returns:
            float: Max surge
        """
        if not self.surge_multipliers:
            return 1.0
        
        return max(self.surge_multipliers)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Zwraca statystyki przychodów
        
        Returns:
            dict: Słownik ze statystykami
        """
        return {
            'total_revenue': self.total_revenue,
            'average_price': self.get_average_price(),
            'average_surge': self.get_average_surge(),
            'max_surge': self.get_max_surge(),
            'courier_earnings': self.courier_earnings,
            'revenue_per_weather': self.revenue_per_weather
        }
