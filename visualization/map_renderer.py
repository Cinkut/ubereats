"""
Renderer mapy symulacji

Rysuje restauracje, klientów, kurierów i trasy
"""

import pygame
from typing import TYPE_CHECKING
from visualization.colors import *
import config

if TYPE_CHECKING:
    from simulation.simulation_engine import SimulationEngine


class MapRenderer:
    """
    Renderer mapy 2D
    
    Rysuje:
    - Tło (kolor zależny od pogody)
    - Restauracje (czerwone kwadraty)
    - Klientów z aktywnymi zamówieniami (żółte trójkąty)
    - Kurierów (kolorowe kółka zależnie od stanu)
    - Trasy kurierów (linie do celu)
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Inicjalizuje renderer mapy
        
        Args:
            x: Pozycja X
            y: Pozycja Y
            width: Szerokość mapy
            height: Wysokość mapy
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Skalowanie (mapa symulacji → mapa wyświetlana)
        self.scale_x = width / config.MAP_WIDTH
        self.scale_y = height / config.MAP_HEIGHT
    
    def render(self, screen: pygame.Surface, engine: 'SimulationEngine'):
        """
        Renderuje mapę
        
        Args:
            screen: Surface pygame
            engine: Silnik symulacji
        """
        # Tło (kolor zależny od pogody)
        weather = engine.weather_system.current_condition
        bg_color = weather.get_background_color()
        pygame.draw.rect(screen, bg_color, (self.x, self.y, self.width, self.height))
        
        # Ramka
        pygame.draw.rect(screen, COLOR_UI_BORDER, (self.x, self.y, self.width, self.height), 2)
        
        # Rysuj restauracje
        for restaurant in engine.restaurants:
            self._draw_restaurant(screen, restaurant)
        
        # Rysuj klientów z aktywnymi zamówieniami
        active_orders = engine.order_manager.get_active_orders()
        for order in active_orders:
            self._draw_customer(screen, order.customer)
        
        # Rysuj trasy kurierów
        for courier in engine.couriers:
            if courier.target_location:
                self._draw_courier_route(screen, courier)
        
        # Rysuj kurierów
        for courier in engine.couriers:
            self._draw_courier(screen, courier)
    
    def _draw_restaurant(self, screen: pygame.Surface, restaurant):
        """Rysuje restaurację jako czerwony kwadrat"""
        x, y = self._world_to_screen(restaurant.location.x, restaurant.location.y)
        size = config.RESTAURANT_SIZE
        
        # Kwadrat
        pygame.draw.rect(
            screen,
            COLOR_RESTAURANT,
            (x - size//2, y - size//2, size, size)
        )
        
        # Ramka
        pygame.draw.rect(
            screen,
            COLOR_RESTAURANT_BORDER,
            (x - size//2, y - size//2, size, size),
            2
        )
    
    def _draw_customer(self, screen: pygame.Surface, customer):
        """Rysuje klienta jako żółty trójkąt (dom)"""
        x, y = self._world_to_screen(customer.location.x, customer.location.y)
        size = config.CUSTOMER_SIZE * 1.5  # Trochę większy dla lepszej widoczności
        
        # Trójkąt (strzałka w górę = dom/lokalizacja)
        points = [
            (x, y - size),           # Góra
            (x - size, y + size),    # Lewy dół
            (x + size, y + size)     # Prawy dół
        ]
        
        # Wypełniony trójkąt
        pygame.draw.polygon(screen, COLOR_CUSTOMER, points)
        
        # Ramka
        pygame.draw.polygon(screen, COLOR_CUSTOMER_BORDER, points, 2)
    
    def _draw_courier(self, screen: pygame.Surface, courier):
        """Rysuje kuriera - RÓŻNE KSZTAŁTY dla różnych typów"""
        x, y = self._world_to_screen(courier.location.x, courier.location.y)
        size = config.COURIER_SIZE
        
        # Kolor zależny od stanu (State Pattern!)
        color = courier._state.get_color() if courier._state else COLOR_COURIER_IDLE
        border_color = tuple(max(0, c - 50) for c in color)
        
        # RÓŻNE KSZTAŁTY dla różnych typów (Strategy Pattern visualization!)
        if courier.courier_type == "drone":
            # DRON = kółko (lata w powietrzu)
            pygame.draw.circle(screen, color, (x, y), size)
            pygame.draw.circle(screen, border_color, (x, y), size, 2)
        
        elif courier.courier_type == "biker":
            # ROWERZYSTA = kwadrat (jedzie po ulicach)
            pygame.draw.rect(screen, color, (x - size, y - size, size*2, size*2))
            pygame.draw.rect(screen, border_color, (x - size, y - size, size*2, size*2), 2)
        
        else:
            # Domyślnie kółko (dla bezpieczeństwa)
            pygame.draw.circle(screen, color, (x, y), size)
            pygame.draw.circle(screen, border_color, (x, y), size, 2)
    
    def _draw_courier_route(self, screen: pygame.Surface, courier):
        """Rysuje linię od kuriera do celu"""
        if not courier.target_location:
            return
        
        # Pozycje
        x1, y1 = self._world_to_screen(courier.location.x, courier.location.y)
        x2, y2 = self._world_to_screen(courier.target_location.x, courier.target_location.y)
        
        # Kolor linii zależny od stanu
        state_name = courier.state_name
        if "ToRestaurant" in state_name:
            color = COLOR_ROUTE_TO_RESTAURANT
        elif "ToCustomer" in state_name:
            color = COLOR_ROUTE_TO_CUSTOMER
        else:
            return  # Nie rysuj dla innych stanów
        
        # Linia
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 1)
    
    def _world_to_screen(self, world_x: float, world_y: float) -> tuple:
        """
        Konwertuje współrzędne świata do współrzędnych ekranu
        
        Args:
            world_x: Współrzędna X w świecie
            world_y: Współrzędna Y w świecie
            
        Returns:
            tuple: (screen_x, screen_y)
        """
        screen_x = int(self.x + world_x * self.scale_x)
        screen_y = int(self.y + world_y * self.scale_y)
        return (screen_x, screen_y)
