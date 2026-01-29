#!/usr/bin/env python3
"""
Symulacja systemu dostaw Uber Eats

Projekt końcowy - Technologie Obiektowe
Autor: Marcin Łukasz
Data: 2026-01-27

Wzorce projektowe demonstrowane w projekcie:
- State Pattern: Stany kuriera (Idle, ToRestaurant, ToCustomer, Accident)
- Strategy Pattern: Strategie cenowe (Base, Surge, Weather) i routingu
- Observer Pattern: Śledzenie zdarzeń (Logger, OrderTracker, RevenueTracker)
- Factory Pattern: Tworzenie obiektów (CourierFactory, OrderFactory, RestaurantFactory)
- Singleton Pattern: SimulationEngine, DatabaseManager

Zasady SOLID:
- Single Responsibility: Każda klasa ma jedną odpowiedzialność
- Open/Closed: Łatwo rozszerzyć o nowe stany, strategie, warunki pogodowe
- Liskov Substitution: Wszystkie pochodne są wymienne
- Interface Segregation: Małe, wyspecjalizowane interfejsy
- Dependency Inversion: Zależności od abstrakcji, nie konkretnych klas

Uruchomienie:
    python main.py                          # Domyślna symulacja
    python main.py --steps 500              # 500 kroków
    python main.py --couriers 15            # 15 kurierów
    python main.py --no-visual              # Bez wizualizacji
    python main.py --weather ice            # Start z gołoledzią
"""

import argparse
import sys
import os

# Dodaj ścieżkę do projektu
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from simulation.simulation_engine import SimulationEngine
import config


