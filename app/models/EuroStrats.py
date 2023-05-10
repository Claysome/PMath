import numpy as np
from scipy.stats import norm
from strats_base import OptionPricingStrats


class BlackScholesPricing(OptionPricingStrats):
    """Black-Scholes-Merton pricing model pricing strategy"""
    def calculate_price(self, S0, K, T, r, sigma):
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        Nd1 = norm.cdf(d1)
        Nd2 = norm.cdf(d2)
        price = S0 * Nd1 - np.exp(-r * T) * K * Nd2
        return price


if __name__ == '__main__':
    bsm = BlackScholesPricing()
    print(bsm.calculate_price(100, 100, 1, 0.05, 0.3))