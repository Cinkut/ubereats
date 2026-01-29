"""
Panel statystyk (prawa strona ekranu)

Wyświetla kluczowe metryki symulacji
"""

import pygame
from typing import TYPE_CHECKING
from visualization.colors import *

if TYPE_CHECKING:
    from simulation.simulation_engine import SimulationEngine


class StatsPanel:
    """
    Panel statystyk
    
    Wyświetla:
    - Krok symulacji
    - Pogodę
    - Zamówienia
    - Kurierów
    - Przychody
    - Surge multiplier
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Inicjalizuje panel statystyk
        
        Args:
            x: Pozycja X
            y: Pozycja Y
            width: Szerokość panelu
            height: Wysokość panelu
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Fonty (zostaną zainicjalizowane w render)
        self.font_header = None
        self.font_normal = None
        self.font_small = None
    
    def render(self, screen: pygame.Surface, engine: 'SimulationEngine'):
        """
        Renderuje panel statystyk
        
        Args:
            screen: Surface pygame do rysowania
            engine: Silnik symulacji (źródło danych)
        """
        # Inicjalizuj fonty (jeśli nie zainicjalizowane)
        if self.font_header is None:
            self.font_header = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 20)
        
        # Tło panelu
        pygame.draw.rect(screen, COLOR_PANEL, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, COLOR_UI_BORDER, (self.x, self.y, self.width, self.height), 2)
        
        # Nagłówek
        header_text = self.font_header.render("STATISTICS", True, COLOR_TEXT)
        screen.blit(header_text, (self.x + 10, self.y + 10))
        
        y_offset = self.y + 50
        
        # Krok symulacji
        step_text = f"Step: {engine.current_step}"
        self._render_text(screen, step_text, self.x + 10, y_offset, self.font_normal, COLOR_TEXT)
        y_offset += 30
        
        # Pogoda
        weather = engine.weather_system.current_condition
        weather_text = f"Weather: {weather.get_display_name()}"
        self._render_text(screen, weather_text, self.x + 10, y_offset, self.font_normal, COLOR_TEXT)
        y_offset += 40
        
        # --- Zamówienia ---
        self._render_text(screen, "ORDERS", self.x + 10, y_offset, self.font_normal, COLOR_UI_HEADER)
        y_offset += 25
        
        order_stats = engine.order_tracker.get_stats()
        
        orders_text = [
            f"  Total: {order_stats['total_orders']}",
            f"  Delivered: {order_stats['delivered_orders']}",
            f"  Cancelled: {order_stats['cancelled_orders']}",
            f"  Active: {order_stats['active_orders']}",
            f"  Pending: {order_stats['pending_orders']}",
            f"  Avg time: {order_stats['average_delivery_time']:.1f}s"
        ]
        
        for text in orders_text:
            self._render_text(screen, text, self.x + 10, y_offset, self.font_small, COLOR_TEXT)
            y_offset += 20
        
        y_offset += 10
        
        # --- Kurierzy ---
        self._render_text(screen, "COURIERS", self.x + 10, y_offset, self.font_normal, COLOR_UI_HEADER)
        y_offset += 25
        
        available = len(engine.courier_manager.get_available_couriers())
        active = len(engine.courier_manager.get_active_couriers())
        total_accidents = sum(c.accidents for c in engine.couriers)
        
        courier_text = [
            f"  Available: {available}",
            f"  Active: {active}",
            f"  Accidents: {total_accidents}"
        ]
        
        for text in courier_text:
            self._render_text(screen, text, self.x + 10, y_offset, self.font_small, COLOR_TEXT)
            y_offset += 20
        
        y_offset += 10
        
        # --- Przychody ---
        self._render_text(screen, "REVENUE", self.x + 10, y_offset, self.font_normal, COLOR_UI_HEADER)
        y_offset += 25
        
        revenue_stats = engine.revenue_tracker.get_stats()
        
        revenue_text = [
            f"  Total: ${revenue_stats['total_revenue']:.2f}",
            f"  Avg price: ${revenue_stats['average_price']:.2f}",
            f"  Max surge: {revenue_stats['max_surge']:.2f}x"
        ]
        
        for text in revenue_text:
            color = COLOR_UI_WARNING if "surge" in text.lower() else COLOR_TEXT
            self._render_text(screen, text, self.x + 10, y_offset, self.font_small, color)
            y_offset += 20
        
        y_offset += 10
        
        # --- Kontrolki ---
        self._render_text(screen, "CONTROLS", self.x + 10, y_offset, self.font_normal, COLOR_UI_HEADER)
        y_offset += 25
        
        controls_text = [
            "  SPACE - Pause",
            "  ESC - Quit",
            "  UP/DOWN - Speed",
            "  W - Change weather"
        ]
        
        for text in controls_text:
            self._render_text(screen, text, self.x + 10, y_offset, self.font_small, (100, 100, 100))
            y_offset += 18
    
    def _render_text(
        self,
        screen: pygame.Surface,
        text: str,
        x: int,
        y: int,
        font: pygame.font.Font,
        color: tuple
    ):
        """Helper do renderowania tekstu"""
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
