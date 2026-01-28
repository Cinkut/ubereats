"""
Główny silnik symulacji Uber Eats

Orkiestruje wszystkie komponenty systemu
"""

from typing import List, Optional
from models.restaurant import Restaurant
from models.courier import Courier
from factories.courier_factory import CourierFactory
from factories.restaurant_factory import RestaurantFactory
from services.order_manager import OrderManager
from services.courier_manager import CourierManager
from services.dispatch_service import DispatchService
from services.pricing_engine import PricingEngine
from weather.weather_system import WeatherSystem
from observers.statistics_logger import StatisticsLogger
from observers.order_tracker import OrderTracker
from observers.revenue_tracker import RevenueTracker
from simulation.time_manager import TimeManager
import config


class SimulationEngine:
    """
    Główny silnik symulacji
    
    Odpowiada za:
    - Inicjalizację wszystkich komponentów
    - Orkiestrację kroków symulacji
    - Integrację wszystkich managerów
    
    Wzorce projektowe:
    - Facade: upraszcza interfejs do całego systemu
    - Singleton (opcjonalnie): jedna instancja silnika
    
    Zasady SOLID:
    - Single Responsibility: orkiestracja symulacji
    - Dependency Inversion: zależy od abstrakcji (managerów)
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Implementacja Singleton (opcjonalna)"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        num_couriers: int = None,
        num_restaurants: int = None,
        time_scale: float = None
    ):
        """
        Inicjalizuje silnik symulacji
        
        Args:
            num_couriers: Liczba kurierów (None = z config)
            num_restaurants: Liczba restauracji (None = z config)
            time_scale: Przyspieszenie symulacji (None = z config)
        """
        # Unikaj ponownej inicjalizacji (Singleton)
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        
        # Parametry
        self.num_couriers = num_couriers or config.NUM_COURIERS
        self.num_restaurants = num_restaurants or config.NUM_RESTAURANTS
        self.time_scale = time_scale or config.TIME_SCALE
        
        # Komponenty
        self.restaurants: List[Restaurant] = []
        self.couriers: List[Courier] = []
        
        # Serwisy
        self.pricing_engine: Optional[PricingEngine] = None
        self.order_manager: Optional[OrderManager] = None
        self.courier_manager: Optional[CourierManager] = None
        self.dispatch_service: Optional[DispatchService] = None
        
        # Systemy
        self.weather_system: Optional[WeatherSystem] = None
        self.time_manager: Optional[TimeManager] = None
        
        # Observery
        self.statistics_logger: Optional[StatisticsLogger] = None
        self.order_tracker: Optional[OrderTracker] = None
        self.revenue_tracker: Optional[RevenueTracker] = None
        
        # Stan symulacji
        self.current_step = 0
        self.is_running = False
        
        print("[SimulationEngine] Inicjalizacja...")
        self._initialize_components()
        print("[SimulationEngine] Gotowy!")
    
    def _initialize_components(self):
        """Inicjalizuje wszystkie komponenty symulacji"""
        print(f"  • Tworzenie {self.num_restaurants} restauracji...")
        self.restaurants = RestaurantFactory.create_batch(self.num_restaurants)
        
        print(f"  • Tworzenie {self.num_couriers} kurierów...")
        self.couriers = CourierFactory.create_batch(self.num_couriers)
        
        print("  • Inicjalizacja serwisów...")
        self.pricing_engine = PricingEngine()
        self.order_manager = OrderManager(self.restaurants, self.pricing_engine)
        self.courier_manager = CourierManager(self.couriers)
        self.dispatch_service = DispatchService(self.order_manager, self.courier_manager)
        
        print("  • Inicjalizacja systemów...")
        self.weather_system = WeatherSystem()
        self.time_manager = TimeManager(self.time_scale, config.FPS)
        
        print("  • Inicjalizacja obserwatorów...")
        self.statistics_logger = StatisticsLogger()
        self.order_tracker = OrderTracker()
        self.revenue_tracker = RevenueTracker()
        
        # Podłączenie obserwatorów
        self.order_manager.attach(self.statistics_logger)
        self.order_manager.attach(self.order_tracker)
        self.order_manager.attach(self.revenue_tracker)
        
        self.courier_manager.attach(self.statistics_logger)
        
        self.weather_system.attach(self.statistics_logger)
    
    def run(self, max_steps: int = 1000, visualize: bool = True):
        """
        Uruchamia symulację
        
        Args:
            max_steps: Maksymalna liczba kroków
            visualize: Czy włączyć wizualizację
        """
        self.is_running = True
        
        print(f"\n[SimulationEngine] START symulacji (max {max_steps} kroków)")
        print(f"  • Restauracje: {len(self.restaurants)}")
        print(f"  • Kurierzy: {len(self.couriers)}")
        print(f"  • Pogoda: {self.weather_system.current_condition.get_display_name()}")
        print()
        
        if visualize:
            self._run_with_visualization(max_steps)
        else:
            self._run_without_visualization(max_steps)
        
        self._finalize()
    
    def _run_without_visualization(self, max_steps: int):
        """Uruchamia symulację bez wizualizacji (szybciej)"""
        try:
            while self.is_running and self.current_step < max_steps:
                self.step()
                
                # Co 100 kroków wyświetl postęp
                if self.current_step % 100 == 0:
                    self._print_progress()
        
        except KeyboardInterrupt:
            print("\n\n[SimulationEngine] Przerwano przez użytkownika")
    
    def _run_with_visualization(self, max_steps: int):
        """Uruchamia symulację z wizualizacją Pygame"""
        # Import tutaj aby uniknąć błędów jeśli pygame nie jest zainstalowany
        try:
            from visualization.pygame_view import PygameView
        except ImportError:
            print("[SimulationEngine] BŁĄD: Brak pygame! Uruchamiam bez wizualizacji...")
            self._run_without_visualization(max_steps)
            return
        
        # Utwórz widok
        view = PygameView(self)
        
        try:
            while self.is_running and self.current_step < max_steps:
                # Obsłuż eventy (zamknięcie okna, klawisze)
                if not view.handle_events():
                    break
                
                # Wykonaj krok symulacji
                self.step()
                
                # Renderuj
                view.render()
                
                # Reguluj FPS
                self.time_manager.tick()
        
        except KeyboardInterrupt:
            print("\n\n[SimulationEngine] Przerwano przez użytkownika")
        
        finally:
            view.close()
    
    def step(self):
        """Wykonuje jeden krok symulacji"""
        self.current_step += 1
        
        # 1. Aktualizuj system pogodowy
        self.weather_system.update(self.current_step)
        current_weather = self.weather_system.get_current_condition()
        
        # 2. Aktualizuj manager zamówień (może wygenerować nowe)
        num_available = len(self.courier_manager.get_available_couriers())
        self.order_manager.update(self.current_step, current_weather, num_available)
        
        # 3. Przydziel oczekujące zamówienia do kurierów
        # NOWE: Przekazujemy pogodę - drony nie latają w deszczu/śniegu!
        self.dispatch_service.assign_orders(current_weather)
        
        # 4. Aktualizuj wszystkich kurierów (State Pattern + pogoda)
        self.courier_manager.update_all_couriers(current_weather)
        
        # 5. Aktualizuj time manager
        self.time_manager.update()
    
    def _print_progress(self):
        """Wyświetla postęp symulacji"""
        order_stats = self.order_tracker.get_stats()
        revenue_stats = self.revenue_tracker.get_stats()
        
        print(f"[Krok {self.current_step}] "
              f"Zamówienia: {order_stats['delivered_orders']}/{order_stats['total_orders']} | "
              f"Przychód: ${revenue_stats['total_revenue']:.2f} | "
              f"Pogoda: {self.weather_system.current_condition.get_display_name()}")
    
    def _finalize(self):
        """Finalizuje symulację i wyświetla statystyki"""
        self.is_running = False
        
        print("\n" + "=" * 70)
        print("KONIEC SYMULACJI")
        print("=" * 70)
        
        # Statystyki zamówień
        order_stats = self.order_tracker.get_stats()
        print(f"\nZAMÓWIENIA:")
        print(f"  • Łącznie: {order_stats['total_orders']}")
        print(f"  • Dostarczone: {order_stats['delivered_orders']}")
        print(f"  • Anulowane: {order_stats['cancelled_orders']}")
        print(f"  • Średni czas dostawy: {order_stats['average_delivery_time']:.1f}s")
        
        # Statystyki przychodów
        revenue_stats = self.revenue_tracker.get_stats()
        print(f"\nPRZYCHÓD:")
        print(f"  • Łączny: ${revenue_stats['total_revenue']:.2f}")
        print(f"  • Średnia cena: ${revenue_stats['average_price']:.2f}")
        print(f"  • Średni surge: {revenue_stats['average_surge']:.2f}x")
        print(f"  • Maksymalny surge: {revenue_stats['max_surge']:.2f}x")
        
        # Statystyki kurierów
        total_accidents = sum(c.accidents for c in self.couriers)
        total_deliveries = sum(c.total_deliveries for c in self.couriers)
        total_earnings = sum(c.total_earnings for c in self.couriers)
        
        print(f"\nKURIERZY:")
        print(f"  • Dostawy: {total_deliveries}")
        print(f"  • Zarobki: ${total_earnings:.2f}")
        print(f"  • Wypadki: {total_accidents}")
        
        # Statystyki pogody
        weather_stats = self.weather_system.get_weather_stats()
        print(f"\nPOGODA:")
        print(f"  • Aktualna: {weather_stats['current']}")
        print(f"  • Zmiany: {weather_stats['changes']}")
        
        print("\n" + "=" * 70)
    
    def stop(self):
        """Zatrzymuje symulację"""
        self.is_running = False
    
    def pause(self):
        """Pauzuje symulację"""
        if self.time_manager:
            self.time_manager.pause()
    
    def resume(self):
        """Wznawia symulację"""
        if self.time_manager:
            self.time_manager.resume()
