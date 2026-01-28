"""
Model zamówienia

Reprezentuje zamówienie jedzenia od klienta.
"""

from datetime import datetime
from typing import Optional
from models.location import Location
from models.restaurant import Restaurant
from models.customer import Customer


class OrderStatus:
    """Enum statusów zamówienia"""
    PENDING = "pending"              # Czeka na kuriera
    ASSIGNED = "assigned"            # Przypisane do kuriera
    PICKED_UP = "picked_up"          # Kurier odebrał z restauracji
    DELIVERED = "delivered"          # Dostarczone
    CANCELLED = "cancelled"          # Anulowane (np. wypadek kuriera)


class Order:
    """
    Reprezentuje zamówienie jedzenia
    
    Zasady SOLID:
    - Single Responsibility: tylko reprezentacja zamówienia i jego statusu
    - Open/Closed: łatwo rozszerzyć o nowe statusy
    """
    
    _id_counter = 0  # Statyczny licznik ID
    
    def __init__(
        self, 
        restaurant: Restaurant,
        customer: Customer,
        price: float,
        distance: float,
        weather_condition: str,
        surge_multiplier: float = 1.0
    ):
        """
        Inicjalizuje zamówienie
        
        Args:
            restaurant: Restauracja źródłowa
            customer: Klient docelowy
            price: Cena dostawy
            distance: Dystans dostawy
            weather_condition: Warunek pogodowy
            surge_multiplier: Mnożnik surge pricing
        """
        Order._id_counter += 1
        self.id = Order._id_counter
        
        self.restaurant = restaurant
        self.customer = customer
        self.price = price
        self.distance = distance
        self.weather_condition = weather_condition
        self.surge_multiplier = surge_multiplier
        
        # Status
        self.status = OrderStatus.PENDING
        
        # Timestampy
        self.created_at = datetime.now()
        self.assigned_at: Optional[datetime] = None
        self.picked_up_at: Optional[datetime] = None
        self.delivered_at: Optional[datetime] = None
        
        # Kurier (przypisany później)
        self.courier_id: Optional[int] = None
        
        # Rejestruj w restauracji i u klienta
        restaurant.register_order()
        customer.register_order()
    
    def assign_to_courier(self, courier_id: int):
        """
        Przypisuje zamówienie do kuriera
        
        Args:
            courier_id: ID kuriera
        """
        self.status = OrderStatus.ASSIGNED
        self.courier_id = courier_id
        self.assigned_at = datetime.now()
    
    def mark_picked_up(self):
        """Oznacza zamówienie jako odebrane z restauracji"""
        self.status = OrderStatus.PICKED_UP
        self.picked_up_at = datetime.now()
    
    def mark_delivered(self):
        """Oznacza zamówienie jako dostarczone"""
        self.status = OrderStatus.DELIVERED
        self.delivered_at = datetime.now()
        
        # Aktualizuj statystyki
        self.restaurant.complete_order()
        self.customer.complete_order()
    
    def cancel(self):
        """Anuluje zamówienie (np. wypadek kuriera)"""
        self.status = OrderStatus.CANCELLED
    
    @property
    def pickup_location(self) -> Location:
        """Lokalizacja odbioru (restauracja)"""
        return self.restaurant.location
    
    @property
    def delivery_location(self) -> Location:
        """Lokalizacja dostawy (klient)"""
        return self.customer.location
    
    @property
    def is_completed(self) -> bool:
        """Czy zamówienie zostało zakończone"""
        return self.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]
    
    @property
    def delivery_time_seconds(self) -> float:
        """
        Czas dostawy w sekundach (od utworzenia do dostarczenia)
        
        Returns:
            float: Czas w sekundach lub 0 jeśli nie dostarczone
        """
        if self.delivered_at and self.created_at:
            return (self.delivered_at - self.created_at).total_seconds()
        return 0.0
    
    def __repr__(self) -> str:
        return (f"Order(id={self.id}, status={self.status}, "
                f"price=${self.price:.2f}, surge={self.surge_multiplier:.2f}x)")
    
    def __str__(self) -> str:
        return (f"Order #{self.id}: {self.restaurant.name} → "
                f"Customer #{self.customer.id} [${self.price:.2f}]")
