import Binance_link
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import time

class BinanceData:
    def __init__(self, ticker):
        self.binance_link = Binance_link.BinanceLink() # Create an instance of the BinanceLink class to connect to the API
        self.ticker = ticker # Store the ticker symbol for which to fetch data (e.g., 'BTC/USDC:USDC' for the BTC/USDC perpetual contract on Binance Futures)
    
    def check_open_signal(self, ohlcv):
         return ohlcv
    
    def check_close_signal(self, ohlcv):
        # Process the OHLCV data as needed (e.g., convert timestamps, calculate indicators, etc.)
        # This is a placeholder function and can be customized based on specific requirements
        return ohlcv
    
    def set_tp(self, ohlcv):
        # Evaluate the processed OHLCV data to determine if there are any open or close signals for trading
        # This is a placeholder function and can be customized based on specific requirements
        return ohlcv
    
    def set_sl(self, ohlcv):
        # Evaluate the processed OHLCV data to determine if there are any open or close signals for trading
        # This is a placeholder function and can be customized based on specific requirements
        return ohlcv

    def fetch_data(self):
        if self.binance_link.exchange.has['fetchOHLCV']: # Check if the exchange supports fetching OHLCV data
            position = [] # List to store outcome of processed OHLCV data for each timeframe whether it is 
            ohlcv = self.binance_link.exchange.fetch_ohlcv(self.ticker, timeframe='12h', limit = 300) # Fetch OHLCV data for the specified ticker and timeframe (e.g., 15 minutes)                     ohlcv = self.binance_link.exchange.fetch_ohlcv(self.ticker, timeframe='30m', limit = 400)
            return ohlcv
            """
            ohlcv = self.binance_link.exchange.fetch_ohlcv(self.ticker, timeframe='1h', limit = 300)
            ohlcv = self.binance_link.exchange.fetch_ohlcv(self.ticker, timeframe='4h', limit = 200) # Fetch OHLCV data for the specified ticker and timeframe (e.g., 4 hours)
            ohlcv = self.binance_link.exchange.fetch_ohlcv(self.ticker, timeframe='6h', limit = 150) # Fetch OHLCV data for the specified ticker and timeframe (e.g., 6 hours)
            ohlcv = self.binance_link.exchange.fetch_ohlcv(self.ticker, timeframe='12h', limit = 100) # Fetch OHLCV data for the specified ticker and timeframe (e.g., 12 hours)
            ohlcv = self.binance_link.exchange.fetch_ohlcv(self.ticker, timeframe='1d', limit = 50) # Fetch OHLCV data for the specified ticker and timeframe (e.g., 1 day)
            """    



