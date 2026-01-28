"""
Factory: Tworzy zamówienia

Wzorzec Factory Method
"""

import random
from typing import List
from models.order import Order
from models.customer import Customer
from models.restaurant import Restaurant
from models.location import Location
import config


class OrderFactory:
    """
    Fabryka zamówień
    
    Wzorce projektowe:
    - Factory Pattern: centralizacja tworzenia zamówień
    
    Zasady SOLID:
    - Single Responsibility: tylko tworzenie zamówień
    """
    
    @staticmethod
    def create(
        restaurant: Restaurant,
        customer: Customer,
        price: float,
        distance: float,
        weather_condition_name: str,
        surge_multiplier: float = 1.0
    ) -> Order:
        """
        Tworzy zamówienie
        
        Args:
            restaurant: Restauracja źródłowa
            customer: Klient docelowy
            price: Cena dostawy
            distance: Dystans dostawy
            weather_condition_name: Nazwa warunku pogodowego
            surge_multiplier: Mnożnik surge pricing
            
        Returns:
            Order: Nowe zamówienie
        """
        return Order(
            restaurant=restaurant,
            customer=customer,
            price=price,
            distance=distance,
            weather_condition=weather_condition_name,
            surge_multiplier=surge_multiplier
        )
    
    @staticmethod
    def create_random(
        restaurants: List[Restaurant],
        customer_pool: List[Customer],
        price: float,
        weather_condition_name: str,
        surge_multiplier: float = 1.0
    ) -> Order:
        """
        Tworzy losowe zamówienie
        
        Args:
            restaurants: Lista dostępnych restauracji
            customer_pool: Pula klientów
            price: Cena dostawy
            weather_condition_name: Warunek pogodowy
            surge_multiplier: Mnożnik surge
            
        Returns:
            Order: Losowe zamówienie
        """
        # Losuj restaurację
        restaurant = random.choice(restaurants)
        
        # Losuj lub utwórz klienta
        if customer_pool and random.random() < 0.7:  # 70% szans na istniejącego klienta
            customer = random.choice(customer_pool)
        else:
            # Utwórz nowego klienta
            customer_location = OrderFactory._random_customer_location()
            customer = Customer(customer_location)
            customer_pool.append(customer)
        
        # Oblicz dystans
        distance = restaurant.location.distance_to(customer.location)
        
        return OrderFactory.create(
            restaurant=restaurant,
            customer=customer,
            price=price,
            distance=distance,
            weather_condition_name=weather_condition_name,
            surge_multiplier=surge_multiplier
        )
    
    @staticmethod
    def _random_customer_location() -> Location:
        """
        Generuje losową lokalizację klienta
        
        Returns:
            Location: Losowa lokalizacja
        """
        # Klienci mogą być wszędzie na mapie
        x = random.uniform(20, config.MAP_WIDTH - 20)
        y = random.uniform(20, config.MAP_HEIGHT - 20)
        return Location(x, y)
