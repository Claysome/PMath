from abc import ABC, abstractmethod


class OptionPricingStrats(ABC):
    """Abstract class for option pricing strategy"""
    @abstractmethod
    def calculate_price(self, S0, K, T, r, sigma):
        pass