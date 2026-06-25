import os
import sys
import pandas as pd
from dotenv import load_dotenv
import ccxt

# 1. Load credentials from your .env file
load_dotenv()
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

ticker = 'BTC/USDC:USDC'
print(f"Initializing Flat Test Script for {ticker}...")

# 2. Configure CCXT for Binance Futures directly
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'  # Explicitly routes requests to Futures API
    }
})

# ⚠️ UNCOMMENT THE LINE BELOW IF YOU ARE TESTING WITH BINANCE FUTURES TESTNET KEYS:
# exchange.set_sandbox_mode(True)

# 3. Connection and Authentication Verification Block
try:
    print("Syncing exchange market pairs and validating API Credentials...")
    exchange.load_markets()
    print("API credentials valid. Successfully connected to market pair endpoints.")
except ccxt.AuthenticationError as e:
    print("\n[CRITICAL] Binance rejected your credentials.")
    print("Reason: Ensure your .env keys have no literal quotes (\"), no spaces, and match the selected network environment (Live vs Testnet).")
    sys.exit(1)
except Exception as e:
    print(f"\n[CRITICAL] Connection failed: {e}")
    sys.exit(1)

# 4. Fetch Margin Account Balance
try:
    print("\nChecking Account Balance...")
    balance = exchange.fetch_balance()
    
    # Safely look up free USDC balance
    usdc_balance = balance.get('USDC', {}).get('free', 0.0)
    print(f" -> Success! Available Margin Balance: {usdc_balance:,.2f} USDC")
except Exception as e:
    print(f" -> Error reading balance data: {e}")

# 5. Fetch Historical Market Data (OHLCV)
try:
    print("\nFetching historical 30-minute market data...")
    raw_ohlcv = exchange.fetch_ohlcv(ticker, timeframe='30m', limit=400)
    
    # Process into an easily readable DataFrame
    columns = ["timestamp", "open", "high", "low", "close", "volume"]
    ohlcv_df = pd.DataFrame(raw_ohlcv, columns=columns)
    
    print(f" -> Success! Retrieved {len(ohlcv_df)} candles.")
    print("Recent Price Stream Slices:")
    print(ohlcv_df[['timestamp', 'open', 'close', 'volume']].tail(5))
except Exception as e:
    print(f" -> Error fetching market candle data matrices: {e}")

# 6. Fetch Live Real-Time Ticker Info
try:
    print("\nFetching immediate live price tick...")
    tickers = exchange.fetch_tickers()
    current_live_price = tickers[ticker]['last']
    print(f" -> Success! Current Live {ticker} Price: ${current_live_price:,.2f}")
except Exception as e:
    print(f" -> Error reading live price tickers: {e}")