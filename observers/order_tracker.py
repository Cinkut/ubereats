"""
Observer: Śledzi zamówienia i ich statusy
"""

from observers.observer import Observer
from typing import Dict, Any, List


class OrderTracker(Observer):
    """
    Obserwator śledzący postęp zamówień
    
    Zbiera statystyki:
    - Liczba zamówień (total, delivered, cancelled)
    - Średni czas dostawy
    - Rozkład zamówień per restauracja
    
    Zasady SOLID:
    - Single Responsibility: tylko śledzenie zamówień
    """
    
    def __init__(self):
        """Inicjalizuje tracker"""
        self.total_orders = 0
        self.delivered_orders = 0
        self.cancelled_orders = 0
        self.pending_orders = 0
        
        # Lista czasów dostaw (w sekundach)
        self.delivery_times: List[float] = []
        
        # Statystyki per restauracja
        self.orders_per_restaurant: Dict[str, int] = {}
        
        # Aktualne zamówienia w systemie (order_id -> status)
        self.active_orders: Dict[int, str] = {}
    
    def update(self, event: Dict[str, Any]):
        """
        Aktualizuje statystyki na podstawie zdarzenia
        
        Args:
            event: Informacje o zdarzeniu
        """
        event_type = event.get('type')
        
        if event_type == 'order_created':
            self._handle_order_created(event)
        
        elif event_type == 'order_assigned':
            self._handle_order_assigned(event)
        
        elif event_type == 'order_delivered':
            self._handle_order_delivered(event)
        
        elif event_type == 'order_cancelled':
            self._handle_order_cancelled(event)
    
    def _handle_order_created(self, event: Dict[str, Any]):
        """Obsługuje utworzenie zamówienia"""
        self.total_orders += 1
        self.pending_orders += 1
        
        order_id = event.get('order_id')
        self.active_orders[order_id] = 'pending'
        
        # Statystyka per restauracja
        restaurant_name = event.get('restaurant_name', 'Unknown')
        self.orders_per_restaurant[restaurant_name] = \
            self.orders_per_restaurant.get(restaurant_name, 0) + 1
    
    def _handle_order_assigned(self, event: Dict[str, Any]):
        """Obsługuje przypisanie zamówienia"""
        order_id = event.get('order_id')
        if order_id in self.active_orders:
            self.active_orders[order_id] = 'assigned'
            self.pending_orders -= 1
    
    def _handle_order_delivered(self, event: Dict[str, Any]):
        """Obsługuje dostarczenie zamówienia"""
        self.delivered_orders += 1
        
        order_id = event.get('order_id')
        if order_id in self.active_orders:
            del self.active_orders[order_id]
        
        # Zapisz czas dostawy
        delivery_time = event.get('delivery_time', 0)
        self.delivery_times.append(delivery_time)
    
    def _handle_order_cancelled(self, event: Dict[str, Any]):
        """Obsługuje anulowanie zamówienia"""
        self.cancelled_orders += 1
        
        order_id = event.get('order_id')
        if order_id in self.active_orders:
            del self.active_orders[order_id]
    
    def get_average_delivery_time(self) -> float:
        """
        Oblicza średni czas dostawy
        
        Returns:
            float: Średni czas w sekundach
        """
        if not self.delivery_times:
            return 0.0
        
        return sum(self.delivery_times) / len(self.delivery_times)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Zwraca statystyki zamówień
        
        Returns:
            dict: Słownik ze statystykami
        """
        return {
            'total_orders': self.total_orders,
            'delivered_orders': self.delivered_orders,
            'cancelled_orders': self.cancelled_orders,
            'pending_orders': self.pending_orders,
            'active_orders': len(self.active_orders),
            'average_delivery_time': self.get_average_delivery_time(),
            'orders_per_restaurant': self.orders_per_restaurant,
            'completion_rate': (self.delivered_orders / self.total_orders * 100) 
                              if self.total_orders > 0 else 0.0
        }
