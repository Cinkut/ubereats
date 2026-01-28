"""
System zarządzający pogodą w symulacji

Implementuje wzorzec Observer - powiadamia o zmianach pogody
"""

import random
from typing import List
import config

from weather.clear_weather import ClearWeather
from weather.rain_weather import RainWeather
from weather.snow_weather import SnowWeather
from weather.frost_weather import FrostWeather
from weather.ice_weather import IceWeather
from weather.weather_condition import WeatherCondition


class WeatherSystem:
    """
    System zarządzający warunkami pogodowymi
    
    Wzorce projektowe:
    - Subject (Observable) dla Observer Pattern
    
    Zasady SOLID:
    - Single Responsibility: tylko zarządzanie pogodą
    - Open/Closed: łatwo dodać nowe warunki pogodowe
    - Dependency Inversion: zwraca abstrakcję WeatherCondition
    """
    
    def __init__(self):
        """Inicjalizuje system pogodowy"""
        # Mapa wszystkich możliwych warunków
        self._conditions = {
            'clear': ClearWeather(),
            'rain': RainWeather(),
            'snow': SnowWeather(),
            'frost': FrostWeather(),
            'ice': IceWeather()
        }
        
        # Aktualny warunek
        self.current_condition: WeatherCondition = self._conditions['clear']
        
        # Licznik do zmiany pogody
        self._change_timer = self._get_random_change_interval()
        
        # Observery (będą dodane później)
        self._observers: List = []
        
        # Statystyki
        self.weather_history = []
        self.current_step = 0
    
    def set_weather(self, weather_name: str):
        """
        Ustawia konkretny warunek pogodowy (do testów)
        
        Args:
            weather_name: Nazwa warunku ('clear', 'rain', 'snow', 'frost', 'ice')
        """
        if weather_name in self._conditions:
            old_condition = self.current_condition
            self.current_condition = self._conditions[weather_name]
            
            if old_condition != self.current_condition:
                self._log_weather_change()
                self._notify_observers()
    
    def update(self, step: int):
        """
        Aktualizuje system pogodowy (wywoływane co krok symulacji)
        
        Args:
            step: Numer kroku symulacji
        """
        self.current_step = step
        self._change_timer -= 1
        
        # Sprawdź czy czas na zmianę pogody
        if self._change_timer <= 0:
            self._change_weather()
            self._change_timer = self._get_random_change_interval()
    
    def _change_weather(self):
        """Losowo zmienia pogodę na podstawie prawdopodobieństw"""
        # Losuj nowy warunek
        weather_names = list(config.WEATHER_PROBABILITIES.keys())
        probabilities = list(config.WEATHER_PROBABILITIES.values())
        
        new_weather_name = random.choices(weather_names, weights=probabilities)[0]
        
        # Nie zmieniaj jeśli to ten sam warunek
        if self._conditions[new_weather_name] == self.current_condition:
            return
        
        # Zmień pogodę
        old_condition = self.current_condition
        self.current_condition = self._conditions[new_weather_name]
        
        print(f"[WeatherSystem] Zmiana pogody: {old_condition.get_display_name()} -> "
              f"{self.current_condition.get_display_name()} (krok {self.current_step})")
        
        self._log_weather_change()
        self._notify_observers()
    
    def _get_random_change_interval(self) -> int:
        """
        Losuje interwał do następnej zmiany pogody
        
        Returns:
            int: Liczba kroków do zmiany
        """
        min_interval, max_interval = config.WEATHER_CHANGE_INTERVAL
        return random.randint(min_interval, max_interval)
    
    def _log_weather_change(self):
        """Zapisuje zmianę pogody do historii"""
        self.weather_history.append({
            'step': self.current_step,
            'condition': self.current_condition.get_name(),
            'display_name': self.current_condition.get_display_name()
        })
    
    # Observer Pattern - metody Subject
    
    def attach(self, observer):
        """
        Dodaje obserwatora
        
        Args:
            observer: Obserwator implementujący metodę update()
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """
        Usuwa obserwatora
        
        Args:
            observer: Obserwator do usunięcia
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self):
        """Powiadamia wszystkich obserwatorów o zmianie pogody"""
        for observer in self._observers:
            observer.update({
                'type': 'weather_change',
                'condition': self.current_condition.get_name(),
                'display_name': self.current_condition.get_display_name(),
                'step': self.current_step
            })
    
    # Metody pomocnicze
    
    def get_current_condition(self) -> WeatherCondition:
        """
        Zwraca aktualny warunek pogodowy
        
        Returns:
            WeatherCondition: Aktualny warunek
        """
        return self.current_condition
    
    def get_weather_stats(self) -> dict:
        """
        Zwraca statystyki pogody
        
        Returns:
            dict: Statystyki
        """
        # Zlicz wystąpienia każdego warunku
        condition_counts = {}
        for entry in self.weather_history:
            condition = entry['condition']
            condition_counts[condition] = condition_counts.get(condition, 0) + 1
        
        return {
            'current': self.current_condition.get_display_name(),
            'changes': len(self.weather_history),
            'condition_counts': condition_counts
        }
    
    def __repr__(self) -> str:
        return f"WeatherSystem(current={self.current_condition.get_name()})"
