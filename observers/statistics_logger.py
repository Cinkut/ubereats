"""
Observer: Loguje statystyki symulacji do pliku
"""

from observers.observer import Observer
from typing import Dict, Any
from datetime import datetime
import os


class StatisticsLogger(Observer):
    """
    Obserwator logujący statystyki do pliku
    
    Loguje wszystkie kluczowe zdarzenia symulacji:
    - Nowe zamówienia
    - Dostawy
    - Wypadki
    - Zmiany pogody
    
    Zasady SOLID:
    - Single Responsibility: tylko logowanie statystyk
    """
    
    def __init__(self, log_file: str = "lab6/simulation.log"):
        """
        Inicjalizuje logger
        
        Args:
            log_file: Ścieżka do pliku logów
        """
        self.log_file = log_file
        
        # Utwórz katalog jeśli nie istnieje
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Wyczyść plik przy starcie
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== UBER EATS SIMULATION LOG ===\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"=" * 50 + "\n\n")
    
    def update(self, event: Dict[str, Any]):
        """
        Loguje zdarzenie do pliku
        
        Args:
            event: Informacje o zdarzeniu
        """
        event_type = event.get('type', 'unknown')
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        message = self._format_event(event_type, event, timestamp)
        
        if message:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + "\n")
    
    def _format_event(self, event_type: str, event: Dict[str, Any], timestamp: str) -> str:
        """
        Formatuje zdarzenie do czytelnego tekstu
        
        Args:
            event_type: Typ zdarzenia
            event: Dane zdarzenia
            timestamp: Znacznik czasu
            
        Returns:
            str: Sformatowana wiadomość
        """
        if event_type == 'order_created':
            return (f"[{timestamp}] ORDER CREATED: #{event.get('order_id')} | "
                   f"Restaurant: {event.get('restaurant_name')} | "
                   f"Price: ${event.get('price', 0):.2f} | "
                   f"Distance: {event.get('distance', 0):.1f} | "
                   f"Weather: {event.get('weather')}")
        
        elif event_type == 'order_assigned':
            return (f"[{timestamp}] ORDER ASSIGNED: #{event.get('order_id')} → "
                   f"Courier {event.get('courier_name')}")
        
        elif event_type == 'order_delivered':
            return (f"[{timestamp}] ORDER DELIVERED: #{event.get('order_id')} | "
                   f"Time: {event.get('delivery_time', 0):.1f}s | "
                   f"Courier: {event.get('courier_name')} | "
                   f"Earnings: ${event.get('earnings', 0):.2f}")
        
        elif event_type == 'accident':
            return (f"[{timestamp}] 🚨 ACCIDENT: Courier {event.get('courier_name')} | "
                   f"Weather: {event.get('weather')} | "
                   f"Location: ({event.get('location_x', 0):.0f}, {event.get('location_y', 0):.0f})")
        
        elif event_type == 'weather_change':
            return (f"[{timestamp}] ⛅ WEATHER CHANGE: {event.get('display_name')} | "
                   f"Step: {event.get('step')}")
        
        elif event_type == 'surge_pricing':
            return (f"[{timestamp}] 💰 SURGE PRICING: {event.get('multiplier', 1.0):.2f}x | "
                   f"Active orders: {event.get('active_orders')} | "
                   f"Available couriers: {event.get('available_couriers')}")
        
        return None
