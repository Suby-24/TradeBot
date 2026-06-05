import Binance_link
import Binance_data

def main():
    ticker = 'BTC/USDC:USDC' # Specify the ticker symbol for which to fetch data (e.g., 'BTC/USDC:USDC' for the BTC/USDC perpetual contract on Binance Futures)
    binance_data = Binance_data.BinanceData(ticker) # Create an instance of the BinanceData class to manage data fetching and processing
    binance_data.fetch_data() # Fetch and process the market data for the specified ticker


if __name__ == "__main__":
    main()