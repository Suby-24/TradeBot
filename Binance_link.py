import os
import pprint
from dotenv import load_dotenv
import ccxt



# Class for connecting to Binance Futures API and fetching market data and account balance 
class BinanceLink:
    def __init__(self):
        #load environment variables from .env file
        load_dotenv()
        # Get API keys from environment variables
        API_KEY = os.getenv('BINANCE_API_KEY')
        SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
        self.exchange = ccxt.binance(config={
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'enableRateLimit': True,  # Enable rate limit to avoid hitting API limits
            'options': {
                'defaultType': 'future'  # Use 'future' for Binance Futures, '
        }})
        markets = self.exchange.load_markets() # Load market data to get the list of coins from Binance Futures
    
    def get_market_data(self,ticker):
        tickers = self.exchange.fetch_tickers() # Fetch ticker data to get the current price of each coin
        BTC_usdc = tickers[ticker] #e.g.) BTC/USDC:USDC is the ticker symbol for the BTC/USDC perpetual contract on Binance Futures
        return BTC_usdc
    
    def get_balance(self):
        balance = self.exchange.fetch_balance() # Fetch account balance to check available funds
        usdc_balance = balance['USDC']['free'] # Get the free USDC balance
        return usdc_balance 

    def get_current_price(self, ticker):
        tickers = self.exchange.fetch_tickers() # Fetch ticker data to get the current price of each coin
        current_price = tickers[ticker]['last'] # Get the last price of the specified ticker
        return current_price





