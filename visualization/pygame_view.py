"""
Główny widok Pygame

Integruje wszystkie komponenty wizualizacji
"""

import pygame
import sys
from typing import TYPE_CHECKING
from visualization.map_renderer import MapRenderer
from visualization.stats_panel import StatsPanel
from visualization.colors import *
import config

if TYPE_CHECKING:
    from simulation.simulation_engine import SimulationEngine


class PygameView:
    """
    Główny widok Pygame
    
    Odpowiada za:
    - Inicjalizację okna
    - Obsługę eventów (klawiatura, mysz)
    - Renderowanie wszystkich komponentów
    - Zamknięcie okna
    
    Zasady SOLID:
    - Single Responsibility: tylko wizualizacja
    """
    
    def __init__(self, engine: 'SimulationEngine'):
        """
        Inicjalizuje widok Pygame
        
        Args:
            engine: Silnik symulacji
        """
        self.engine = engine
        
        # Inicjalizacja pygame
        pygame.init()
        
        # Utwórz okno
        self.width = config.WINDOW_WIDTH
        self.height = config.WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Uber Eats Simulation")
        
        # Zegar (do kontroli FPS)
        self.clock = pygame.time.Clock()
        
        # Komponenty renderujące
        map_width = config.MAP_WIDTH if config.MAP_WIDTH < self.width - 400 else self.width - 400
        map_height = config.MAP_HEIGHT if config.MAP_HEIGHT < self.height - 100 else self.height - 100
        
        self.map_renderer = MapRenderer(
            x=config.MAP_OFFSET_X,
            y=config.MAP_OFFSET_Y,
            width=map_width,
            height=map_height
        )
        
        self.stats_panel = StatsPanel(
            x=map_width + config.MAP_OFFSET_X + 20,
            y=config.MAP_OFFSET_Y,
            width=config.STATS_PANEL_WIDTH,
            height=map_height
        )
        
        # Font dla nagłówka
        self.title_font = pygame.font.Font(None, 40)
    
    def handle_events(self) -> bool:
        """
        Obsługuje eventy pygame
        
        Returns:
            bool: False jeśli należy zamknąć okno
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC - wyjście
                    return False
                
                elif event.key == pygame.K_SPACE:
                    # SPACE - pauza
                    self.engine.time_manager.toggle_pause()
                
                elif event.key == pygame.K_UP:
                    # Strzałka w górę - przyspiesz
                    current_scale = self.engine.time_manager.time_scale
                    self.engine.time_manager.set_time_scale(current_scale * 1.5)
                    print(f"[View] Speed: {self.engine.time_manager.time_scale:.1f}x")
                
                elif event.key == pygame.K_DOWN:
                    # Strzałka w dół - zwolnij
                    current_scale = self.engine.time_manager.time_scale
                    self.engine.time_manager.set_time_scale(current_scale / 1.5)
                    print(f"[View] Speed: {self.engine.time_manager.time_scale:.1f}x")
                
                elif event.key == pygame.K_w:
                    # W - zmiana pogody (losowa)
                    import random
                    weathers = ['clear', 'rain', 'snow', 'frost', 'ice']
                    new_weather = random.choice(weathers)
                    self.engine.weather_system.set_weather(new_weather)
                    print(f"[View] Weather changed to: {new_weather}")
        
        return True
    
    def render(self):
        """Renderuje całą scenę"""
        # Wyczyść ekran
        self.screen.fill(COLOR_BACKGROUND)
        
        # Nagłówek
        self._render_header()
        
        # Mapa
        self.map_renderer.render(self.screen, self.engine)
        
        # Panel statystyk
        self.stats_panel.render(self.screen, self.engine)
        
        # Status (na dole)
        self._render_status()
        
        # Odśwież ekran
        pygame.display.flip()
        
        # Kontroluj FPS
        self.clock.tick(config.FPS)
    
    def _render_header(self):
        """Renderuje nagłówek (góra ekranu)"""
        title_text = self.title_font.render("Uber Eats Simulation", True, COLOR_TEXT)
        self.screen.blit(title_text, (20, 10))
        
        # Informacja o pauzie
        if self.engine.time_manager.is_paused:
            pause_font = pygame.font.Font(None, 36)
            pause_text = pause_font.render("⏸ PAUSED", True, COLOR_UI_WARNING)
            x = config.MAP_OFFSET_X + self.map_renderer.width // 2 - pause_text.get_width() // 2
            y = config.MAP_OFFSET_Y + self.map_renderer.height // 2 - pause_text.get_height() // 2
            
            # Półprzezroczyste tło
            s = pygame.Surface((pause_text.get_width() + 40, pause_text.get_height() + 20))
            s.set_alpha(200)
            s.fill((50, 50, 50))
            self.screen.blit(s, (x - 20, y - 10))
            
            # Tekst
            self.screen.blit(pause_text, (x, y))
    
    def _render_status(self):
        """Renderuje status na dole ekranu"""
        status_font = pygame.font.Font(None, 20)
        
        fps = self.engine.time_manager.get_fps()
        speed = self.engine.time_manager.time_scale
        
        status_text = f"FPS: {fps:.0f} | Speed: {speed:.1f}x | Step: {self.engine.current_step}"
        
        text_surface = status_font.render(status_text, True, (100, 100, 100))
        self.screen.blit(text_surface, (20, self.height - 30))
    
    def close(self):
        """Zamyka okno pygame"""
        pygame.quit()
