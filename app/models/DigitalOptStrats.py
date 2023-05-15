import numpy as np
from strats_base import OptionPricingStrats


class MonteCarloPricing(OptionPricingStrats):
    """Monte Carlo pricing model pricing strategy"""
    def calculate_price(self, S0, K, T, r, sigma, R1, R2, m=252, n=10000):
        dt = T / m
        z = np.random.randn(n, m)
        payoff = np.zeros(n)

        for i in range(n):
            S = S0
            for j in range(m):
                S = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z[i, j])
            if S > K:
                payoff[i] = R1
            elif S < K:
                payoff[i] = R2
        
        v = sum(payoff) * np.exp(-r * T) / n 
        return v
    

if __name__ == '__main__':
    mc = MonteCarloPricing()
    print(mc.calculate_price(100, 101, 1, 0.05, 0.3, 0, 1))