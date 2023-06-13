#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   order_generator.py
@Time    :   2023/06/13 13:51:22
@Author  :   Clay
'''

import time
import random
import warnings
warnings.filterwarnings('ignore')
import numpy as np

from order import LimitOrder, MarketOrder
from orderbook import OrderBook
from price_history import PriceHistoryDB
from matching_engine import MatchingEngine


class PrimaryOrderGenerator:
    indicative_order_count = 1000
    sigma = 0.1
    k = 1000

    def __init__(self, orderbook:OrderBook, previous_close_price:float):
        self.orderbook = orderbook
        self.previous_close_price = previous_close_price

    def generate_bid_side(self, order_count:int=indicative_order_count):
        random_prices = np.round(
            np.random.normal(
                loc=self.previous_close_price,
                scale=self.sigma * self.previous_close_price,
                size=order_count
            ), decimals=2
        )
        random_bid_prices = random_prices[random_prices < self.previous_close_price]
        random_order_sizes = np.random.randint(low=100, high=1000, size=len(random_bid_prices))
        time_delay = 10**(-self.k)
        for i in range(len(random_bid_prices)):
            self.orderbook.insert_order(
                LimitOrder(
                    direction='Buy',
                    size=random_order_sizes[i],
                    price_limit=random_bid_prices[i]
                )
            )
            time.sleep(time_delay)
    
    def generate_ask_side(self, order_count:int=indicative_order_count):
        random_prices = np.round(
            np.random.normal(
                loc=self.previous_close_price,
                scale=self.sigma * self.previous_close_price,
                size=order_count
            ), decimals=2
        )
        random_ask_prices = random_prices[random_prices > self.previous_close_price]
        random_order_sizes = np.random.randint(low=100, high=1000, size=len(random_ask_prices))
        time_delay = 10**(-self.k)
        for i in range(len(random_ask_prices)):
            self.orderbook.insert_order(
                LimitOrder(
                    direction='Sell',
                    size=random_order_sizes[i],
                    price_limit=random_ask_prices[i]
                )
            )
            time.sleep(time_delay)


class OrderGenerator:

    def __init__(self, orderbook:OrderBook, price_history:PriceHistoryDB):
        self.orderbook = orderbook
        self.price_history = price_history
        self.security = orderbook.get_security()
        self.order_type = ['Market', 'Limit']
        self.order_direction = ['Buy', 'Sell']
        self.order_size = None

    def get_last_traded_price(self):
        return self.price_history.get_last_traded_price()
    
    def generate_market_order(self):
        direction = self.order_direction[0] if random.uniform(0, 1) <= 0.5 else self.order_direction[1]
        size = 1000
        security = self.security
        return MarketOrder(direction, size, security)
    
    def generate_limit_order(self):
        direction = self.order_direction[0] if random.uniform(0, 1) <= 0.5 else self.order_direction[1]
        size = 1000
        security = self.security
        mu = self.price_history.get_last_traded_price()
        sigma = self.price_history.get_total_volume() / self.price_history.get_trade_count()
        price_limit = random.normalvariate(mu, sigma)
        return LimitOrder(direction, size, price_limit, security)
    
    def set_order_type(self):
        return 'Market' if random.uniform(0, 1) <= 0.5 else 'Limit'
    


if __name__ == '__main__':

    book = OrderBook()
    primary_generator = PrimaryOrderGenerator(book, previous_close_price = 2230)
    primary_generator.generate_ask_side()
    primary_generator.generate_bid_side()
    book.display()
    db = PriceHistoryDB("AMZN")
    data = [2229, '12:15:01', [25, 54], 2000]
    db.insert_trade(data)
    data = [2230, '12:17:25', [4, 21], 4000]
    db.insert_trade(data)
    data = [2228, '13:27:00', [11, 10], 5000]
    db.insert_trade(data)
    
    me = MatchingEngine(book, db)
    book.display(display_size=5)
    m1 = MarketOrder("Buy", 1000, "AMZN")
    me.match_buy_market_order(m1)
    book.display(display_size=5)
    m2 = MarketOrder("Sell", 1000, "AMZN")
    me.match_sell_market_order(m2)
    book.display(display_size = 5)

    lb1 = LimitOrder(direction = 'Sell', size = 1000, price_limit = 2200.47, security = "AMZN")
    print(lb1.get_order_id())
    me.match_sell_limit_order(lb1)
    book.display(display_size = 5)

    avg_price = round((book.sort_price_time(bid_side=True)['Price_limit'].iloc[0] + book.sort_price_time(bid_side=True)['Price_limit'].iloc[1]) / 2,2)
    print(avg_price)

    lb2 = LimitOrder(direction='Sell', size=1000, price_limit=avg_price, security="AMZN")
    print(lb2.get_order_id())

    me.match_sell_limit_order(lb2)
    book.display(display_size=5)