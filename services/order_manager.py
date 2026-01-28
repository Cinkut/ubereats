"""
Manager zarządzający zamówieniami

Odpowiada za tworzenie i śledzenie zamówień
"""

import random
from typing import List
from models.order import Order, OrderStatus
from models.restaurant import Restaurant
from models.customer import Customer
from factories.order_factory import OrderFactory
from services.pricing_engine import PricingEngine
from observers.subject import Subject
# DirectRoute nie jest już potrzebne - każdy kurier ma swoją strategię!
import config


class OrderManager(Subject):
    """
    Manager zamówień
    
    Odpowiada za:
    - Generowanie nowych zamówień
    - Śledzenie aktywnych zamówień
    - Powiadamianie obserwatorów o zdarzeniach
    
    Zasady SOLID:
    - Single Responsibility: tylko zarządzanie zamówieniami
    - Open/Closed: łatwo rozszerzyć o nowe typy zamówień
    """
    
    def __init__(
        self,
        restaurants: List[Restaurant],
        pricing_engine: PricingEngine
    ):
        """
        Inicjalizuje manager zamówień
        
        Args:
            restaurants: Lista restauracji
            pricing_engine: Silnik cenowy
        """
        super().__init__()
        
        self.restaurants = restaurants
        self.pricing_engine = pricing_engine
        
        # Lista wszystkich zamówień
        self.all_orders: List[Order] = []
        
        # Pula klientów (mogą zamawiać wielokrotnie)
        self.customer_pool: List[Customer] = []
    
    def update(self, step: int, weather_condition, num_available_couriers: int):
        """
        Aktualizuje manager (może wygenerować nowe zamówienie)
        
        Args:
            step: Numer kroku symulacji
            weather_condition: Aktualny warunek pogodowy
            num_available_couriers: Liczba dostępnych kurierów
        """
        # Losowo generuj nowe zamówienie
        if random.random() < config.ORDER_SPAWN_RATE:
            self._create_order(weather_condition, num_available_couriers)
    
    def _create_order(self, weather_condition, num_available_couriers: int):
        """
        Tworzy nowe zamówienie
        
        Args:
            weather_condition: Warunek pogodowy
            num_available_couriers: Liczba dostępnych kurierów
        """
        # Oblicz liczbę aktywnych zamówień
        num_active_orders = len(self.get_pending_orders())
        
        # Wybierz losową restaurację
        restaurant = random.choice(self.restaurants)
        
        # Utwórz lub wybierz klienta
        if self.customer_pool and random.random() < 0.7:
            customer = random.choice(self.customer_pool)
        else:
            from factories.order_factory import OrderFactory as OF
            customer_location = OF._random_customer_location()
            customer = Customer(customer_location)
            self.customer_pool.append(customer)
        
        # Oblicz dystans ŚREDNI (różni kurierzy = różne dystanse!)
        # Dla ceny używamy DirectRoute jako baseline
        from strategies.direct_route import DirectRoute
        baseline_strategy = DirectRoute()
        distance = baseline_strategy.calculate_distance(
            restaurant.location,
            customer.location
        )
        
        # Oblicz cenę
        price, surge_multiplier = self.pricing_engine.calculate_price(
            distance=distance,
            num_available_couriers=num_available_couriers,
            num_active_orders=num_active_orders,
            weather_condition=weather_condition
        )
        
        # Utwórz zamówienie
        order = OrderFactory.create(
            restaurant=restaurant,
            customer=customer,
            price=price,
            distance=distance,
            weather_condition_name=weather_condition.get_name(),
            surge_multiplier=surge_multiplier
        )
        
        self.all_orders.append(order)
        
        # Powiadom obserwatorów
        self.notify({
            'type': 'order_created',
            'order_id': order.id,
            'restaurant_name': restaurant.name,
            'price': price,
            'distance': distance,
            'weather': weather_condition.get_display_name(),
            'surge_multiplier': surge_multiplier
        })
    
    def get_pending_orders(self) -> List[Order]:
        """
        Zwraca zamówienia oczekujące na kuriera
        
        Returns:
            list: Lista zamówień pending
        """
        return [order for order in self.all_orders if order.status == OrderStatus.PENDING]
    
    def get_active_orders(self) -> List[Order]:
        """
        Zwraca aktywne zamówienia (assigned, picked_up)
        
        Returns:
            list: Lista aktywnych zamówień
        """
        return [order for order in self.all_orders 
                if order.status in [OrderStatus.ASSIGNED, OrderStatus.PICKED_UP]]
    
    def get_completed_orders(self) -> List[Order]:
        """
        Zwraca zakończone zamówienia (delivered, cancelled)
        
        Returns:
            list: Lista zakończonych zamówień
        """
        return [order for order in self.all_orders if order.is_completed]
    
    def get_total_orders(self) -> int:
        """Zwraca liczbę wszystkich zamówień"""
        return len(self.all_orders)
