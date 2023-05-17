from AmericanStrats import BinomialPricing, MonteCalroPricing


class AmericanCall:
    """American call option class"""
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
    bp = BinomialPricing()
    mc = MonteCalroPricing()
    call = AmericanCall(100, 102, 1, 0.03, 0.2, mc)
    print(call.price())