# -*- encoding: utf-8 -*-
'''
@File    :   orderbook.py
@Time    :   2023/06/12 22:25:26
@Author  :   Claysome 
@Contact :   claysomes@outlook.com
'''

import os
import time
import numpy as np
import pandas as pd
from tabulate import tabulate
pd.options.display.max_columns = None


class OrderBook:
    columns = ['Order ID', 'Order_type', 'Direction', 'Size', 'Price_limit', 'Security', 'Status', 'Arrival_time']

    def __init__(self, security:str="AMZN"):
        self.security = security
        self.bid_side = {}
        self.ask_side = {}

    def get_security(self):
        return self.security
    
    def insert_order(self, order):
        order_id = order.get_order_id()
        order_direction = order.get_direction()
        if order_direction == 'Sell':
            if order_id not in self.ask_side.keys():
                self.ask_side[order_id] = order
            else:
                raise Exception("Order already in the order book.")
        else:
            if order_id not in self.bid_side.keys():
                self.bid_side[order_id] = order
            else:
                raise Exception("Order already in the order book.")

    def pop_order(self, order_id:int=None):
        if order_id in self.bid_side.keys():
            return self.bid_side.pop(order_id)
        else:
            return self.ask_side.pop(order_id)
        
    def to_dataframe(self, bid_side:bool=True):
        book_size = self.bid_side if bid_side else self.ask_side
        order_series = [order.to_series() for order in book_size.values()]
        return pd.concat(objs=order_series, axis=1).T.set_index(keys='Order ID')
    
    def sort_price_time(self, bid_side:bool=True):
        """
        价格-时间优先排序的订单簿，没有订单聚合。
        返回一个数据表格，其中最好的出价或报价在数据框架的顶部。
        """
        if bid_side:
            return self.to_dataframe(bid_side).sort_values(
                axis=0,
                by=['Price_limit', 'Arrival_time'],
                ascending=[False, True]
            )
        else:
            return self.to_dataframe(bid_side).sort_values(
                axis=0,
                by=['Price_limit', 'Arrival_time'],
                ascending=[True, True]
            )
        
    def get_aggregate_size(self, bid_side:bool=True):
        return self.to_dataframe(bid_side)['Size'].sum(axis=0)

    def display(self, display_size:int=5):
        display_columns = ['Security', 'Direction', 'Price_limit', 'Size',
                           'Aggregate_size', 'Arrival_time']
        # 订单簿
        book_ask_side = self.to_dataframe(bid_side=False)
        book_bid_side = self.to_dataframe(bid_side=True)
        # 排队
        book_ask_side.sort_values(
            axis=0,
            by=['Price_limit', 'Arrival_time'],
            ascending=[True, True],
            inplace=True
        )
        book_bid_side.sort_values(
            axis=0,
            by=['Price_limit', 'Arrival_time'],
            ascending=[False, True],
            inplace=True
        )
        # 聚合
        book_ask_side['Aggregate_size'] = book_ask_side['Size'][::-1].cumsum(axis=0)[::-1]
        book_bid_side['Aggregate_size'] = book_bid_side['Size'].cumsum(axis=0)

        sep_series = pd.Series(data = [' ' for _ in range(len(book_ask_side.columns))], 
                               index = book_ask_side.columns, name = '')
        
        sep_frame = sep_series.to_frame().transpose()
        
        entire_book = pd.concat([book_ask_side.iloc[-display_size:][::-1], sep_frame, book_bid_side.iloc[:display_size]]).rename_axis(index = 'Order ID')
        print('\n')
        # print(entire_book)
        print(tabulate(entire_book[display_columns], headers = display_columns,
                        tablefmt = 'fancy_grid', stralign = 'center'))


if __name__ == '__main__':
    import order
    T = 10**(-6)    
    m1 = order.MarketOrder(direction = 'Sell', size = 3000, security = "AMZN")    
    lb1 = order.LimitOrder(direction = 'Buy', size = 500, price_limit = 1600, security = "AMZN")
    time.sleep(T)
    lb2 = order.LimitOrder(direction = 'Buy', size = 100, price_limit = 1700, security = "AMZN")
    time.sleep(T)
    lb3 = order.LimitOrder(direction = 'Buy', size = 3000, price_limit = 1750, security = "AMZN")
    time.sleep(T)
    lb4 = order.LimitOrder(direction = 'Buy', size = 1500, price_limit = 1750, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    lb5 = order.LimitOrder(direction = 'Buy', size = 1500, price_limit = 1750, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls1 = order.LimitOrder(direction = 'Sell', size = 1500, price_limit = 2000, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls2 = order.LimitOrder(direction = 'Sell', size = 10000, price_limit = 1800, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls3 = order.LimitOrder(direction = 'Sell', size = 70, price_limit = 1800, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls4 = order.LimitOrder(direction = 'Sell', size = 900, price_limit = 1760, security = "AMZN")
    book = OrderBook()
    time.sleep(T)
    ls5 = order.LimitOrder(direction = 'Sell', size = 900, price_limit = 1760, security = "AMZN")
    book = OrderBook()
    for i in [lb1, lb2, lb3, lb4, lb5, ls1, ls2, ls3, ls4, ls5]:
        book.insert_order(i)
    book.display()