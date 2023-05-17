import numpy as np
from scipy.stats import norm
from strats_base import OptionPricingStrats


class MonteCarloPricing(OptionPricingStrats):
    """Monte Carlo pricing model pricing strategy"""
    # def calculate_price(self, S0, K, T, r, sigma, n=10000):
    #     z = np.random.standard_normal(n)
    #     ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z)
    #     hT = np.maximum(ST - K, 0)
    #     price = np.exp(-r * T) * np.sum(hT) / n
    #     return price

    def calculate_price(self, S0, K, T, r, sigma, m=100, n=5000):
        deltaT = T / m  # time interval
        S = np.zeros((n, m + 1))
        A = np.zeros((n, m + 1))
        V1 = np.zeros((n, 1))
        for i in range(0, n):
            S[i, 0] = S0
            A[i, 0] = S0
            for j in range(1, m + 1):
                S[i, j] = S[i, j - 1] * np.exp((r - 0.5 * sigma ** 2) * deltaT + sigma * np.sqrt(deltaT) * np.random.randn())
                A[i, j] = A[i, j - 1] + S[i, j]
            V1[i] = + np.exp(-r * T) * max(A[i, m] / (m + 1) - K, 0)
        
        price = sum(V1) / n
        return price
    

if __name__ == '__main__':
    mc = MonteCarloPricing()
    print(mc.calculate_price(100, 103, 1, 0.05, 0.3, 100, 10000))