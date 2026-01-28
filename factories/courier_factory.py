"""
Factory: Tworzy kurierów z domyślną konfiguracją

Wzorzec Factory Method + Strategy Pattern!
Teraz tworzy 3 typy kurierów z różnymi strategiami routingu.
"""

import random
from models.courier import Courier
from models.location import Location
from states.idle_state import IdleState
from strategies.direct_route import DirectRoute
from strategies.grid_route import GridRoute

import config


class CourierFactory:
    """
    Fabryka kurierów
    
    Wzorce projektowe:
    - Factory Pattern: centralizacja tworzenia kurierów
    
    Zasady SOLID:
    - Single Responsibility: tylko tworzenie kurierów
    - Open/Closed: łatwo rozszerzyć o nowe typy kurierów
    """
    
    # Pula imion dla kurierów
    COURIER_NAMES = [
        "Adam", "Bartosz", "Cezary", "Damian", "Emil",
        "Filip", "Grzegorz", "Hubert", "Igor", "Jakub",
        "Kamil", "Łukasz", "Mateusz", "Norbert", "Oskar",
        "Paweł", "Robert", "Sebastian", "Tomasz", "Wojciech",
        "Anna", "Barbara", "Celina", "Diana", "Ewa",
        "Franciszka", "Gabriela", "Helena", "Iwona", "Julia"
    ]
    
    _name_index = 0
    
    @staticmethod
    def create(location: Location = None, name: str = None, speed: float = None, routing_strategy=None) -> Courier:
        """
        Tworzy kuriera z domyślną konfiguracją
        
        Args:
            location: Początkowa lokalizacja (None = losowa)
            name: Imię kuriera (None = generowane)
            speed: Bazowa prędkość (None = z config)
            
        Returns:
            Courier: Nowy kurier
        """
        # Generuj domyślne wartości jeśli nie podane
        if location is None:
            location = CourierFactory._random_location()
        
        if name is None:
            name = CourierFactory._generate_name()
        
        if speed is None:
            speed = config.COURIER_BASE_SPEED
        
        # Domyślna strategia jeśli nie podana
        if routing_strategy is None:
            routing_strategy = DirectRoute()
        
        # Utwórz kuriera
        courier = Courier(name, location, speed, routing_strategy)
        
        # Ustaw domyślny stan (Idle)
        courier.set_state(IdleState())
        
        return courier
    
    @staticmethod
    def create_batch(count: int) -> list:
        """
        Tworzy wiele kurierów naraz
        
        NOWE: Teraz tworzy 3 typy kurierów!
        - 40% Drony (DirectRoute) - najszybsze, linia prosta
        - 40% Rowerzyści (GridRoute) - ulice, wolniejsze
        - 20% Auta (HighwayRoute) - autostrady, średnie
        
        Args:
            count: Liczba kurierów do utworzenia
            
        Returns:
            list: Lista kurierów z różnymi strategiami
        """
        couriers = []
        
        # Statystyki dla użytkownika
        drones_count = 0
        bikers_count = 0
        
        for i in range(count):
            # Wybierz typ kuriera (50% / 50%)
            if random.random() < 0.5:
                # Dron - leci prosto (50%)
                courier = CourierFactory.create_drone()
                drones_count += 1
            else:
                # Rowerzysta - ulice (50%)
                courier = CourierFactory.create_biker()
                bikers_count += 1
            
            couriers.append(courier)
        
        # Wyświetl statystyki
        print(f"  • Drony: {drones_count}, Rowerzyści: {bikers_count}")
        
        return couriers
    
    @staticmethod
    def create_drone() -> Courier:
        """Tworzy drona - najszybszy, linia prosta"""
        location = CourierFactory._random_location()
        name = CourierFactory._generate_name()
        courier = Courier(name + " Dron", location, 15.0, DirectRoute(), courier_type="drone")
        courier.set_state(IdleState())
        return courier
    
    @staticmethod
    def create_biker() -> Courier:
        """Tworzy rowerzystę - ulice w siatce"""
        location = CourierFactory._random_location()
        name = CourierFactory._generate_name()
        courier = Courier(name + " Rower", location, 8.0, GridRoute(), courier_type="biker")
        courier.set_state(IdleState())
        return courier
    
    
    @staticmethod
    def _random_location() -> Location:
        """
        Generuje losową lokalizację na mapie
        
        Returns:
            Location: Losowa lokalizacja
        """
        x = random.uniform(50, config.MAP_WIDTH - 50)
        y = random.uniform(50, config.MAP_HEIGHT - 50)
        return Location(x, y)
    
    @staticmethod
    def _generate_name() -> str:
        """
        Generuje imię kuriera z puli
        
        Returns:
            str: Imię kuriera
        """
        name = CourierFactory.COURIER_NAMES[CourierFactory._name_index % len(CourierFactory.COURIER_NAMES)]
        CourierFactory._name_index += 1
        return name
