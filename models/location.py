"""
Model lokalizacji (punkt na mapie)

Reprezentuje pozycję na dwuwymiarowej mapie symulacji.
"""

import math
from typing import Tuple


class Location:
    """
    Reprezentuje punkt na mapie 2D
    
    Zasady SOLID:
    - Single Responsibility: tylko reprezentacja lokalizacji i podstawowe operacje
    """
    
    def __init__(self, x: float, y: float):
        """
        Inicjalizuje lokalizację
        
        Args:
            x: Współrzędna X (0 do MAP_WIDTH)
            y: Współrzędna Y (0 do MAP_HEIGHT)
        """
        self.x = x
        self.y = y
    
    def distance_to(self, other: 'Location') -> float:
        """
        Oblicza odległość euklidesową do innej lokalizacji
        
        Args:
            other: Docelowa lokalizacja
            
        Returns:
            float: Odległość
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def manhattan_distance_to(self, other: 'Location') -> float:
        """
        Oblicza odległość Manhattan do innej lokalizacji
        
        Args:
            other: Docelowa lokalizacja
            
        Returns:
            float: Odległość Manhattan
        """
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def move_towards(self, target: 'Location', distance: float) -> 'Location':
        """
        Tworzy nową lokalizację przesuniętą w kierunku celu o zadany dystans
        
        Args:
            target: Cel ruchu
            distance: Dystans do przesunięcia
            
        Returns:
            Location: Nowa lokalizacja
        """
        current_distance = self.distance_to(target)
        
        # Jeśli jesteśmy wystarczająco blisko, zwróć cel
        if current_distance <= distance:
            return Location(target.x, target.y)
        
        # Oblicz wektor kierunku (znormalizowany)
        ratio = distance / current_distance
        new_x = self.x + (target.x - self.x) * ratio
        new_y = self.y + (target.y - self.y) * ratio
        
        return Location(new_x, new_y)
    
    def to_tuple(self) -> Tuple[float, float]:
        """
        Konwertuje lokalizację do tupli
        
        Returns:
            tuple: (x, y)
        """
        return (self.x, self.y)
    
    def __repr__(self) -> str:
        return f"Location({self.x:.1f}, {self.y:.1f})"
    
    def __eq__(self, other) -> bool:
        """Porównuje dwie lokalizacje"""
        if not isinstance(other, Location):
            return False
        return abs(self.x - other.x) < 0.01 and abs(self.y - other.y) < 0.01
    
    def __hash__(self):
        """Hash lokalizacji (dla użycia w słownikach/setach)"""
        return hash((round(self.x, 2), round(self.y, 2)))
