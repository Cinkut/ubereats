# Symulacja Uber Eats

## Opis projektu

Kompleksowa symulacja systemu dostaw jedzenia z dynamicznym modelem pogodowym, adaptacyjnym cenowaniem i wizualizacją w czasie rzeczywistym.

### Funkcjonalności

-  **Dynamiczne cenowanie** - cena zależna od dystansu, natężenia zamówień (surge pricing) i warunków pogodowych
-  **System pogodowy** - 5 warunków atmosferycznych wpływających na prędkość kurierów, ryzyko wypadku i ceny
-  **Wypadki kurierów** - losowe wypadki zależne od pogody (najwyższe ryzyko na gołoledzi)
-  **Wizualizacja real-time** - animowana mapa z kurierami, restauracjami i klientami
-  **Statystyki** - śledzenie metryk: czas dostawy, przychody, wypadki, surge multiplier
-  **Persystencja danych** - zapis do bazy SQLite przez SQLAlchemy ORM

## Warunki pogodowe

| Pogoda          | Prędkość | Ryzyko wypadku | Mnożnik ceny |
| --------------- | -------- | -------------- | ------------ |
|  Czyste niebo | 100%     | 0.01%          | 1.0x         |
|  Deszcz       | 80%      | 0.1%           | 1.3x         |
|  Śnieg        | 60%      | 0.3%           | 1.6x         |
|  Mróz         | 70%      | 0.5%           | 1.5x         |
|  Gołoledź     | 40%      | 1.5%           | 2.5x         |

## Wzorce projektowe

### 1. Strategy (Strategia)

- **Lokalizacja:** `strategies/`
- **Zastosowanie:**
  - Strategie cenowe (`pricing_strategy.py`) - różne algorytmy obliczania ceny
  - Strategie routingu (`routing_strategy.py`) - różne metody wyznaczania trasy
- **Korzyści:** Łatwe dodawanie nowych algorytmów bez modyfikacji istniejącego kodu (Open/Closed)

### 2. State (Stan)

- **Lokalizacja:** `states/`
- **Zastosowanie:** Stany kuriera (wolny → do restauracji → do klienta → wypadek)
- **Korzyści:** Kurier zmienia zachowanie w zależności od stanu bez ifologii

### 3. Observer (Obserwator)

- **Lokalizacja:** `observers/`
- **Zastosowanie:** Śledzenie zdarzeń (nowe zamówienie, dostawa, wypadek)
- **Korzyści:** Luźne powiązanie między komponentami (Dependency Inversion)

### 4. Factory (Fabryka)

- **Lokalizacja:** `factories/`
- **Zastosowanie:** Tworzenie kurierów, zamówień, restauracji
- **Korzyści:** Centralizacja logiki tworzenia obiektów z walidacją

### 5. Singleton

- **Lokalizacja:** `simulation/simulation_engine.py`
- **Zastosowanie:** Jeden globalny silnik symulacji
- **Korzyści:** Gwarancja jednej instancji zarządzającej stanem

## Zasady SOLID

### S - Single Responsibility Principle

Każda klasa ma jedną odpowiedzialność:

- `WeatherSystem` - tylko zarządzanie pogodą
- `PricingEngine` - tylko obliczanie cen
- `CourierManager` - tylko zarządzanie kurierami
- `DispatchService` - tylko przydzielanie zamówień

### O - Open/Closed Principle

System otwarty na rozszerzenia, zamknięty na modyfikacje:

- Nowy warunek pogodowy? Dziedzicz po `WeatherCondition`
- Nowa strategia cenowa? Dziedzicz po `PricingStrategy`
- Nie trzeba modyfikować istniejącego kodu

### L - Liskov Substitution Principle

Obiekty mogą być zastępowane przez podtypy:

- Wszystkie stany kuriera są wymienne przez `CourierState`
- Wszystkie strategie cenowe przez `PricingStrategy`
- Wszystkie warunki pogodowe przez `WeatherCondition`

