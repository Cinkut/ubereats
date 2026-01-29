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
        # Oblicz stosunek popyt/podaż
        if context.num_available_couriers == 0:
            # Brak kurierów:
            # Zamiast panikować (dzielić przez 0.5), zakładamy "wirtualną pojemność"
            # równą 5 kurierom (zakładamy, że zaraz ktoś wróci).
            # To zapobiega skokom ceny do 10x przy zaledwie 3 zamówieniach.
            ratio = context.num_active_orders / 5.0
        else:
            ratio = context.num_active_orders / context.num_available_couriers
            
        # Łagodniejszy wzrost - potęga 1.2 (zamiast 1.5)
        surge_multiplier = max(1.0, ratio ** 1.2)
        
        # Ogranicz maksymalny surge
        surge_multiplier = min(surge_multiplier, 10.0)
        
        # Oblicz bazową cenę i zastosuj surge
        base_price = config.BASE_PRICE + context.distance * config.PRICE_PER_KM
        
        # Dodatkowa opłata = (surge - 1.0) * base_price
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
            ratio = context.num_active_orders / 5.0
        else:
            ratio = context.num_active_orders / context.num_available_couriers
            
        surge = max(1.0, ratio ** 1.2)
        return min(surge, 10.0)
    
    def get_name(self) -> str:
        return "Surge Pricing"
