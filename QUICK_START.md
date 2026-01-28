# Quick Start - Symulacja Uber Eats

## Instalacja

```bash
cd lab6
pip install -r requirements.txt
```

## Uruchomienie

### Podstawowe
```bash
python main.py
```

### Przykłady

```bash
# Szybka symulacja bez wizualizacji
python main.py --steps 100 --no-visual

# Gołoledź - demonstracja wypadków
python main.py --weather ice --steps 500

# Więcej kurierów i restauracji
python main.py --couriers 20 --restaurants 10

# Szybka symulacja (10x)
python main.py --speed 10.0 --no-visual
```

## Sterowanie (z wizualizacją)

- **SPACE** - Pauza/Wznowienie
- **ESC** - Zakończ
- **↑/↓** - Zmień prędkość
- **W** - Zmień pogodę

## Wyniki

Po zakończeniu symulacji:
- **Logi**: `lab6/simulation.log`
- **Baza danych**: `lab6/uber_eats.db`
- **Statystyki**: Wyświetlane w konsoli

## Scenariusze testowe

### 1. Normalna pogoda
```bash
python main.py --weather clear --steps 200 --no-visual
```
**Oczekiwany efekt**: Prawie brak wypadków, stabilne ceny

### 2. Gołoledź (szklanka)
```bash
python main.py --weather ice --steps 200 --no-visual
```
**Oczekiwany efekt**: Wiele wypadków, wysokie ceny, spowolnienie dostaw

### 3. Szpica zamówień (mało kurierów)
```bash
python main.py --couriers 3 --steps 200 --no-visual
```
**Oczekiwany efekt**: Wysoki surge pricing (3x-5x), długie czasy oczekiwania

### 4. Kaskada wypadków
```bash
python main.py --weather ice --couriers 3 --steps 300 --no-visual
```
**Oczekiwany efekt**: Nieliniowy problem - wypadki → mniej kurierów → wyższe ceny → więcej zamówień w kolejce

## Struktura projektu

```
lab6/
├── main.py                 # Punkt wejścia
├── config.py               # Konfiguracja
├── models/                 # Modele domenowe
├── states/                 # State Pattern (stany kuriera)
├── strategies/             # Strategy Pattern (cenowanie, routing)
├── weather/                # System pogodowy
├── observers/              # Observer Pattern
├── factories/              # Factory Pattern
├── services/               # Logika biznesowa
├── simulation/             # Silnik symulacji
├── visualization/          # GUI (Pygame)
├── database/               # ORM (SQLAlchemy)
└── utils/                  # Narzędzia pomocnicze
```

## Wzorce projektowe

1. **State Pattern**: 4 stany kuriera (Idle, ToRestaurant, ToCustomer, Accident)
2. **Strategy Pattern**: Strategie cenowe (Base, Surge, Weather) i routingu
3. **Observer Pattern**: 3 observery (Logger, OrderTracker, RevenueTracker)
4. **Factory Pattern**: 3 fabryki (Courier, Order, Restaurant)
5. **Singleton Pattern**: SimulationEngine, DatabaseManager

## Problem złożony - nieliniowy

- **Surge Pricing**: `cena = (zamówienia/kurierzy)^1.5` → nieliniowy wzrost!
- **Kaskada wypadków**: wypadek → mniej kurierów → surge → więcej wypadków
- **Interakcja pogody**: pogoda → prędkość → wypadki → dostępność → ceny

## Troubleshooting

### Błąd importu pygame
```bash
pip install pygame
```

### Błąd importu sqlalchemy
```bash
pip install sqlalchemy
```

### Błąd kodowania (Windows)
Projekt automatycznie używa ASCII-safe znaków dla kompatybilności z Windows console.

## Autor

Marcin Łukasz  
Projekt końcowy - Technologie Obiektowe  
2026-01-27
