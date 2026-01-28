"""
Wzorzec Observer - abstrakcyjna klasa bazowa dla obserwatorów

Demonstracja Observer Pattern
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Observer(ABC):
    """
    Abstrakcyjna klasa bazowa dla obserwatorów
    
    Wzorce projektowe:
    - Observer Pattern: obserwator reagujący na zdarzenia
    
    Zasady SOLID:
    - Interface Segregation: minimalny interfejs (tylko update)
    - Dependency Inversion: komponenty zależą od tej abstrakcji
    """
    
    @abstractmethod
    def update(self, event: Dict[str, Any]):
        """
        Wywoływane gdy Subject powiadamia o zdarzeniu
        
        Args:
            event: Słownik z informacjami o zdarzeniu
                   Zawiera co najmniej klucz 'type' określający typ zdarzenia
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
