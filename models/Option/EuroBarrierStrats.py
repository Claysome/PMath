import numpy as np
from strats_base import OptionPricingStrats


class MonteCarloPricing(OptionPricingStrats):
    """Monte Carlo pricing model pricing strategy"""
    def calculate_price(self, S0, T, r, sigma, KU, KL, BU, BL, R1, R2, m=252, n=10000):
        dt = T / m
        z = np.random.randn(n, m)
        payoff = np.zeros(n)
        S = np.zeros((n, m + 1))

        for i in range(n):
            S[i, 0] = S0
            for j in range(m):
                S[i, j + 1] = S[i, j] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z[i, j])
            if S[i, m] > BL and S[i, m] < BU:
                payoff[i] = max(S[i, m] - KU, 0) + max(KL - S[i, m], 0) + R2
            elif S[i, m] <= BL or S[i, m] >= BU:
                payoff[i] = R1 + R2

        v = sum(payoff) / n * np.exp(-r * T)
        return v


if __name__ == '__main__':
    mc = MonteCarloPricing()
    print(mc.calculate_price(6855, 1, 0.036, 0.15, 6855*1.02, 6855*0.98, 6855*1.2, 6855*0.8, 6855*0.05, 6855*0.01)/6855)

        