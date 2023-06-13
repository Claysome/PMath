#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   price_history.py
@Time    :   2023/06/13 13:56:01
@Author  :   Clay
'''

# 
# Place on MongoDB
# 
import numpy as np
import pandas as pd


class PriceHistoryDB:
    columns = ["Trade_price", "Execution_time", "Matched_orders", "Size"]

    def __init__(self, security:str="AMZN"):
        self.security = security
        self.price_history = pd.DataFrame(columns=self.columns)

    def insert_trade(self, trade_data):
        trade_details = pd.DataFrame(
            data=np.array(trade_data).reshape((1,4)),
            columns=self.columns
        )
        self.price_history = pd.concat([self.price_history, trade_details], ignore_index=True)
    
    def get_last_traded_price(self):
        return self.price_history.iloc[-1]['Trade_price']
    
    def get_trade_count(self):
        return self.price_history.shape[0]
    
    def get_price_history(self, execution_time_index:bool=True):
        if execution_time_index:
            return self.price_history.set_index(keys=['Execution_time'])['Trade_price']
        else:
            return self.price_history['Trade_price']
    
    def get_total_volume(self):
        return self.price_history['Size'].sum()
    

if __name__ == '__main__':
    db = PriceHistoryDB()
    data = [100, '12:15:01', [25, 54], 2000]
    db.insert_trade(data)
    data = [125, '12:17:25', [4, 21], 4000]
    db.insert_trade(data)
    data = [110, '13:27:00', [11, 10], 5000]
    db.insert_trade(data)
    print(db.price_history)   