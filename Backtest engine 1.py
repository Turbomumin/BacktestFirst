import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def stockdata(tickers, startdate, enddate):
    # Download data for multiple tickers, ensure the group_by ticker to structure data by ticker
    stocks = yf.download(tickers, start=startdate, end=enddate, group_by='ticker')
    return stocks

def SMA(stockdata, period):
    return stockdata.rolling(window=period).mean()
def crossover(data1, data2):
    return data1 > data2
def crossunder(data1, data2):
    return data1 < data2

def apply_trading_system(stock, ticker, operation_money, costs, enter_pos, exit_pos, direction):
    ticker_data = stock[ticker].copy()
    sma30 = SMA(ticker_data['Close'], 30)
    sma200 = SMA(ticker_data['Close'], 200)

    # Update signals based on trading direction
    enter_pos, exit_pos = update_signals(sma30, sma200, direction)

    # Market positions: 1 for entered, 0 for not in position
    ticker_data['market_position'] = 0
    ticker_data.loc[enter_pos, 'market_position'] = 1
    ticker_data.loc[exit_pos, 'market_position'] = 0
    ticker_data['market_position'] = ticker_data['market_position'].ffill().fillna(0)

    # Only consider entries not currently in a position (THIS IS WHERE PROBLEM IS!!!)
    adjusted_enter_pos = enter_pos & (ticker_data['market_position'].shift(1) == 0)

# Set entry price to close price when market pos switches from 0 to 1, fill this entry price until market pos turns back to 0
    ticker_data['entry_price'] = np.where(
        (ticker_data['market_position'] == 1) & (ticker_data['market_position'].shift(1) == 0),
        ticker_data['Close'],
        np.nan
    )
    ticker_data['entry_price'] = ticker_data['entry_price'].ffill().fillna(0) # Returns 0 when NaN is found otherwise forward fill

# Set exit price to close price when market pos switches from 1 to 0
    ticker_data['exit_price'] = np.where(
        (ticker_data['market_position'] == 1) & (ticker_data['market_position'].shift(-1) == 0),
        ticker_data['Close'],
        np.nan
    )
    if ticker_data['market_position'].iloc[-1] == 1:
        ticker_data['exit_price'].iloc[-1] = ticker_data['Close'].iloc[-1]

    ticker_data['exit_price'] = ticker_data['exit_price'].fillna(0) # Returns 0 when NaN is found otherwise forward fill

    # Compute positions and operations
    compute_positions_and_operations(ticker_data, adjusted_enter_pos, exit_pos, operation_money, costs)
    print(ticker_data)
    # Visualize trading data and SMAs, this will be altered when system is adapted for 1000s of stocks
    # plot_trading_signals(ticker_data, sma30, sma200, ticker)

    return ticker_data['closed_equity']

# This def is unused as of now, it exists purely for debugging
def log_signals(data, enter_pos, exit_pos, message):
    print(f"\n{message}")
    print(f"Enter signals on: {data.loc[enter_pos].index.tolist()}")
    print(f"Exit signals on: {data.loc[exit_pos].index.tolist()}")

# This def is unused as of now, also a part of debugging
def debug_price_changes(data, enter_pos, exit_pos):
    entry_data = data.loc[enter_pos, 'entry_price']
    exit_data = data.loc[exit_pos, 'exit_price']
    print("\nEntry Prices at Signal Points:")
    for date, price in entry_data.dropna().items():
        print(f"Entry on {date.strftime('%Y-%m-%d')}: {round(price,2)}")
    print("\nExit Prices at Signal Points:")
    for date, price in exit_data.dropna().items():
        print(f"Exit on {date.strftime('%Y-%m-%d')}: {round(price,2)}")

# Defines long and short strategies, will require further testing
def update_signals(sma30, sma200, direction):
    if direction == 'long':
        enter_pos = crossover(sma30, sma200)
        exit_pos = crossunder(sma30, sma200)
    else:  # Assuming 'short'
        enter_pos = crossunder(sma30, sma200)
        exit_pos = crossover(sma30, sma200)
    return enter_pos, exit_pos

