import ccxt
import time
import datetime
import threading
import pandas as pd
from time import sleep
import queue
from queue import Queue

class BinanceDataSaver:

    """Binance data saver"""

    def __init__(self, 
                 symbol='BTC/USDT', 
                 timeframe=None):
        self.exchange = ccxt.binance()
        self.markets = self.exchange.load_markets()
        self.symbol = symbol
        self.timeframe = timeframe


    def get_ticker(self):
        t = self.exchange.fetch_ticker(self.symbol)
        return t
    
    def get_tickers(self, end_time, queue):
        start = int(time.time()*1000)
        end = int(end_time.timestamp()*1000)
        data = []

        while start < end:
            t = self.exchange.fetch_ticker(self.symbol)
            data.append([t['timestamp'], t['ask'], t['askVolume'], t['bid'], t['bidVolume'], t['open'], t['high'], t['low'], t['close'], t['last']])
            timed = datetime.datetime.fromtimestamp(t['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f'tickers: {timed}')
            start = int(t['timestamp'])
            sleep(self.exchange.rateLimit / 1000)
        
        data = pd.DataFrame(data, columns=['datetime', 'ask', 'askVolume', 'bid', 'bidVolume', 'open', 'high', 'low', 'close', 'last'])
        data['datetime'] = pd.to_datetime(data['datetime'], unit='ms')
        data = data.set_index('datetime')
        data.to_csv(f'tickers.csv')
        queue.put(data)
    
    def get_depth(self):
        d = self.exchange.fetch_order_book(self.symbol, 10)
        return d
    
    def get_depths(self, end_time, queue):
        start = int(time.time()*1000)
        end = int(end_time.timestamp()*1000)
        data = []

        while start < end:
            d = self.exchange.fetch_order_book(self.symbol, 10)
            start = int(time.time()*1000)
            timed = datetime.datetime.fromtimestamp(start / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f'depths: {timed}')
            data.append([start, d['asks'], d['bids']])
            sleep(self.exchange.rateLimit * 5/ 1000)

        data = pd.DataFrame(data, columns=['datetime', 'asks', 'bids'])
        data['datetime'] = pd.to_datetime(data['datetime'], unit='ms')
        data = data.set_index('datetime')
        data.to_csv(f'depths.csv')
        queue.put(data)
    
    def get_ohlcv(self, start, end):
        """Fetch OHLCV data from Binance"""
        if self.exchange.has['fetchOHLCV']:
            data = []
            limit = 1000
            start_time = int(start.timestamp() * 1000)
            end_time = int(end.timestamp() * 1000)

            while start_time < end_time:
                # 设置获取时间段的起止时间
                fetch_since = start_time
                # print(fetch_since)
                print(datetime.datetime.fromtimestamp(fetch_since / 1000).strftime('%Y-%m-%d %H:%M:%S'))
                fetch_until = min(start_time + limit * 1000 * self.exchange.parse_timeframe(self.timeframe), end_time)

                # 获取数据
                raw_data = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, fetch_since, limit)

                # 处理数据
                for row in raw_data:
                    timestamp = int(row[0])
                    dt = datetime.datetime.utcfromtimestamp(timestamp / 1000)
                    data.append([dt, row[1], row[2], row[3], row[4], row[5]])

                # 更新起始时间
                start_time = fetch_until

                # 等待一段时间，避免过于频繁访问API
                sleep(self.exchange.rateLimit / 1000)

            # 将数据转换为DataFrame
            data = pd.DataFrame(data, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
            data['datetime'] = pd.to_datetime(data['datetime'], unit='ms')
            data = data.set_index('datetime')
            
        return data
    
    def get_trades(self, start, end):
        """Fetch trades data from Binance"""
        if self.exchange.has['fetchTrades']:
            data = []
            limit = 1000
            start_time = int(start.timestamp() * 1000)
            end_time = int(end.timestamp() * 1000)

            while start_time < end_time:
                # 设置获取时间段的起止时间
                fetch_since = start_time
                # print(fetch_since)
                print(datetime.datetime.fromtimestamp(fetch_since / 1000).strftime('%Y-%m-%d %H:%M:%S'))

                # 获取数据
                raw_data = self.exchange.fetch_trades(self.symbol, fetch_since, limit)

                # 处理数据
                for row in raw_data:
                    timestamp = int(row['info']['T'])
                    dt = datetime.datetime.utcfromtimestamp(timestamp / 1000)
                    data.append([dt, row['info']['p'], row['info']['q'], row['info']['m']])

                # 更新起始时间
                start_time = int(raw_data[-1]['info']['T'])

                # 等待一段时间，避免过于频繁访问API
                sleep(self.exchange.rateLimit / 1000)

            # 将数据转换为DataFrame
            data = pd.DataFrame(data, columns=['datetime', 'price', 'amount', 'side'])
            data['datetime'] = pd.to_datetime(data['datetime'], unit='ms')
            data = data.set_index('datetime')
            
        return data

    def saver(self, end_time):
        q_ticker = Queue()
        q_depth = Queue()
        ticker_thread = threading.Thread(target=self.get_tickers, args=(end_time, q_ticker))
        depth_thread = threading.Thread(target=self.get_depths, args=(end_time, q_depth))
        depth_thread.start()
        ticker_thread.start()
        ticker_thread.join()
        depth_thread.join()
        tickers = q_ticker.get()
        depths = q_depth.get()
        return tickers, depths


if __name__ == '__main__':
    symbol = 'BTC/USDT'
    bot = BinanceDataSaver(symbol)
    start = datetime.datetime(2023, 5, 18, 13, 27, 18)
    end = datetime.datetime(2023, 5, 18, 13, 43, 0)
    # t, d = bot.saver(end)
    # print(t)
    # print(d)
    trades = bot.get_trades(start, end)
    trades.to_csv('trades.csv')
    print(trades)