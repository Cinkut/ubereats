"""
Stan: Kurier jedzie do restauracji po zamówienie
"""

import random
from states.courier_state import CourierState
from typing import TYPE_CHECKING
import config

if TYPE_CHECKING:
    from models.courier import Courier

# Circular import - importujemy w funkcji
def get_accident_state():
    from states.accident_state import AccidentState
    return AccidentState()

def get_waiting_state():
    from states.waiting_at_restaurant_state import WaitingAtRestaurantState
    return WaitingAtRestaurantState()


class ToRestaurantState(CourierState):
    """
    Stan kuriera: Jedzie do restauracji po zamówienie
    
    W tym stanie kurier:
    - Porusza się w kierunku restauracji
    - Jest narażony na wypadek (zależnie od pogody)
    - Przechodzi do ToCustomerState gdy dotrze do celu
    - Przechodzi do AccidentState gdy ma wypadek
    """
    
    def on_enter(self, courier: 'Courier'):
        """
        Wejście w stan jazdy do restauracji
        
        Args:
            courier: Kurier wchodzący w stan
        """
        if courier.current_order:
            courier.target_location = courier.current_order.pickup_location
    
    def update(self, courier: 'Courier', weather_condition):
        """
        Aktualizacja kuriera jadącego do restauracji
        
        Args:
            courier: Kurier
            weather_condition: Aktualny warunek pogodowy
        """
        courier.active_time += 1
        
        # Oblicz prędkość z modyfikatorem pogody
        speed = courier.base_speed * weather_condition.get_speed_multiplier()
        
        # Sprawdź ryzyko wypadku
        accident_prob = weather_condition.get_accident_probability()
        if random.random() < accident_prob:
            # Wypadek!
            courier.register_accident()
            courier.set_state(get_accident_state())
            
            # Anuluj zamówienie
            if courier.current_order:
                courier.current_order.cancel()
                courier.current_order = None
            return
        
        # Poruszaj się w kierunku restauracji
        courier.move_towards_target(speed)
        
        # Sprawdź czy dotarł do restauracji
        if courier.has_reached_target():
            # Dotarł! Teraz CZEKA na przygotowanie jedzenia
            # (nie odbiera od razu - realistyczna symulacja!)
            courier.set_state(get_waiting_state())
    
    def is_available(self) -> bool:
        """
        Kurier w trasie nie jest dostępny
        
        Returns:
            bool: False
        """
        return False
    
    def get_color(self) -> tuple:
        """
        Kolor niebieski dla jazdy do restauracji
        
        Returns:
            tuple: RGB niebieski
        """
        return config.COLOR_COURIER_TO_RESTAURANT
    
    def __repr__(self) -> str:
        return "ToRestaurantState"
