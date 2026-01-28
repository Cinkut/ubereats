"""
Strategia cenowa: Opłata pogodowa

Dodatkowa opłata za trudne warunki atmosferyczne
"""

from strategies.pricing_strategy import PricingStrategy, PricingContext
import config


class WeatherPricing(PricingStrategy):
    """
    Strategia cenowa uwzględniająca pogodę
    
    Oblicza dodatkową opłatę na podstawie:
    - Mnożnika pogodowego (1.0x - 2.5x)
    - Dystansu dostawy
    
    Czym gorsze warunki, tym wyższa dodatkowa opłata
    
    Przykład:
    - Czyste niebo (1.0x): brak dodatkowej opłaty
    - Deszcz (1.3x): +30% na dystans
    - Gołoledź (2.5x): +150% na dystans
    """
    
    def calculate(self, context: PricingContext) -> float:
        """
        Oblicza dodatkową opłatę pogodową
        
        Args:
            context: Kontekst cenowy
            
        Returns:
            float: Dodatkowa opłata w $
        """
        weather_multiplier = context.weather_condition.get_price_multiplier()
        
        # Dodatkowa opłata na podstawie dystansu
        # (weather_multiplier - 1.0) * distance * PRICE_PER_KM
        # 
        # Przykład: Gołoledź (2.5x), 10km:
        # (2.5 - 1.0) * 10 * 1.5 = 1.5 * 10 * 1.5 = $22.50
        
        if weather_multiplier <= 1.0:
            return 0.0  # Brak dodatkowej opłaty
        
        distance_charge = context.distance * config.PRICE_PER_KM
        additional_charge = (weather_multiplier - 1.0) * distance_charge
        
        return additional_charge
    
    def get_name(self) -> str:
        return "Weather Pricing"
