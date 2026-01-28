"""
Serwis dyspozytorski - przydziela zamówienia do kurierów

Implementuje algorytm matchingu zamówień z kurierami
"""

from typing import List, TYPE_CHECKING
from models.order import Order
from models.courier import Courier
from services.order_manager import OrderManager
from services.courier_manager import CourierManager

if TYPE_CHECKING:
    from weather.weather_condition import WeatherCondition


class DispatchService:
    """
    Serwis dyspozytorski
    
    Odpowiada za:
    - Przydzielanie zamówień do dostępnych kurierów
    - Optymalizację przydziału (najbliższy kurier)
    
    Zasady SOLID:
    - Single Responsibility: tylko przydzielanie zamówień
    - Dependency Inversion: zależy od abstrakcji (managerów)
    """
    
    def __init__(
        self,
        order_manager: OrderManager,
        courier_manager: CourierManager
    ):
        """
        Inicjalizuje serwis dyspozytorski
        
        Args:
            order_manager: Manager zamówień
            courier_manager: Manager kurierów
        """
        self.order_manager = order_manager
        self.courier_manager = courier_manager
        self.current_weather = None  # Aktualna pogoda (ustawiana przez engine)
    
    def assign_orders(self, weather_condition: 'WeatherCondition'):
        """
        Przydziela oczekujące zamówienia do dostępnych kurierów
        
        NOWE: Drony nie latają w deszczu i śniegu!
        
        Algorytm:
        1. Pobierz oczekujące zamówienia
        2. Pobierz dostępnych kurierów
        3. FILTRUJ dronów jeśli pada deszcz/śnieg
        4. Dla każdego zamówienia znajdź najbliższego kuriera
        5. Przypisz zamówienie
        
        Args:
            weather_condition: Aktualna pogoda
        """
        pending_orders = self.order_manager.get_pending_orders()
        available_couriers = self.courier_manager.get_available_couriers()
        
        # NOWE: Filtruj dronów w złej pogodzie
        available_couriers = self._filter_couriers_by_weather(available_couriers, weather_condition)
        
        # Dopóki są zamówienia i kurierzy
        while pending_orders and available_couriers:
            # Pobierz pierwsze zamówienie z kolejki
            order = pending_orders[0]
            
            # Znajdź najbliższego kuriera
            closest_courier = self._find_closest_courier(order, available_couriers)
            
            if closest_courier:
                # Przypisz zamówienie
                self.courier_manager.assign_order_to_courier(closest_courier, order)
                
                # Usuń z list
                pending_orders.remove(order)
                available_couriers.remove(closest_courier)
            else:
                break
    
    def _find_closest_courier(
        self,
        order: Order,
        available_couriers: List[Courier]
    ) -> Courier:
        """
        Znajduje najbliższego kuriera do restauracji zamówienia
        
        Args:
            order: Zamówienie
            available_couriers: Lista dostępnych kurierów
            
        Returns:
            Courier: Najbliższy kurier lub None
        """
        if not available_couriers:
            return None
        
        restaurant_location = order.pickup_location
        
        # Znajdź kuriera z minimalnym dystansem
        closest_courier = min(
            available_couriers,
            key=lambda c: c.location.distance_to(restaurant_location)
        )
        
        return closest_courier
    
    def _filter_couriers_by_weather(
        self,
        couriers: List[Courier],
        weather_condition: 'WeatherCondition'
    ) -> List[Courier]:
        """
        Filtruje kurierów na podstawie pogody
        
        REALIZM: Drony nie mogą latać w deszczu i śniegu!
        
        Args:
            couriers: Lista dostępnych kurierów
            weather_condition: Aktualna pogoda
            
        Returns:
            List[Courier]: Odfiltrowana lista kurierów
        """
        weather_name = weather_condition.get_display_name().lower()
        
        # Drony nie latają w deszczu i śniegu
        bad_weather_for_drones = ['deszcz', 'snieg']
        
        filtered = []
        grounded_drones = 0
        
        for courier in couriers:
            # Jeśli to dron i jest zła pogoda - pomiń
            if courier.courier_type == "drone" and any(bad in weather_name for bad in bad_weather_for_drones):
                grounded_drones += 1
                continue
            
            filtered.append(courier)
        
        # Informuj o uziemionych dronach (tylko raz na zmianę pogody)
        if grounded_drones > 0 and not hasattr(self, '_last_grounded_warning'):
            print(f"[Dispatch] UWAGA: {grounded_drones} dronow uziemionych z powodu pogody!")
            self._last_grounded_warning = weather_name
        elif grounded_drones == 0:
            # Reset warningów gdy pogoda się poprawi
            if hasattr(self, '_last_grounded_warning'):
                delattr(self, '_last_grounded_warning')
        
        return filtered
