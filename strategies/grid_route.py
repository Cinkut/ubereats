"""
Strategia routingu: Siatka ulic (Manhattan distance)

Symuluje jazdę po siatce ulic - tylko poziomo i pionowo
"""

from strategies.routing_strategy import RoutingStrategy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.location import Location


class GridRoute(RoutingStrategy):
    """
    Strategia routingu: Manhattan Distance (siatka ulic)
    
    Oblicza odległość Manhattan między dwoma punktami:
    distance = |x2 - x1| + |y2 - y1|
    
    Zakłada:
    - Kurier porusza się po siatce ulic
    - Można jechać tylko poziomo lub pionowo
    - Bardziej realistyczne dla miejskiego środowiska
    
    Przykład:
    - Punkt A: (0, 0)
    - Punkt B: (3, 4)
    - Euclidean: 5.0
    - Manhattan: 7.0 (3 + 4)
    """
    
    def calculate_distance(self, start: 'Location', end: 'Location') -> float:
        """
        Oblicza odległość Manhattan
        
        Args:
            start: Punkt startowy
            end: Punkt końcowy
            
        Returns:
            float: Odległość Manhattan w jednostkach mapy
        """
        return start.manhattan_distance_to(end)
    
    def get_name(self) -> str:
        return "Grid Route (Manhattan)"
    
    def move_towards(self, current: 'Location', target: 'Location', distance: float) -> 'Location':
        """
        Porusza się po gridzie ulic (najpierw X, potem Y)
        
        REALIZM: Rowerzyści nie mogą jechać przez budynki!
        Najpierw jedzie w poziomie (X), potem w pionie (Y)
        
        Args:
            current: Obecna lokalizacja
            target: Cel
            distance: Dystans do przesunięcia
            
        Returns:
            Location: Nowa lokalizacja
        """
        from models.location import Location
        
        dx = target.x - current.x
        dy = target.y - current.y
        
        remaining = distance
        new_x = current.x
        new_y = current.y
        
        # Najpierw jedź w poziomie (X)
        if abs(dx) > 0.1:
            move_x = min(remaining, abs(dx))
            new_x = current.x + (move_x if dx > 0 else -move_x)
            remaining -= move_x
        
        # Potem jedź w pionie (Y)
        if remaining > 0.1 and abs(dy) > 0.1:
            move_y = min(remaining, abs(dy))
            new_y = current.y + (move_y if dy > 0 else -move_y)
        
        return Location(new_x, new_y)
