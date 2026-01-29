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
            # Zapisz statystyki przed aktualizacją
            accidents_before = courier.accidents
            deliveries_before = courier.total_deliveries
            
            # Zapisz referencję do zamówienia (przed jego usunięciem w update)
            order_before = courier.current_order
            
            # Aktualizuj kuriera (State Pattern)
            courier.update(weather_condition)
            
            # Sprawdź czy był wypadek
            if courier.accidents > accidents_before:
                # Jeśli kurier miał zamówienie, zostało anulowane
                if order_before:
                    self._notify_order_cancelled(order_before.id, courier, weather_condition)
                self._notify_accident(courier, weather_condition)
            
            # Sprawdź czy była dostawa
            if courier.total_deliveries > deliveries_before:
                # Przekaż zakończone zamówienie do powiadomienia
                self._notify_delivery(courier, order_before)

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
    
    def _notify_order_cancelled(self, order_id: int, courier: Courier, weather_condition):
        """
        Powiadamia obserwatorów o anulowanym zamówieniu
        
        Args:
            order_id: ID anulowanego zamówienia
            courier: Kurier który miał wypadek
            weather_condition: Warunek pogodowy
        """
        self.notify({
            'type': 'order_cancelled',
            'order_id': order_id,
            'courier_id': courier.id,
            'courier_name': courier.name,
            'reason': f'Wypadek kuriera ({weather_condition.get_display_name()})'
        })
    
    def _notify_delivery(self, courier: Courier, order):
        """
        Powiadamia obserwatorów o dostawie
        
        Args:
            courier: Kurier który dostarczył zamówienie
            order: Zamówienie które zostało dostarczone
        """
        # Pobieramy dane z obiektu zamówienia (który wciąż istnieje w pamięci)
        delivery_time = order.delivery_time_seconds if order else 0.0
        order_id = order.id if order else None
        
        # Pełna cena zamówienia (przychód firmy)
        price = order.price if order else 0.0
        # Zarobek kuriera (40%)
        earnings = price * 0.40
        
        self.notify({
            'type': 'order_delivered',
            'order_id': order_id,
            'courier_id': courier.id,
            'courier_name': courier.name,
            'price': price,        # NOWE: Pełna cena
            'earnings': earnings,  # Zarobek kuriera
            'delivery_time': delivery_time
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
