import os
import pprint
from dotenv import load_dotenv
import ccxt
import pandas as pd
import time

#load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

exchange = ccxt.binance(config={
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True,  # Enable rate limit to avoid hitting API limits
    'options': {
        'defaultType': 'future'  # Use 'future' for Binance Futures, '
}})

markets = exchange.load_markets() # Load market data to get the list of coins from Binance Futures
tickers = exchange.fetch_tickers() # Fetch ticker data to get the current price of each coin
BTC_usdc = tickers['BTC/USDC:USDC']

balance = exchange.fetch_balance() # Fetch account balance to check available funds
usdc_balance = balance['USDC']['free'] # Get the free USDC balance
print(f"Current USDC Balance: {usdc_balance}")

