"""
Model kuriera

Reprezentuje kuriera dostarczającego zamówienia.
Wykorzystuje wzorzec State do zarządzania stanami kuriera.
"""

from typing import Optional, TYPE_CHECKING
from models.location import Location

# Unikamy circular imports
if TYPE_CHECKING:
    from states.courier_state import CourierState
    from models.order import Order


class Courier:
    """
    Reprezentuje kuriera dostarczającego jedzenie
    
    Wzorce projektowe:
    - State Pattern: zmienia zachowanie w zależności od stanu
    
    Zasady SOLID:
    - Single Responsibility: reprezentacja kuriera + delegacja do stanów
    - Open/Closed: nowe stany bez modyfikacji tej klasy
    - Dependency Inversion: zależy od abstrakcji CourierState
    """
    
    _id_counter = 0  # Statyczny licznik ID
    
    def __init__(self, name: str, location: Location, base_speed: float, routing_strategy=None, courier_type: str = "drone"):
        """
        Inicjalizuje kuriera
        
        Args:
            name: Nazwa/imię kuriera
            location: Początkowa lokalizacja
            base_speed: Bazowa prędkość (jednostek/krok)
            routing_strategy: Strategia routingu (DirectRoute, GridRoute, etc.)
            courier_type: Typ kuriera ("drone", "biker", "car") dla wizualizacji
        """
        Courier._id_counter += 1
        self.id = Courier._id_counter
        
        self.name = name
        self.location = location
        self.base_speed = base_speed
        self.courier_type = courier_type  # NOWE - typ kuriera dla wizualizacji
        
        # Strategia routingu (Strategy Pattern!)
        self.routing_strategy = routing_strategy
        if self.routing_strategy is None:
            from strategies.direct_route import DirectRoute
            self.routing_strategy = DirectRoute()  # Domyślna
        
        # Stan (ustawiany przez Factory)
        self._state: Optional['CourierState'] = None
        
        # Aktualne zamówienie (jeśli przypisane)
        self.current_order: Optional['Order'] = None
        
        # Cel ruchu (zależny od stanu)
        self.target_location: Optional[Location] = None
        
        # Statystyki
        self.total_deliveries = 0
        self.total_earnings = 0.0
        self.total_distance_traveled = 0.0
        self.accidents = 0
        
        # Czas w różnych stanach (w krokach symulacji)
        self.idle_time = 0
        self.active_time = 0
        self.accident_time = 0
        
        # Licznik kroków od ostatniego wypadku (dla recovery)
        self.accident_recovery_counter = 0
    
    def set_state(self, state: 'CourierState'):
        """
        Ustawia nowy stan kuriera (State Pattern)
        
        Args:
            state: Nowy stan
        """
        self._state = state
        self._state.on_enter(self)
    
    def update(self, weather_condition):
        """
        Aktualizuje stan kuriera (delegacja do State)
        
        Args:
            weather_condition: Aktualny warunek pogodowy
        """
        if self._state:
            self._state.update(self, weather_condition)
    
    def assign_order(self, order: 'Order'):
        """
        Przypisuje zamówienie do kuriera
        
        Args:
            order: Zamówienie do dostarczenia
        """
        self.current_order = order
        self.target_location = order.pickup_location
    
    def complete_delivery(self, earnings: float):
        """
        Oznacza dostawę jako zakończoną
        
        Args:
            earnings: Zarobek z dostawy
        """
        self.total_deliveries += 1
        self.total_earnings += earnings
        self.current_order = None
        self.target_location = None
    
    def register_accident(self):
        """Rejestruje wypadek kuriera"""
        self.accidents += 1
    
    def move_towards_target(self, speed: float):
        """
        Przesuwa kuriera w kierunku celu UŻYWAJĄC STRATEGII ROUTINGU
        
        NOWE - prawdziwy Strategy Pattern dla ruchu!
        Każdy typ kuriera porusza się inaczej:
        - Dron: linia prosta (DirectRoute)
        - Rowerzysta: po gridzie ulic (GridRoute)
        - Samochód: autostrada (HighwayRoute)
        
        Args:
            speed: Prędkość ruchu (zmodyfikowana przez pogodę)
        """
        if self.target_location:
            distance_moved = speed
            old_location = self.location
            # NOWE - używamy routing_strategy do poruszania się!
            self.location = self.routing_strategy.move_towards(self.location, self.target_location, distance_moved)
            
            # Aktualizuj statystykę dystansu
            actual_distance = old_location.distance_to(self.location)
            self.total_distance_traveled += actual_distance
    
    def has_reached_target(self, threshold: float = 5.0) -> bool:
        """
        Sprawdza czy kurier dotarł do celu
        
        Args:
            threshold: Próg odległości uznawany za dotarcie
            
        Returns:
            bool: True jeśli dotarł
        """
        if self.target_location is None:
            return False
        
        return self.location.distance_to(self.target_location) < threshold
    
    @property
    def state_name(self) -> str:
        """
        Nazwa aktualnego stanu
        
        Returns:
            str: Nazwa stanu
        """
        if self._state:
            return self._state.__class__.__name__
        return "NoState"
    
    @property
    def is_available(self) -> bool:
        """
        Czy kurier jest dostępny do przypisania zamówienia
        
        Returns:
            bool: True jeśli dostępny
        """
        # Będzie implementowane przez stan
        if self._state:
            return self._state.is_available()
        return False
    
    @property
    def utilization_rate(self) -> float:
        """
        Procent czasu wykorzystania kuriera
        
        Returns:
            float: Procent (0-100)
        """
        total_time = self.idle_time + self.active_time + self.accident_time
        if total_time > 0:
            return (self.active_time / total_time) * 100
        return 0.0
    
    @property
    def average_earnings_per_delivery(self) -> float:
        """
        Średni zarobek na dostawę
        
        Returns:
            float: Średni zarobek
        """
        if self.total_deliveries > 0:
            return self.total_earnings / self.total_deliveries
        return 0.0
    
    def __repr__(self) -> str:
        return (f"Courier(id={self.id}, name='{self.name}', state={self.state_name}, "
                f"deliveries={self.total_deliveries})")
    
    def __str__(self) -> str:
        return f"{self.name} [{self.state_name}] @ ({self.location.x:.0f}, {self.location.y:.0f})"
