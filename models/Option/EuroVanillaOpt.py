from EuroStrats import BlackScholesPricing


class EuroVanillaOpt:
    """European vanilla option class"""
    def __init__(self, S0,
                       K,
                       T,
                       r,
                       sigma,
                       otype,
                       pricing_strats):
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.sigma = sigma
        self.otype = otype
        self.pricing_strats = pricing_strats

    def price(self):
        return self.pricing_strats.calculate_price(self.S0,
                                                    self.K,
                                                    self.T,
                                                    self.r,
                                                    self.sigma,
                                                    self.otype)
    
    def greeks(self):
        greeks = {}
        greeks["delta"] = self.pricing_strats.delta(self.S0,
                                                    self.K,
                                                    self.T,
                                                    self.r,
                                                    self.sigma,
                                                    self.otype)
        greeks["gamma"] = self.pricing_strats.gamma(self.S0,
                                                    self.K,
                                                    self.T,
                                                    self.r,
                                                    self.sigma,
                                                    self.otype)
        greeks["theta"] = self.pricing_strats.theta(self.S0,
                                                    self.K,
                                                    self.T,
                                                    self.r,
                                                    self.sigma,
                                                    self.otype)
        greeks["rho"] = self.pricing_strats.rho(self.S0,
                                                    self.K,
                                                    self.T,
                                                    self.r,
                                                    self.sigma,
                                                    self.otype)
        greeks["vega"] = self.pricing_strats.vega(self.S0,
                                                    self.K,
                                                    self.T,
                                                    self.r,
                                                    self.sigma,
                                                    self.otype)
        return greeks

    


if __name__ == '__main__':
    bsm = BlackScholesPricing()
    call = EuroVanillaOpt(100, 100, 1, 0.05, 0.3, "call", bsm)
    print(call.price())
    print(call.greeks())