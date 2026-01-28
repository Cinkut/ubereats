"""
Wzorzec Observer - Subject (Observable)

Klasa bazowa dla obiektów które powiadamiają obserwatorów
"""

from typing import List, Dict, Any
from observers.observer import Observer


class Subject:
    """
    Subject (Observable) w wzorcu Observer
    
    Zarządza listą obserwatorów i powiadamia ich o zdarzeniach
    
    Wzorce projektowe:
    - Observer Pattern: Subject powiadamiający obserwatorów
    
    Zasady SOLID:
    - Open/Closed: nowi obserwatorzy bez modyfikacji
    - Dependency Inversion: zależy od abstrakcji Observer
    """
    
    def __init__(self):
        """Inicjalizuje Subject"""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """
        Dodaje obserwatora
        
        Args:
            observer: Obserwator do dodania
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """
        Usuwa obserwatora
        
        Args:
            observer: Obserwator do usunięcia
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: Dict[str, Any]):
        """
        Powiadamia wszystkich obserwatorów o zdarzeniu
        
        Args:
            event: Słownik z informacjami o zdarzeniu
        """
        for observer in self._observers:
            observer.update(event)
    
    def get_observer_count(self) -> int:
        """
        Zwraca liczbę obserwatorów
        
        Returns:
            int: Liczba obserwatorów
        """
        return len(self._observers)
