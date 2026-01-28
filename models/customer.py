"""
Model klienta

Reprezentuje klienta zamawiającego jedzenie.
"""

from models.location import Location


class Customer:
    """
    Reprezentuje klienta zamawiającego jedzenie
    
    Zasady SOLID:
    - Single Responsibility: tylko reprezentacja klienta
    """
    
    _id_counter = 0  # Statyczny licznik ID
    
    def __init__(self, location: Location):
        """
        Inicjalizuje klienta
        
        Args:
            location: Lokalizacja dostawy
        """
        Customer._id_counter += 1
        self.id = Customer._id_counter
        
        self.location = location
        
        # Statystyki
        self.total_orders = 0
        self.completed_orders = 0
    
    def register_order(self):
        """Rejestruje nowe zamówienie klienta"""
        self.total_orders += 1
    
    def complete_order(self):
        """Rejestruje zakończone zamówienie"""
        self.completed_orders += 1
    
    def __repr__(self) -> str:
        return f"Customer(id={self.id}, location={self.location})"
    
    def __str__(self) -> str:
        return f"Customer #{self.id}"
