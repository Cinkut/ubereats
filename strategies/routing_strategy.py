"""
Wzorzec Strategy - abstrakcyjna klasa bazowa dla strategii routingu

Demonstracja Strategy Pattern dla wyznaczania tras
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.location import Location


class RoutingStrategy(ABC):
    """
    Abstrakcyjna klasa bazowa dla strategii routingu
    
    Wzorce projektowe:
    - Strategy Pattern: różne algorytmy wyznaczania tras
    
    Zasady SOLID:
    - Open/Closed: nowe strategie bez modyfikacji tej klasy
    - Liskov Substitution: wszystkie strategie są wymienne
    """
    
    @abstractmethod
    def calculate_distance(self, start: 'Location', end: 'Location') -> float:
        """
        Oblicza dystans między dwoma punktami
        
        Args:
            start: Punkt startowy
            end: Punkt końcowy
            
        Returns:
            float: Dystans
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Nazwa strategii routingu
        
        Returns:
            str: Nazwa
        """
        pass
    
    @abstractmethod
    def move_towards(self, current: 'Location', target: 'Location', distance: float) -> 'Location':
        """
        Przesuwa kuriera w kierunku celu zgodnie ze strategią routingu
        
        NOWA METODA - prawdziwy Strategy Pattern dla ruchu!
        
        Args:
            current: Obecna lokalizacja
            target: Cel
            distance: Dystans do przesunięcia
            
        Returns:
            Location: Nowa lokalizacja
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
