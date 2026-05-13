import Binance_link

BinanceLink = Binance_link.BinanceLink() # Create an instance of the BinanceLink class to connect to the API
t = input("Enter the ticker symbol (e.g., BTC/USDC:USDC): ") # Prompt user to enter the ticker symbol for the desired market
print(BinanceLink.get_market_data(t))   # Fetch and print the market data for the specified ticker

