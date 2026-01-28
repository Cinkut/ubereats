"""
Stan: Kurier miał wypadek (tymczasowo nieaktywny)
"""

from states.courier_state import CourierState
from typing import TYPE_CHECKING
import config

if TYPE_CHECKING:
    from models.courier import Courier

# Circular import - importujemy w funkcji
def get_idle_state():
    from states.idle_state import IdleState
    return IdleState()


class AccidentState(CourierState):
    """
    Stan kuriera: Miał wypadek (unieruchomiony)
    
    W tym stanie kurier:
    - Jest unieruchomiony przez określony czas
    - Nie jest dostępny do przypisania zamówienia
    - Nie porusza się
    - Po czasie recovery wraca do stanu wolnego
    """
    
    def on_enter(self, courier: 'Courier'):
        """
        Wejście w stan wypadku
        
        Args:
            courier: Kurier wchodzący w stan
        """
        # Ustaw licznik odliczania do powrotu
        courier.accident_recovery_counter = config.ACCIDENT_RECOVERY_TIME
        
        # Usuń cel i zamówienie
        courier.target_location = None
        # current_order powinno być już anulowane przez poprzedni stan
    
    def update(self, courier: 'Courier', weather_condition):
        """
        Aktualizacja kuriera po wypadku
        
        Args:
            courier: Kurier
            weather_condition: Pogoda (nieistotna w tym stanie)
        """
        courier.accident_time += 1
        courier.accident_recovery_counter -= 1
        
        # Sprawdź czy kurier się zregenerował
        if courier.accident_recovery_counter <= 0:
            # Wróć do stanu wolnego
            courier.set_state(get_idle_state())
    
    def is_available(self) -> bool:
        """
        Kurier po wypadku nie jest dostępny
        
        Returns:
            bool: False
        """
        return False
    
    def get_color(self) -> tuple:
        """
        Kolor czerwony dla wypadku
        
        Returns:
            tuple: RGB czerwony
        """
        return config.COLOR_COURIER_ACCIDENT
    
    def __repr__(self) -> str:
        return "AccidentState"
