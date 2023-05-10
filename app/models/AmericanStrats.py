import numpy as np
from scipy.stats import norm
from strats_base import OptionPricingStrats


class MonteCalroPricing(OptionPricingStrats):
    """Monte Carlo pricing model pricing strategy"""