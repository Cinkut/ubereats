"""
Strategia cenowa: Bazowa cena (opłata stała + dystans)
"""

from strategies.pricing_strategy import PricingStrategy, PricingContext
import config


class BasePricing(PricingStrategy):
    """
    Bazowa strategia cenowa
    
    Oblicza cenę na podstawie:
    - Opłaty stałej (BASE_PRICE)
    - Dystansu (PRICE_PER_KM)
    
    Wzór: BASE_PRICE + distance * PRICE_PER_KM
    """
    
    def calculate(self, context: PricingContext) -> float:
        """
        Oblicza bazową cenę
        
        Args:
            context: Kontekst cenowy
            
        Returns:
            float: Bazowa cena w $
        """
        base = config.BASE_PRICE
        distance_charge = context.distance * config.PRICE_PER_KM
        
        return base + distance_charge
    
    def get_name(self) -> str:
        return "Base Pricing"
