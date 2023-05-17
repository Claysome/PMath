import numpy as np
from strats_base import OptionPricingStrats


class BinomialPricing(OptionPricingStrats):
    """Binomial pricing model pricing strategy"""
    def calculate_price(self, S0, K, T, r, sigma, m=1000):
        dt = T / m
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        df = np.exp(-r * dt)
        p = (np.exp(r * dt) - d) / (u - d)
        V = np.zeros(m + 1)

        for i in range(m + 1):
            V[i] = max(S0 * u ** (2 * i - m) - K, 0)
        for n in range(m - 1, -1, -1):
            for j in range(n + 1):
                V[j] = max(df * (p * V[j+1] + (1 - p) * V[j]), max(S0 * u ** (2 * j - n) - K, 0))

        return V[0]


class MonteCarloPricing(OptionPricingStrats):
    """Monte Carlo LS pricing model pricing strategy"""
    def calculate_price(self, S0, K, T, r, sigma, m=2440, n=10000):
        dt = T / m
        df = np.exp(-r * dt)
        z = np.random.randn(m, n)
        M = np.shape(z)[0]
        S = np.zeros((M, m + 1))
        S[:, 0] = S0

        for i in range(m):
            S[:, i + 1] = S[:, i] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z[:, i])

        h = np.maximum(S - K, 0)
        V = np.copy(h)

        for t in range(m - 1, 0, -1):
            reg = np.polyfit(S[:, t], V[:, t + 1] * df, 4)
            C = np.polyval(reg, S[:, t])
            V[:, t] = np.where(C > h[:, t], V[:, t + 1] * df, h[:, t])

        val = df * sum(V[:, 1]) / M
        return val









if __name__ == '__main__':
    bp = BinomialPricing()
    print(bp.calculate_price(100, 102, 1, 0.03, 0.2, 1000))
    mc = MonteCarloPricing()
    print(mc.calculate_price(100, 102, 1, 0.03, 0.2))