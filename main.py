import pandas as pd
import time
import sys

# Import all your custom project files/classes
from Binance_link import BinanceLink
from Binance_data import BinanceData
from Binance_logic import BinanceLogic  # Matching class name from Binance_logic.py
import draw

def main():
    # ==========================================
    # 1. INITIALIZATION & SETUP
    # ==========================================
    ticker = 'BTC/USDC:USDC'
    print(f"Initializing Suby Bot Core for {ticker}...")
    
    # Instantiate the data fetching module
    binance_data = BinanceData(ticker)
    
    # = "binance_data" internally creates an instance of BinanceLink, 
    #   but we can also reference it directly to check account balances or live tickers.
    exchange_link = binance_data.binance_link

    try:
        # Check initial connectivity and account balance
        balance = exchange_link.get_balance()
        print(f"Connected successfully. Available Margin Balance: {balance:,.2f} USDC")
    except Exception as e:
        print(f"API Connection Error: {e}")
        print("Ensure your .env file contains valid BINANCE_API_KEY and BINANCE_SECRET_KEY.")
        sys.exit(1)

    # ==========================================
    # 2. DATA INGESTION & FORMATTING
    # ==========================================
    print("\nFetching historical candle market matrices...")
    # Fetch data (This calls fetch_ohlcv and auto-saves to local storage csv)
    raw_ohlcv = binance_data.fetch_data()
    
    if raw_ohlcv is None or len(raw_ohlcv) == 0:
        print("CRITICAL ERROR: No market data retrieved from exchange.")
        return

    # Convert the raw CCXT nested list structure into the proper Pandas DataFrame format 
    # expected by Binance_Logic
    columns = ["timestamp", "open", "high", "low", "close", "volume"]
    ohlcv_df = pd.DataFrame(raw_ohlcv, columns=columns)
    
    # Ensure standard data types are fully supported across mathematical slices
    ohlcv_df = ohlcv_df.astype({
        'open': 'float64', 'high': 'float64', 'low': 'float64', 
        'close': 'float64', 'volume': 'float64'
    })

    # ==========================================
    # 3. QUANTITATIVE ANALYSIS PIPELINE
    # ==========================================
    print("Instantiating analytical model parameters...")
    # Feed formatted dataframe container directly into your logic module
    bot_brain = BinanceLogic(ohlcv_dataframe=ohlcv_df)

    print("Running sequential time-series engine to build inflection points...")
    inflection_points = bot_brain.calc_inflection_points()

    print("Constructing adaptive support and resistance structural boxes...")
    trend_lines = bot_brain.construct_boxes()
    print(f"Active Historical Levels Identified: {trend_lines}")

    # ==========================================
    # 4. LIVE EXECUTION SCAN
    # ==========================================
    print("\nFetching real-time price tick and running execution scanning...")
    try:
        # Pull the absolute last live trade price directly via CCXT tickers
        current_live_price = exchange_link.get_current_price(ticker)
        print(f"Live Market Price Anchor: ${current_live_price:,.2f}")
        
        # Scan volume environment and positions relative to boxes to generate signals
        trade_signal = bot_brain.check_trade_opportunity(
            current_price=current_live_price, 
            trend_lines=trend_lines
        )
        print(f"Current Pipeline Output Signal: {trade_signal}")
        
    except Exception as e:
        print(f"Error handling live data matching loop: {e}")

    # ==========================================
    # 5. CHARTS & VISUALIZATION
    # ==========================================
    print("\nLaunching visualization workspace engine...")
    try:
        # Pass computed matrices straight into your interactive Plotly canvas
        draw.plot_inflection_points(
            inflection_list=inflection_points, 
            ohlcv_df=ohlcv_df, 
            horizontal_lines_list=trend_lines
        )
    except Exception as e:
        print(f"Visual rendering step skipped: {e}")

if __name__ == "__main__":
    main()