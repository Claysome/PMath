import numpy as np
from scipy.stats import norm
from strats_base import OptionPricingStrats


class MonteCalroPricing(OptionPricingStrats):
    """Monte Carlo pricing model pricing strategy"""
    # def calculate_price(self, S0, K, T, r, sigma, n=10000):
    #     z = np.random.standard_normal(n)
    #     ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z)
    #     hT = np.maximum(ST - K, 0)
    #     price = np.exp(-r * T) * np.sum(hT) / n
    #     return price

    def calculate_price(self, S0, K, T, r, sigma, m=100, n=5000):
        deltaT = T / m  # time interval
        V1 = 0
        for i in range(0, n):
            S = S0
            A = S0
            for j in range(0, m):
                e = np.random.normal(0, 1)
                S = S * np.exp((r - 0.5 * sigma ** 2) * deltaT + sigma * np.sqrt(deltaT) * e)
                A = A + S
            V1 = V1 + np.exp(-r * T) * max(A / (m + 1) - K, 0)
        
        price = V1 / n
        return price
    

if __name__ == '__main__':
    mc = MonteCalroPricing()
    print(mc.calculate_price(100, 103, 1, 0.03, 0.2))