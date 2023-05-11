from AsianStrats import MonteCalroPricing


class AsianCall:
    """Asian call option class"""
    def __init__(self, S0,
                       K,
                       T,
                       r,
                       sigma,
                       pricing_strats):
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.sigma = sigma
        self.pricing_strats = pricing_strats

    def price(self):
        return self.pricing_strats.calculate_price(self.S0,
                                                    self.K,
                                                    self.T,
                                                    self.r,
                                                    self.sigma)
    


if __name__ == '__main__':
    mc = MonteCalroPricing()
    call = AsianCall(100, 100, 1, 0.05, 0.3, mc)
    print(call.price())