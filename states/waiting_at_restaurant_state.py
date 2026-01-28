"""
Stan: Kurier czeka w restauracji na przygotowanie jedzenia

NOWY STAN - zwiększa realizm symulacji!
"""

import random
from states.courier_state import CourierState
from typing import TYPE_CHECKING
import config

if TYPE_CHECKING:
    from models.courier import Courier

# Circular import - importujemy w funkcji
def get_to_customer_state():
    from states.to_customer_state import ToCustomerState
    return ToCustomerState()


class WaitingAtRestaurantState(CourierState):
    """
    Stan kuriera: Czeka w restauracji na przygotowanie jedzenia
    
    W tym stanie kurier:
    - Stoi w miejscu (nie porusza się)
    - Czeka określony czas (20-50 kroków)
    - NIE ma ryzyka wypadku (stoi w miejscu)
    - Przechodzi do ToCustomerState gdy jedzenie gotowe
    
    REALIZM: Dokładnie jak w prawdziwym Uber Eats - kurier przyjeżdża,
    czeka aż burger się usmaży, potem dopiero jedzie do klienta!
    """
    
    def __init__(self):
        """Inicjalizuje stan oczekiwania"""
        super().__init__()
        # Losowy czas przygotowania (różne restauracje = różny czas)
        self.preparation_time = random.randint(
            config.RESTAURANT_PREPARATION_TIME_MIN,
            config.RESTAURANT_PREPARATION_TIME_MAX
        )
        self.wait_counter = 0
    
    def on_enter(self, courier: 'Courier'):
        """
        Wejście w stan oczekiwania
        
        Args:
            courier: Kurier wchodzący w stan
        """
        # Kurier dotarł do restauracji - teraz czeka!
        self.wait_counter = 0
        
        # Cel osiągnięty - teraz czekamy na jedzenie
        # (target_location zostaje bez zmian - pokazuje restaurację)
    
    def update(self, courier: 'Courier', weather_condition):
        """
        Aktualizacja kuriera czekającego w restauracji
        
        Args:
            courier: Kurier
            weather_condition: Pogoda (nieistotna - kurier stoi)
        """
        # Zwiększ licznik czasu aktywnego (ale nie porusza się)
        courier.active_time += 1
        
        # Odliczaj czas oczekiwania
        self.wait_counter += 1
        
        # Sprawdź czy jedzenie jest gotowe
        if self.wait_counter >= self.preparation_time:
            # Jedzenie gotowe! Odbierz zamówienie i jedź do klienta
            if courier.current_order:
                courier.current_order.mark_picked_up()
                courier.target_location = courier.current_order.delivery_location
            
            # Zmień stan na dostawę do klienta
            courier.set_state(get_to_customer_state())
    
    def is_available(self) -> bool:
        """
        Kurier czekający nie jest dostępny do nowych zamówień
        
        Returns:
            bool: False
        """
        return False
    
    def get_color(self) -> tuple:
        """
        Kolor żółty dla czekającego kuriera
        
        Returns:
            tuple: RGB żółty
        """
        return (255, 200, 0)  # Żółty - czeka na jedzenie
    
    def __repr__(self) -> str:
        return f"WaitingAtRestaurantState(waited={self.wait_counter}/{self.preparation_time})"