def parse_arguments():
    """
    Parsuje argumenty linii poleceń
    
    Returns:
        argparse.Namespace: Argumenty
    """
    parser = argparse.ArgumentParser(
        description='Symulacja systemu dostaw Uber Eats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Wzorce projektowe:
  • State     - Stany kuriera (Idle/ToRestaurant/ToCustomer/Accident)
  • Strategy  - Strategie cenowe i routingu
  • Observer  - Śledzenie zdarzeń (Logger/OrderTracker/RevenueTracker)
  • Factory   - Tworzenie obiektów (Courier/Order/Restaurant)
  • Singleton - SimulationEngine

Problem zlozony - nieliniowy:
  • Surge Pricing: cena rosnie nieliniowo z natezeniem zamowien
  • Kaskada wypadkow: wypadek > mniej kurierow > wyzsze ceny > wiecej wypadkow
  • Interakcja pogody z systemem: pogoda > predkosc > wypadki > dostepnosc > ceny

Przykłady:
  python main.py --steps 1000 --couriers 10
  python main.py --weather ice --steps 500
  python main.py --no-visual --speed 10.0
"""
    )
    
    parser.add_argument(
        '--steps', '-s',
        type=int,
        default=1000,
        help='Liczba kroków symulacji (0 = bez limitu, domyślnie: 1000)'
    )
    
    parser.add_argument(
        '--infinite', '-i',
        action='store_true',
        help='Tryb nieskończony (to samo co --steps 0)'
    )
    
    parser.add_argument(
        '--couriers', '-c',
        type=int,
        default=config.NUM_COURIERS,
        help=f'Liczba kurierów (domyślnie: {config.NUM_COURIERS})'
    )
    
    parser.add_argument(
        '--restaurants', '-r',
        type=int,
        default=config.NUM_RESTAURANTS,
        help=f'Liczba restauracji (domyślnie: {config.NUM_RESTAURANTS})'
    )
    
    parser.add_argument(
        '--no-visual', '-q',
        action='store_true',
        help='Wyłącz wizualizację Pygame (szybsza symulacja)'
    )
    
    parser.add_argument(
        '--speed', '-S',
        type=float,
        default=config.TIME_SCALE,
        help=f'Przyspieszenie symulacji (domyślnie: {config.TIME_SCALE})'
    )
    
    parser.add_argument(
        '--weather', '-w',
        type=str,
        choices=['clear', 'rain', 'snow', 'frost', 'ice'],
        default=None,
        help='Wymuś warunek pogodowy na start (domyślnie: losowo)'
    )
    
    return parser.parse_args()


def print_header():
    """Wyświetla nagłówek aplikacji"""
    print("""
===================================================================
                                                               
   Uber Eats Simulation - Delivery System                     
                                                               
   Demonstracja wzorc projektowych i zasad SOLID               
   Projekt koncowy - Technologie Obiektowe                     
                                                               
   Autor: Marcin Lukasz                                        
   Data: 2026-01-27                                            
                                                               
===================================================================
""")


def print_patterns_info():
    """Wyświetla informacje o wzorcach projektowych"""
    print("\n[WZORCE PROJEKTOWE]")
    print("  • State Pattern      - Stany kuriera (5 stanow)")
    print("  • Strategy Pattern   - Cenowanie (3) + Routing (2: Drone vs Biker)")
    print("  • Observer Pattern   - Obserwatorzy zdarzen (3 observery)")
    print("  • Factory Pattern    - Fabryki obiektow (3 fabryki)")
    print("  • Singleton Pattern  - SimulationEngine")
    
    print("\n[ZASADY SOLID]")
    print("  • S - Single Responsibility: kazda klasa ma jedna odpowiedzialnosc")
    print("  • O - Open/Closed: latwo rozszerzyc bez modyfikacji")
    print("  • L - Liskov Substitution: pochodne sa wymienne")
    print("  • I - Interface Segregation: male, wyspecjalizowane interfejsy")
    print("  • D - Dependency Inversion: zaleznosci od abstrakcji")
    
    print("\n[*] PROBLEM ZLOZONY - NIELINIOWY:")
    print("  • Surge Pricing: cena = (zamowienia/kurierzy)^1.5")
    print("  • Kaskada wypadkow przy gololedzi")
    print("  • Wielowymiarowa interakcja: pogoda <-> predkosc <-> wypadki <-> ceny")


def main():
    """Główna funkcja programu"""
    # Parsuj argumenty
    args = parse_arguments()
    
    # Obsługa trybu nieskończonego
    if args.infinite:
        args.steps = 0
    
    # Wyświetl nagłówek
    print_header()
    print_patterns_info()
    
    # Informacje o symulacji
    print("\n" + "=" * 70)
    print("PARAMETRY SYMULACJI")
    print("=" * 70)
    
    steps_info = "bez limitu (nieskończona)" if args.steps <= 0 else str(args.steps)
    print(f"  • Kroki:        {steps_info}")
    print(f"  • Kurierzy:     {args.couriers}")
    print(f"  • Restauracje:  {args.restaurants}")
    print(f"  • Wizualizacja: {'NIE' if args.no_visual else 'TAK (Pygame)'}")
    print(f"  • Prędkość:     {args.speed}x")
    if args.weather:
        print(f"  • Pogoda:       {args.weather} (wymuszona)")
    else:
        print(f"  • Pogoda:       losowa")
    print("=" * 70)
    
    # Utwórz silnik symulacji
    try:
        engine = SimulationEngine(
            num_couriers=args.couriers,
            num_restaurants=args.restaurants,
            time_scale=args.speed
        )
        
        # Ustaw pogodę jeśli wymuszono
        if args.weather:
            engine.weather_system.set_weather(args.weather)
            print(f"\n[Main] Wymuszona pogoda: {engine.weather_system.current_condition.get_display_name()}")
        
        # Uruchom symulację
        print("\n[*] URUCHAMIANIE SYMULACJI...\n")
        
        engine.run(
            max_steps=args.steps,
            visualize=not args.no_visual
        )
        
    except KeyboardInterrupt:
        print("\n\n[Main] Symulacja przerwana przez uzytkownika (Ctrl+C)")
    
    except Exception as e:
        print(f"\n[Main] BLAD: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n[OK] Symulacja zakonczona pomyslnie!")
    print(f"[LOG] Logi zapisane w: {config.LOG_FILE}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
