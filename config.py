"""
Konfiguracja globalna symulacji Uber Eats
"""

# Parametry mapy
MAP_WIDTH = 800
MAP_HEIGHT = 600
GRID_SIZE = 50  # rozmiar siatki dla routingu

# Parametry symulacji
NUM_RESTAURANTS = 5
NUM_COURIERS = 10
NUM_CUSTOMERS_POOL = 20  # pula potencjalnych klientów

# Częstotliwość zamówień
ORDER_SPAWN_RATE = 0.3  # prawdopodobieństwo nowego zamówienia/step (30%)

# Cenowanie
BASE_PRICE = 5.0  # $ - bazowa cena dostawy
PRICE_PER_KM = 0.015  # $/jednostka - cena za dystans (dystans w pikselach!)

# Parametry kurierów
COURIER_BASE_SPEED = 10.0  # jednostek/step (pikseli na krok)
ACCIDENT_RECOVERY_TIME = 50  # steps - czas nieaktywności po wypadku

# Czas przygotowania jedzenia w restauracji
RESTAURANT_PREPARATION_TIME_MIN = 20  # min kroków (szybka restauracja)
RESTAURANT_PREPARATION_TIME_MAX = 50  # max kroków (wolna restauracja)

# Pogoda
WEATHER_CHANGE_INTERVAL = (100, 300)  # (min, max) steps między zmianami pogody

# Mnożniki prędkości dla różnych warunków pogodowych
WEATHER_SPEED_MULTIPLIERS = {
    'clear': 1.0,      # normalna prędkość
    'rain': 0.8,       # 20% wolniej
    'snow': 0.6,       # 40% wolniej
    'frost': 0.7,      # 30% wolniej
    'ice': 0.4         # 60% wolniej (gołoledź)
}

# Prawdopodobieństwo wypadku (per step gdy kurier się porusza)
WEATHER_ACCIDENT_PROBABILITY = {
    'clear': 0.0001,   # 0.01% (praktycznie brak)
    'rain': 0.001,     # 0.1%
    'snow': 0.003,     # 0.3%
    'frost': 0.005,    # 0.5%
    'ice': 0.015       # 1.5% (najwyższe ryzyko)
}

# Mnożniki ceny dla różnych warunków pogodowych
WEATHER_PRICE_MULTIPLIERS = {
    'clear': 1.0,
    'rain': 1.3,       # +30%
    'snow': 1.6,       # +60%
    'frost': 1.5,      # +50%
    'ice': 2.5         # +150%
}

# Prawdopodobieństwa wystąpienia pogody (suma = 1.0)
WEATHER_PROBABILITIES = {
    'clear': 0.40,     # 40%
    'rain': 0.25,      # 25%
    'snow': 0.15,      # 15%
    'frost': 0.10,     # 10%
    'ice': 0.10        # 10%
}

# Wizualizacja
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
MAP_OFFSET_X = 20
MAP_OFFSET_Y = 50
STATS_PANEL_WIDTH = 350

# Kolory (RGB)
COLOR_BACKGROUND = (240, 240, 240)
COLOR_ROAD = (200, 200, 200)
COLOR_RESTAURANT = (220, 50, 50)
COLOR_CUSTOMER = (255, 200, 0)
COLOR_COURIER_IDLE = (50, 200, 50)
COLOR_COURIER_TO_RESTAURANT = (50, 150, 255)
COLOR_COURIER_TO_CUSTOMER = (255, 150, 50)
COLOR_COURIER_ACCIDENT = (255, 50, 50)
COLOR_TEXT = (20, 20, 20)
COLOR_PANEL = (255, 255, 255)

# Rozmiary elementów
RESTAURANT_SIZE = 12
CUSTOMER_SIZE = 8
COURIER_SIZE = 10

# Symulacja
TIME_SCALE = 1.0  # 1.0 = realtime, 2.0 = 2x szybciej
FPS = 60  # klatek na sekundę

# Logowanie
LOG_FILE = "lab6/simulation.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
