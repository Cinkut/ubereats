"""
Manager zarządzający kurierami

Odpowiada za aktualizację stanów kurierów
"""

from typing import List
from models.courier import Courier
from observers.subject import Subject


class CourierManager(Subject):
    """
    Manager kurierów
    
    Odpowiada za:
    - Aktualizację wszystkich kurierów
    - Śledzenie dostępności kurierów
    - Powiadamianie o wypadkach
    
    Zasady SOLID:
    - Single Responsibility: tylko zarządzanie kurierami
    """
    
    def __init__(self, couriers: List[Courier]):
        """
        Inicjalizuje manager kurierów
        
        Args:
            couriers: Lista kurierów
        """
        super().__init__()
        self.couriers = couriers
    
    def update_all_couriers(self, weather_condition):
        """
        Aktualizuje wszystkich kurierów (delegacja do State Pattern)
        
        Args:
            weather_condition: Aktualny warunek pogodowy
        """
        for courier in self.couriers:
            # Zapisz liczbę wypadków przed aktualizacją
            accidents_before = courier.accidents
            
            # Aktualizuj kuriera (State Pattern)
            courier.update(weather_condition)
            
            # Sprawdź czy był wypadek
            if courier.accidents > accidents_before:
                self._notify_accident(courier, weather_condition)
    
    def _notify_accident(self, courier: Courier, weather_condition):
        """
        Powiadamia obserwatorów o wypadku
        
        Args:
            courier: Kurier który miał wypadek
            weather_condition: Warunek pogodowy
        """
        self.notify({
            'type': 'accident',
            'courier_id': courier.id,
            'courier_name': courier.name,
            'location_x': courier.location.x,
            'location_y': courier.location.y,
            'weather': weather_condition.get_display_name()
        })
    
    def get_available_couriers(self) -> List[Courier]:
        """
        Zwraca dostępnych kurierów (stan Idle)
        
        Returns:
            list: Lista dostępnych kurierów
        """
        return [courier for courier in self.couriers if courier.is_available]
    
    def get_active_couriers(self) -> List[Courier]:
        """
        Zwraca aktywnych kurierów (w trasie)
        
        Returns:
            list: Lista aktywnych kurierów
        """
        return [courier for courier in self.couriers if not courier.is_available]
    
    def assign_order_to_courier(self, courier: Courier, order):
        """
        Przypisuje zamówienie do kuriera
        
        Args:
            courier: Kurier
            order: Zamówienie
        """
        from states.to_restaurant_state import ToRestaurantState
        
        # Przypisz zamówienie
        courier.assign_order(order)
        order.assign_to_courier(courier.id)
        
        # Zmień stan kuriera na "jedzie do restauracji"
        courier.set_state(ToRestaurantState())
        
        # Powiadom obserwatorów
        self.notify({
            'type': 'order_assigned',
            'order_id': order.id,
            'courier_id': courier.id,
            'courier_name': courier.name
        })