# adjusted_enter_pos and exit_pos are being unused in the def right now, I need to change this in future updates
def compute_positions_and_operations(ticker_data, adjusted_enter_pos, exit_pos, operation_money, costs):
    ticker_data['number_of_stocks'] = operation_money / ticker_data['entry_price'].fillna(0) # Amount of stocks purchased at enter_pos is calculated and filled down
    ticker_data['number_of_stocks'].replace([np.inf, -np.inf], 0, inplace=True) # Replace inf with 0 (happens when entry price is 0)
    ticker_data['number_of_stocks'] = np.floor(ticker_data['number_of_stocks'])  # Round down to nearest integer
    
    # Initialize operations
    ticker_data['operations'] = 0  # Set all initial operations to 0

    # Determine the rows where market position changes from 1 to 0 or it's the last row in the DataFrame
    last_entries = (ticker_data['market_position'].shift(-1) == 0) & (ticker_data['market_position'] == 1)
    if not ticker_data['market_position'].iloc[-1] == 0:
        last_entries.iloc[-1] = True  # Set the last row to True if market position is 1

    # Calculate operations only for these specific last entries
    ticker_data.loc[last_entries, 'operations'] = (
        ticker_data['exit_price'] - ticker_data['entry_price']) * ticker_data['number_of_stocks'] * (1 - costs)
    
    # Cumulative sum of operations to track closed equity
    ticker_data['closed_equity'] = ticker_data['operations'].cumsum()

    return ticker_data

# Def which outlines stock prices and SMAs, will be reconfigured in future versions so it is more versatile
def plot_trading_signals(ticker_data, sma30, sma200, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(ticker_data['Close'], label='Close')
    plt.plot(sma30, label='30-day SMA', linestyle='--')
    plt.plot(sma200, label='200-day SMA', linestyle='--')
    plt.title(f"{ticker} Close vs. SMAs")
    plt.legend()
    plt.show()

def apply_trading_system_to_portfolio(tickers):
    results = {}
    enddate = datetime.now() - timedelta(days=90) # Strategy stops 90 days earlier than current date
    startdate = enddate - timedelta(days=3000) # Strategy starts 3000 days earlier than end date, meaning strategy rolls for a total of 3000 days

    # Fetch data for all tickers at once, avoids pushing request limit of yfinance
    stocks = stockdata(tickers, startdate, enddate)

    for ticker in tickers:
        sma30 = SMA(stocks[ticker]['Close'], 30)
        sma200 = SMA(stocks[ticker]['Close'], 200)
        enter_pos = crossover(sma30, sma200)
        exit_pos = crossunder(sma30, sma200)

        # Parameters
        operation_money = 10000 # Right now an investment of 10000 is made in each enter_pos, this will change as I want it to be more fluid
        costs = 0.002 # Set as decimal, right now 2% of price
        direction = 'long' # Set as 'long' or 'short'

        trading_system = apply_trading_system(stocks, ticker, operation_money, costs, enter_pos, exit_pos, direction)
        results[ticker] = trading_system

    # Combine results for all tickers into a single DataFrame
    portfolio_equity = pd.DataFrame(results)
    portfolio_equity['Total Equity'] = portfolio_equity.sum(axis=1)
    return portfolio_equity

if __name__ == "__main__":
    # Right now it will analyse only these two tickers, in the final version it will be changed to analyse all stock tickers available
    tickers = ['AAPL', 'GOOGL']
    
    portfolio_results = apply_trading_system_to_portfolio(tickers)
    portfolio_results.to_csv('portfolio_equity.csv')

    # Chart which shows portfolio equity over time, should be primarly used for analysis and debugging reasons.
    # Chart will be changed to be more versatile. Total portfolio equity will be given as a chart of market value of both invested and liquidated capital
    plt.figure(figsize=(14, 7))
    plt.plot(portfolio_results['Total Equity'], label='Total Portfolio Equity')
    plt.title('Portfolio Equity Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Equity')
    plt.legend()
    plt.grid(True)
    plt.show()
    print(portfolio_results)
