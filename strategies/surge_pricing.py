"""
Strategia cenowa: Surge Pricing (dynamiczne cenowanie)

Cena rośnie NIELINIOWO z natężeniem zamówień - problem złożony!
"""

from strategies.pricing_strategy import PricingStrategy, PricingContext
import config


class SurgePricing(PricingStrategy):
    """
    Surge Pricing - dynamiczne cenowanie
    
    Oblicza dodatkową opłatę na podstawie stosunku:
    - Liczby aktywnych zamówień
    - Liczby dostępnych kurierów
    
    PROBLEM ZŁOŻONY - NIELINIOWY:
    Surge = (active_orders / available_couriers) ^ 1.5
    
    Przykłady:
    - 10 zamówień, 10 kurierów → surge = 1.0x (norma)
    - 20 zamówień, 10 kurierów → surge = 2.8x (!)
    - 30 zamówień, 10 kurierów → surge = 5.2x (!!)
    
    Cena rośnie SZYBCIEJ niż liniowo!
    """
    
    def calculate(self, context: PricingContext) -> float:
        """
        Oblicza dodatkową opłatę surge
        
        Args:
            context: Kontekst cenowy
            
        Returns:
            float: Dodatkowa opłata w $
        """
        # Zabezpieczenie przed dzieleniem przez zero
        if context.num_available_couriers == 0:
            # Brak kurierów = maksymalny surge
            surge_multiplier = 5.0
        else:
            # Oblicz stosunek popyt/podaż
            ratio = context.num_active_orders / context.num_available_couriers
            
            # NIELINIOWY wzrost - potęga 1.5
            # To sprawia że cena rośnie szybciej niż liniowo!
            surge_multiplier = max(1.0, ratio ** 1.5)
            
            # Ogranicz maksymalny surge do rozsądnego poziomu
            surge_multiplier = min(surge_multiplier, 5.0)
        
        # Oblicz bazową cenę i zastosuj surge
        base_price = config.BASE_PRICE + context.distance * config.PRICE_PER_KM
        
        # Dodatkowa opłata = (surge - 1.0) * base_price
        # Przykład: surge 2.0x → dodatkowe 100% ceny bazowej
        additional_charge = (surge_multiplier - 1.0) * base_price
        
        return additional_charge
    
    def get_surge_multiplier(self, context: PricingContext) -> float:
        """
        Oblicza sam mnożnik surge (do statystyk)
        
        Args:
            context: Kontekst cenowy
            
        Returns:
            float: Mnożnik surge
        """
        if context.num_available_couriers == 0:
            return 5.0
        
        ratio = context.num_active_orders / context.num_available_couriers
        surge = max(1.0, ratio ** 1.5)
        return min(surge, 5.0)
    
    def get_name(self) -> str:
        return "Surge Pricing"
