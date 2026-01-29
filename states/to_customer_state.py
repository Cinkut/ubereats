"""
Stan: Kurier dostarcza zamówienie do klienta
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

def get_idle_state():
    from states.idle_state import IdleState
    return IdleState()


class ToCustomerState(CourierState):
    """
    Stan kuriera: Dostarcza zamówienie do klienta
    
    W tym stanie kurier:
    - Porusza się w kierunku klienta
    - Jest narażony na wypadek (zależnie od pogody)
    - Przechodzi do IdleState gdy dostarczy zamówienie
    - Przechodzi do AccidentState gdy ma wypadek
    """
    
    def on_enter(self, courier: 'Courier'):
        """
        Wejście w stan dostawy do klienta
        
        Args:
            courier: Kurier wchodzący w stan
        """
        if courier.current_order:
            courier.target_location = courier.current_order.delivery_location
    
    def update(self, courier: 'Courier', weather_condition):
        """
        Aktualizacja kuriera dostarczającego zamówienie
        
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
        
        # Poruszaj się w kierunku klienta
        courier.move_towards_target(speed)
        
        # Sprawdź czy dotarł do klienta
        if courier.has_reached_target():
            # Dostarcz zamówienie
            if courier.current_order:
                courier.current_order.mark_delivered()
                
                # Zarobek = 40% ceny zamówienia (reszta dla platformy)
                earnings = courier.current_order.price * 0.40
                courier.complete_delivery(earnings)
            
            # Wróć do stanu wolnego
            courier.set_state(get_idle_state())
    
    def is_available(self) -> bool:
        """
        Kurier w trasie nie jest dostępny
        
        Returns:
            bool: False
        """
        return False
    
    def get_color(self) -> tuple:
        """
        Kolor pomarańczowy dla dostawy do klienta
        
        Returns:
            tuple: RGB pomarańczowy
        """
        return config.COLOR_COURIER_TO_CUSTOMER
    
    def __repr__(self) -> str:
        return "ToCustomerState"
