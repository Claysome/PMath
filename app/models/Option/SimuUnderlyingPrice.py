import numpy as np
import matplotlib.pyplot as plt


class Simulation:

    def __init__(self):
        pass

    def draw_paths(self, S0, T, r, sigma, m, n):
        dt = T / m
        S = np.zeros(m + 1)
        x = np.linspace(0, T, m + 1)
        
        for i in range(n):
            S[0] = S0
            for j in range(0, m):
                S[j+1] = S[j] * np.exp((r - 0.5 * sigma ** 2)) * dt + sigma * np.sqrt(dt) * np.random.randn()
            plt.plot(x, S)

        plt.title("Simulation of underlying asset price")
        plt.xlabel("Steps of time")
        plt.ylabel("Price")
        plt.show()


if __name__ == '__main__':

    bot = Simulation()
    bot.draw_paths(100, 1, 0.01, 0.3, 252, 100)