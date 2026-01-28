"""
Model restauracji

Reprezentuje restaurację w systemie dostaw.
"""

from models.location import Location


class Restaurant:
    """
    Reprezentuje restaurację z której można zamawiać jedzenie
    
    Zasady SOLID:
    - Single Responsibility: tylko reprezentacja restauracji
    """
    
    _id_counter = 0  # Statyczny licznik ID
    
    def __init__(self, name: str, location: Location):
        """
        Inicjalizuje restaurację
        
        Args:
            name: Nazwa restauracji
            location: Lokalizacja na mapie
        """
        Restaurant._id_counter += 1
        self.id = Restaurant._id_counter
        
        self.name = name
        self.location = location
        
        # Statystyki
        self.total_orders = 0
        self.completed_orders = 0
    
    def register_order(self):
        """Rejestruje nowe zamówienie"""
        self.total_orders += 1
    
    def complete_order(self):
        """Rejestruje zakończone zamówienie"""
        self.completed_orders += 1
    
    @property
    def completion_rate(self) -> float:
        """
        Procent zakończonych zamówień
        
        Returns:
            float: Procent (0-100)
        """
        if self.total_orders > 0:
            return (self.completed_orders / self.total_orders) * 100
        return 0.0
    
    def __repr__(self) -> str:
        return f"Restaurant(id={self.id}, name='{self.name}', location={self.location})"
    
    def __str__(self) -> str:
        return f"{self.name} @ ({self.location.x:.0f}, {self.location.y:.0f})"
