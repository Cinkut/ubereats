"""
Abstrakcyjna klasa bazowa dla warunków pogodowych

Demonstracja wzorca Strategy i Open/Closed Principle
"""

from abc import ABC, abstractmethod


class WeatherCondition(ABC):
    """
    Abstrakcyjna klasa reprezentująca warunek pogodowy
    
    Wzorce projektowe:
    - Strategy Pattern: różne warunki pogodowe jako strategie
    
    Zasady SOLID:
    - Open/Closed: nowe warunki pogodowe bez modyfikacji tej klasy
    - Liskov Substitution: wszystkie warunki są wymienne
    - Interface Segregation: minimalny interfejs
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Nazwa warunku pogodowego
        
        Returns:
            str: Nazwa (np. "clear", "rain", "ice")
        """
        pass
    
    @abstractmethod
    def get_display_name(self) -> str:
        """
        Nazwa wyświetlana (z emoji)
        
        Returns:
            str: Nazwa do wyświetlenia (np. " Czyste niebo")
        """
        pass
    
    @abstractmethod
    def get_speed_multiplier(self) -> float:
        """
        Mnożnik prędkości kuriera
        
        Returns:
            float: Mnożnik (1.0 = normalna prędkość, 0.5 = 50% wolniej)
        """
        pass
    
    @abstractmethod
    def get_accident_probability(self) -> float:
        """
        Prawdopodobieństwo wypadku na krok symulacji
        
        Returns:
            float: Prawdopodobieństwo (0.0 - 1.0)
        """
        pass
    
    @abstractmethod
    def get_price_multiplier(self) -> float:
        """
        Mnożnik ceny dostawy
        
        Returns:
            float: Mnożnik (1.0 = normalna cena, 2.0 = 2x droższa)
        """
        pass
    
    @abstractmethod
    def get_background_color(self) -> tuple:
        """
        Kolor tła mapy dla tego warunku (do wizualizacji)
        
        Returns:
            tuple: RGB kolor
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
    
    def __str__(self) -> str:
        return self.get_display_name()
