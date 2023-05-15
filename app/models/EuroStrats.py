import numpy as np
from scipy.stats import norm
from strats_base import OptionPricingStrats


class BlackScholesPricing(OptionPricingStrats):
    """Black-Scholes-Merton pricing model pricing strategy"""
    def calculate_price(self, S0, K, T, r, sigma, otype):
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        Nd1 = norm.cdf(d1)
        Nd2 = norm.cdf(d2)
        if otype == "call":
            price = S0 * Nd1 - np.exp(-r * T) * K * Nd2
        elif otype == "put":
            price = S0 * Nd1 - np.exp(-r * T) * K * Nd2 + np.exp(-r * T) * K - S0
        return price

    def delta(self, S0, K, T, r, sigma, otype):
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        if otype == "call":
            delta = norm.cdf(d1)
        elif otype == "put":
            delta = norm.cdf(d1) - 1
        return delta

    def gamma(self, S0, K, T, r, sigma, otype):
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        gamma = norm.pdf(d1) / (S0 * sigma * np.sqrt(T))
        return gamma

    def theta(self, S0, K, T, r, sigma, otype):
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        Nd2 = norm.cdf(d2)
        if otype == "call":
            theta = -S0 * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * Nd2
        elif otype == "put":
            theta = -S0 * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * Nd2
        return theta
    
    def rho(self, S0, K, T, r, sigma, otype):
        d2 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        Nd2 = norm.cdf(d2)
        if otype == "call":
            rho = K * T * np.exp(-r * T) * Nd2
        elif otype == "put":
            rho = -K * T * np.exp(-r * T) * Nd2
        return rho
    
    def vega(self, S0, K, T, r, sigma, otype):
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        vega = S0 * norm.pdf(d1) * np.sqrt(T)
        return vega


class BinomialTreePricing(OptionPricingStrats):
    """Binomial pricing model pricing strategy"""
    def calculate_price(self, S0, K, T, r, sigma, otype, m=1000):
        dt = T / m
        df = np.exp(-r * dt)
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)
        # initialize the stock price tree
        mu = np.arange(m + 1)
        mu = np.resize(mu, (m + 1, m + 1))
        md = np.transpose(mu)
        mu = u ** (mu - md)
        md = d ** md
        S = S0 * mu * md

        if otype == "call":
            V = np.maximum(S - K, 0)
        else:
            V = np.maximum(K - S, 0)
        z = 0
        for t in range(m - 1, -1, -1):
            V[0:m - z, t] = (p * V[0:m - z, t + 1] + (1 - p) * V[1:m - z + 1, t + 1]) * df
            z += 1
        return V[0, 0]

    def delta(self, S0, K, T, r, sigma, otype, m=1000):
        dt = T / m
        df = np.exp(-r * dt)
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)
        # initialize the stock price tree
        mu = np.arange(m + 1)
        mu = np.resize(mu, (m + 1, m + 1))
        md = np.transpose(mu)
        mu = u ** (mu - md)
        md = d ** md
        S = S0 * mu * md

        if otype == "call":
            V = np.maximum(S - K, 0)
        else:
            V = np.maximum(K - S, 0)
        z = 0
        for t in range(m - 1, -1, -1):
            V[0:m - z, t] = (p * V[0:m - z, t + 1] + (1 - p) * V[1:m - z + 1, t + 1]) * df
            z += 1
        delta = (V[0, 1] - V[1, 1]) / (S[0, 1] - S[1, 1])
        return delta
