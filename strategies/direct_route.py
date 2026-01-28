"""
Strategia routingu: Prosta linia (odległość euklidesowa)

Najkrótsza możliwa trasa - linia prosta między punktami
"""

from strategies.routing_strategy import RoutingStrategy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.location import Location


class DirectRoute(RoutingStrategy):
    """
    Strategia routingu: Prosta linia (as the crow flies)
    
    Oblicza odległość euklidesową między dwoma punktami:
    distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    
    Zakłada:
    - Kurier może jechać w dowolnym kierunku
    - Brak przeszkód na mapie
    - Najkrótsza możliwa trasa
    """
    
    def calculate_distance(self, start: 'Location', end: 'Location') -> float:
        """
        Oblicza odległość euklidesową
        
        Args:
            start: Punkt startowy
            end: Punkt końcowy
            
        Returns:
            float: Odległość w jednostkach mapy
        """
        return start.distance_to(end)
    
    def get_name(self) -> str:
        return "Direct Route (Euclidean)"
    
    def move_towards(self, current: 'Location', target: 'Location', distance: float) -> 'Location':
        """
        Porusza się w linii prostej (jak dron w powietrzu)
        
        Args:
            current: Obecna lokalizacja
            target: Cel
            distance: Dystans do przesunięcia
            
        Returns:
            Location: Nowa lokalizacja
        """
        from models.location import Location
        
        current_distance = current.distance_to(target)
        
        # Jeśli jesteśmy blisko celu, wróć cel
        if current_distance <= distance:
            return Location(target.x, target.y)
        
        # Linia prosta - znormalizowany wektor kierunku
        ratio = distance / current_distance
        new_x = current.x + (target.x - current.x) * ratio
        new_y = current.y + (target.y - current.y) * ratio
        
        return Location(new_x, new_y)
