"""
Wzorzec State - abstrakcyjna klasa bazowa dla stanów kuriera

Demonstracja State Pattern i zasady Open/Closed Principle
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.courier import Courier


class CourierState(ABC):
    """
    Abstrakcyjna klasa bazowa dla stanów kuriera
    
    Wzorce projektowe:
    - State Pattern: definicja interfejsu dla wszystkich stanów
    
    Zasady SOLID:
    - Open/Closed: nowe stany bez modyfikacji tej klasy
    - Liskov Substitution: wszystkie stany są wymienne
    - Interface Segregation: minimalny interfejs
    """
    
    @abstractmethod
    def on_enter(self, courier: 'Courier'):
        """
        Wywoływane gdy kurier wchodzi w ten stan
        
        Args:
            courier: Kurier zmieniający stan
        """
        pass
    
    @abstractmethod
    def update(self, courier: 'Courier', weather_condition):
        """
        Aktualizuje stan kuriera w każdym kroku symulacji
        
        Args:
            courier: Kurier do aktualizacji
            weather_condition: Aktualny warunek pogodowy
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Czy kurier w tym stanie jest dostępny do przypisania zamówienia
        
        Returns:
            bool: True jeśli dostępny
        """
        pass
    
    @abstractmethod
    def get_color(self) -> tuple:
        """
        Zwraca kolor reprezentujący ten stan (do wizualizacji)
        
        Returns:
            tuple: Kolor RGB
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
