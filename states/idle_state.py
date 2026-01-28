"""
Stan: Kurier wolny (oczekuje na zamówienie)
"""

from states.courier_state import CourierState
from typing import TYPE_CHECKING
import config

if TYPE_CHECKING:
    from models.courier import Courier


class IdleState(CourierState):
    """
    Stan kuriera: Wolny / Oczekuje na zamówienie
    
    W tym stanie kurier:
    - Jest dostępny do przypisania zamówienia
    - Nie porusza się
    - Nie ma ryzyka wypadku
    """
    
    def on_enter(self, courier: 'Courier'):
        """
        Wejście w stan wolny
        
        Args:
            courier: Kurier wchodzący w stan
        """
        courier.current_order = None
        courier.target_location = None
    
    def update(self, courier: 'Courier', weather_condition):
        """
        Aktualizacja kuriera w stanie wolnym
        
        Args:
            courier: Kurier
            weather_condition: Pogoda (nieistotna w tym stanie)
        """
        # Kurier stoi w miejscu, zwiększ czas bezczynności
        courier.idle_time += 1
    
    def is_available(self) -> bool:
        """
        Kurier wolny jest dostępny
        
        Returns:
            bool: True
        """
        return True
    
    def get_color(self) -> tuple:
        """
        Kolor zielony dla kuriera wolnego
        
        Returns:
            tuple: RGB zielony
        """
        return config.COLOR_COURIER_IDLE
    
    def __repr__(self) -> str:
        return "IdleState"
