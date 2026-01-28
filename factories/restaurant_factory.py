"""
Factory: Tworzy restauracje

Wzorzec Factory Method
"""

import random
from models.restaurant import Restaurant
from models.location import Location
import config


class RestaurantFactory:
    """
    Fabryka restauracji
    
    Wzorce projektowe:
    - Factory Pattern: centralizacja tworzenia restauracji
    
    Zasady SOLID:
    - Single Responsibility: tylko tworzenie restauracji
    """
    
    # Pula nazw restauracji
    RESTAURANT_NAMES = [
        "Pizza Napoli", "Burger King", "KFC", "McDonald's", "Subway",
        "Sushi Bar", "Thai Express", "India Gate", "Taco Bell", "Domino's Pizza",
        "Pho Vietnam", "Greek Taverna", "Italian Bistro", "French Cuisine", "Spanish Tapas",
        "Chinese Dragon", "Japanese Garden", "Korean BBQ", "Mexican Cantina", "Turkish Kebab",
        "American Diner", "English Pub", "German Brathouse", "Polish Pierogi", "Russian Café"
    ]
    
    _name_index = 0
    
    @staticmethod
    def create(location: Location = None, name: str = None) -> Restaurant:
        """
        Tworzy restaurację
        
        Args:
            location: Lokalizacja restauracji (None = losowa)
            name: Nazwa restauracji (None = generowana)
            
        Returns:
            Restaurant: Nowa restauracja
        """
        # Generuj domyślne wartości
        if location is None:
            location = RestaurantFactory._random_location()
        
        if name is None:
            name = RestaurantFactory._generate_name()
        
        return Restaurant(name, location)
    
    @staticmethod
    def create_batch(count: int) -> list:
        """
        Tworzy wiele restauracji naraz
        
        Args:
            count: Liczba restauracji do utworzenia
            
        Returns:
            list: Lista restauracji
        """
        restaurants = []
        
        for _ in range(count):
            restaurant = RestaurantFactory.create()
            restaurants.append(restaurant)
        
        return restaurants
    
    @staticmethod
    def _random_location() -> Location:
        """
        Generuje losową lokalizację dla restauracji
        
        Restauracje są rozmieszczone równomiernie na mapie
        
        Returns:
            Location: Losowa lokalizacja
        """
        # Dodaj margines od krawędzi
        margin = 100
        x = random.uniform(margin, config.MAP_WIDTH - margin)
        y = random.uniform(margin, config.MAP_HEIGHT - margin)
        return Location(x, y)
    
    @staticmethod
    def _generate_name() -> str:
        """
        Generuje nazwę restauracji z puli
        
        Returns:
            str: Nazwa restauracji
        """
        name = RestaurantFactory.RESTAURANT_NAMES[
            RestaurantFactory._name_index % len(RestaurantFactory.RESTAURANT_NAMES)
        ]
        RestaurantFactory._name_index += 1
        return name