### I - Interface Segregation Principle

Małe, wyspecjalizowane interfejsy:

- `Observer` - tylko `update(event)`
- `Subject` - tylko `attach()`, `detach()`, `notify()`
- Klasy nie są zmuszane do implementacji nieużywanych metod

### D - Dependency Inversion Principle

Zależności od abstrakcji, nie konkretnych klas:

- `SimulationEngine` → `PricingStrategy` (ABC)
- `Courier` → `CourierState` (ABC)
- `WeatherSystem` → `WeatherCondition` (ABC)
- Dependency Injection przez konstruktory

## Problem złożony (nieliniowy)

### 1. Surge Pricing

Cena rośnie **nieliniowo** z natężeniem zamówień:

```
surge_multiplier = (active_orders / available_couriers) ^ 1.2
```

### 2. Kaskadowy efekt wypadków

- Wypadek kuriera → mniej dostępnych kurierów
- Mniej kurierów → wzrost surge pricing
- Wzrost cen → dłuższe czasy oczekiwania
- **Efekt nieliniowy** przy gołoledzi!

### 3. Interakcja pogody z systemem

- Pogoda wpływa na prędkość
- Pogoda wpływa na wypadki
- Wypadki wpływają na dostępność
- Dostępność wpływa na ceny
- **Wielowymiarowy problem nieliniowy**

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie

### Podstawowe

```bash
python main.py
```

### Z parametrami

```bash
# 500 kroków, 15 kurierów
python main.py --steps 500 --couriers 15

# Bez wizualizacji (szybciej)
python main.py --no-visual

# Szybka symulacja (2x)
python main.py --speed 2.0

# Wymuszenie gołoledzi na początku
python main.py --weather ice
```

### Parametry CLI

- `--steps N` - liczba kroków symulacji (domyślnie: 1000)
- `--couriers N` - liczba kurierów (domyślnie: 10)
- `--restaurants N` - liczba restauracji (domyślnie: 5)
- `--no-visual` - wyłącz wizualizację
- `--speed X` - przyspieszenie symulacji (1.0 = normalnie)
- `--weather TYPE` - wymuś pogodę na start (clear/rain/snow/frost/ice)

## Sterowanie

- **ESC** - zakończ symulację
- **SPACJA** - pauza/wznowienie
- **↑/↓** - zmiana prędkości symulacji
- **W** - losowa zmiana pogody
- **R** - restart symulacji

## Struktura projektu

```
lab6/
├── main.py                    # Punkt wejścia
├── config.py                  # Konfiguracja
├── requirements.txt           # Zależności
├── README.md                  # Dokumentacja
├── models/                    # Modele domenowe
│   ├── location.py
│   ├── order.py
│   ├── courier.py
│   ├── restaurant.py
│   └── customer.py
├── states/                    # State Pattern
│   ├── courier_state.py      # ABC
│   ├── idle_state.py
│   ├── to_restaurant_state.py
│   ├── to_customer_state.py
│   └── accident_state.py
├── strategies/                # Strategy Pattern
│   ├── pricing_strategy.py   # ABC cenowe
│   ├── routing_strategy.py   # ABC routingu
│   └── ...
├── weather/                   # System pogodowy
│   ├── weather_condition.py  # ABC
│   └── weather_system.py
├── observers/                 # Observer Pattern
│   ├── observer.py           # ABC
│   └── subject.py
├── factories/                 # Factory Pattern
├── services/                  # Logika biznesowa
├── simulation/                # Silnik symulacji
└── visualization/             # GUI (Pygame)
```

## Technologie

- **Python 3.13**
- **Pygame 2.5+** - wizualizacja
- **SQLAlchemy 2.0+** - ORM
- **NumPy 1.24+** - obliczenia

## Wyniki symulacji

Po zakończeniu symulacji generowane są:

- `uber_eats.db` - baza danych SQLite z historią
- `simulation.log` - logi zdarzeń
- Statystyki wyświetlane w konsoli

## Przykładowe metryki

