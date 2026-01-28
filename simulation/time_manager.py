"""
Zarządzanie czasem symulacji

Opcjonalny moduł do zarządzania czasem i prędkością symulacji
"""

import time


class TimeManager:
    """
    Manager czasu symulacji
    
    Odpowiada za:
    - Kontrolę prędkości symulacji
    - Pauza/wznowienie
    - Śledzenie czasu rzeczywistego
    
    Zasady SOLID:
    - Single Responsibility: tylko zarządzanie czasem
    """
    
    def __init__(self, time_scale: float = 1.0, target_fps: int = 60):
        """
        Inicjalizuje manager czasu
        
        Args:
            time_scale: Przyspieszenie symulacji (1.0 = normalnie, 2.0 = 2x szybciej)
            target_fps: Docelowa liczba klatek na sekundę
        """
        self.time_scale = time_scale
        self.target_fps = target_fps
        self.target_frame_time = 1.0 / target_fps if target_fps > 0 else 0
        
        self.current_step = 0
        self.is_paused = False
        
        self.last_frame_time = time.time()
        self.delta_time = 0.0
    
    def update(self):
        """Aktualizuje licznik kroków"""
        if not self.is_paused:
            self.current_step += 1
    
    def tick(self):
        """
        Reguluje prędkość symulacji (frame limiting)
        
        Zwraca True jeśli należy kontynuować
        """
        current_time = time.time()
        self.delta_time = current_time - self.last_frame_time
        
        # Oblicz czas do następnej klatki
        adjusted_frame_time = self.target_frame_time / self.time_scale
        time_to_wait = adjusted_frame_time - self.delta_time
        
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        
        self.last_frame_time = time.time()
        
        return not self.is_paused
    
    def pause(self):
        """Pauzuje symulację"""
        self.is_paused = True
    
    def resume(self):
        """Wznawia symulację"""
        self.is_paused = False
    
    def toggle_pause(self):
        """Przełącza pauzę"""
        self.is_paused = not self.is_paused
    
    def set_time_scale(self, scale: float):
        """
        Ustawia przyspieszenie symulacji
        
        Args:
            scale: Przyspieszenie (1.0 = normalnie, 2.0 = 2x szybciej)
        """
        self.time_scale = max(0.1, min(scale, 10.0))  # Ogranicz do [0.1, 10.0]
    
    def get_fps(self) -> float:
        """
        Oblicza aktualne FPS
        
        Returns:
            float: FPS
        """
        if self.delta_time > 0:
            return 1.0 / self.delta_time
        return 0.0
