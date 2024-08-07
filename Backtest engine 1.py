import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def stockdata(tickers, startdate, enddate):
    # Download data for multiple tickers, only 'close' prices are downloaded to speed up processing and reduce unnecessary computations
    stocks = yf.download(tickers, start=startdate, end=enddate)['Close']
    stocks.columns = pd.MultiIndex.from_product([[ticker for ticker in tickers], ['Close']], names=['Ticker', None])
    print("Stocks have been downloaded")
    return stocks

def SMA(stockdata, period):
    return stockdata.rolling(window=period).mean()
def crossover(data1, data2):
    return data1 > data2
def crossunder(data1, data2):
    return data1 < data2

def apply_trading_system(stocks, ticker, initial_capital, costs, enter_pos, exit_pos, direction):
    ticker_data = stocks[ticker].copy()
    sma30 = SMA(ticker_data['Close'], 30)
    sma200 = SMA(ticker_data['Close'], 200)

    # Update signals based on the trading direction
    enter_pos, exit_pos = update_signals(sma30, sma200, direction)

    # Market positions: 1 for entering, 0 for not in position
    ticker_data['market_position'] = 0
    ticker_data.loc[enter_pos, 'market_position'] = 1
    ticker_data.loc[exit_pos, 'market_position'] = 0
    ticker_data['market_position'] = ticker_data['market_position'].ffill().fillna(0)

# Set entry price to close price when market pos switches from 0 to 1, fill this entry price until market pos turns back to 0
    ticker_data['entry_price'] = np.where(
        (ticker_data['market_position'] == 1) & (ticker_data['market_position'].shift(1) == 0),
        ticker_data['Close'],
        np.nan
    )
    ticker_data['entry_price'] = ticker_data['entry_price'].ffill().fillna(0) # Returns 0 when NaN is found otherwise forward fill

# Set exit price to close price when market pos switch from 1 to 0
    ticker_data['exit_price'] = np.where(
        (ticker_data['market_position'] == 1) & (ticker_data['market_position'].shift(-1) == 0),
        ticker_data['Close'],
        np.nan
    )
    if ticker_data['market_position'].iloc[-1] == 1:
        ticker_data['exit_price'].iloc[-1] = ticker_data['Close'].iloc[-1]

    ticker_data['exit_price'] = ticker_data['exit_price'].fillna(0) # Returns 0 when NaN is found otherwise forward fill

    # Compute positions and operations
    print(ticker_data)
    compute_positions_and_operations(ticker_data, initial_capital, costs)
    print(f'Data received and calculated for ticker {ticker}') # Print which provides a quick checkup of progress

    return ticker_data['Balance']

# Buy/Sell defined for long and short strategies
def update_signals(sma30, sma200, direction):
    if direction == 'long':
        enter_pos = crossover(sma30, sma200)
        exit_pos = crossunder(sma30, sma200)
    else:  # Assuming 'short'
        enter_pos = crossunder(sma30, sma200)
        exit_pos = crossover(sma30, sma200)
    return enter_pos, exit_pos

def compute_positions_and_operations(ticker_data, initial_capital, costs):
    # Initialize the four different columns
    ticker_data['Shares_owned'] = 0
    ticker_data['Invested'] = 0
    ticker_data['Uninvested'] = initial_capital
    ticker_data['Balance'] = initial_capital # Both 'Uninvested' and 'Balance' are set initially to initial capital

    # Iterate Over Rows
    for i in range(len(ticker_data)):
        current_row = ticker_data.iloc[i]

        if i == 0:
            # Skip the first row since there is no previous row
            continue
        
        # Introduce a modified dataframe that consists of the last row for each instance
        previous_row = ticker_data.iloc[i - 1]

        # Action if no buy signal is detected
        if (current_row['market_position'] == 0) and (previous_row['market_position'] == 0):
            ticker_data.at[ticker_data.index[i], 'Shares_owned'] = 0
            ticker_data.at[ticker_data.index[i], 'Uninvested'] = previous_row['Balance']
            ticker_data.at[ticker_data.index[i], 'Invested'] = ticker_data.at[ticker_data.index[i], 'Shares_owned'] * ticker_data.at[ticker_data.index[i], 'Close']
            ticker_data.at[ticker_data.index[i], 'Balance'] = ticker_data.at[ticker_data.index[i], 'Invested'] + ticker_data.at[ticker_data.index[i], 'Uninvested']
        # Action if a buy signal is detected
        elif (current_row['market_position'] == 1) and (previous_row['market_position'] == 0):
            ticker_data.at[ticker_data.index[i], 'Shares_owned'] = previous_row['Balance'] / current_row['entry_price']
            ticker_data.at[ticker_data.index[i], 'Shares_owned'] = np.floor(ticker_data.at[ticker_data.index[i], 'Shares_owned'])  # Floor returns the largest integer where i <= x, i.e. the largest whole number 
            ticker_data.at[ticker_data.index[i], 'Invested'] = ticker_data.at[ticker_data.index[i], 'Shares_owned'] * ticker_data.at[ticker_data.index[i], 'Close']
            ticker_data.at[ticker_data.index[i], 'Uninvested'] = previous_row['Balance'] - ticker_data.at[ticker_data.index[i], 'Invested']
            ticker_data.at[ticker_data.index[i], 'Balance'] = ticker_data.at[ticker_data.index[i], 'Invested'] + ticker_data.at[ticker_data.index[i], 'Uninvested']
        # Action if no sell signal is detected
        elif (current_row['market_position'] == 1) and (previous_row['market_position'] == 1):
            ticker_data.at[ticker_data.index[i], 'Shares_owned'] = previous_row['Shares_owned']
            ticker_data.at[ticker_data.index[i], 'Uninvested'] = previous_row['Uninvested']
            ticker_data.at[ticker_data.index[i], 'Invested'] = ticker_data.at[ticker_data.index[i], 'Shares_owned'] * ticker_data.at[ticker_data.index[i], 'Close']
            ticker_data.at[ticker_data.index[i], 'Balance'] = ticker_data.at[ticker_data.index[i], 'Invested'] + ticker_data.at[ticker_data.index[i], 'Uninvested']
        # Action if a sell_signal is detected
        elif (current_row['market_position'] == 0) and (previous_row['market_position'] == 1):
            ticker_data.at[ticker_data.index[i], 'Shares_owned'] = 0
            ticker_data.at[ticker_data.index[i], 'Uninvested'] = previous_row['Balance']
            ticker_data.at[ticker_data.index[i], 'Invested'] = ticker_data.at[ticker_data.index[i], 'Shares_owned'] * ticker_data.at[ticker_data.index[i], 'Close']
            ticker_data.at[ticker_data.index[i], 'Balance'] = ticker_data.at[ticker_data.index[i], 'Invested'] + ticker_data.at[ticker_data.index[i], 'Uninvested']
        
        # Update Balance to reflect transaction costs
        ticker_data.at[ticker_data.index[i], 'Balance'] = ticker_data.at[ticker_data.index[i], 'Shares_owned'] * current_row['Close'] * (1 - costs) + ticker_data.at[ticker_data.index[i], 'Uninvested']

        # Handle last row to sell remaining shares
        if i == len(ticker_data) - 1:
            # Sell all remaining shares at the current price
            ticker_data.at[ticker_data.index[i], 'Balance'] = ticker_data.at[ticker_data.index[i], 'Shares_owned'] * current_row['Close'] * (1 - costs) + ticker_data.at[ticker_data.index[i], 'Uninvested']
            ticker_data.at[ticker_data.index[i], 'Shares_owned'] = 0
            ticker_data.at[ticker_data.index[i], 'Uninvested'] = ticker_data.at[ticker_data.index[i], 'Balance']

    return ticker_data

def metriccalc(portfolio_equity, startdate, enddate):
    #TODO: Fix Vol so that it can work even if there arent 365d to calculate with
    portfolio_equity['Vol'] = portfolio_equity['Total Equity'].rolling(window=365).std() / portfolio_equity['Total Equity'] # Timeperiod for volatility is now 365d, might change since I need to research the timeperiod choice of volatility calcs.
    portfolio_equity['Benchmark_Index'] = yf.download('^GSPC', start=startdate, end=enddate)['Close'] # Downloads the SP500 index as benchmark to the dataframe
    # Loop that calculates the metrics for each stock ticker
    for ticker in tickers:
        portfolio_equity[f'{ticker}_return'] = (portfolio_equity[ticker] / portfolio_equity[ticker].shift(1))-1 # Calculate daily returns of stocks
        portfolio_equity['Benchmark_return'] = (portfolio_equity['Benchmark_Index'] / portfolio_equity['Benchmark_Index'].shift(1))-1 # Calculate daily returns of benchmark
        portfolio_equity[f'{ticker}_weight'] = portfolio_equity[ticker] / portfolio_equity['Total Equity'] # Calculate asset weights for each individual day
        portfolio_equity[f'{ticker}_weighted_beta'] = (portfolio_equity[f'{ticker}_return'].rolling(window=365).cov(portfolio_equity['Benchmark_return']) / portfolio_equity['Benchmark_return'].rolling(window=365).var()) * portfolio_equity[f'{ticker}_weight'] # Calculate daily weighted asset betas
    # Calculate daily portfolio beta
    portfolio_equity['Beta'] = sum(
        portfolio_equity[f'{ticker}_weighted_beta'] for ticker in tickers
    )

    return portfolio_equity

def yearly_total_equity_change(group):
    start_value = group['Total Equity'].iloc[0] # First value in a given year
    end_value = group['Total Equity'].iloc[-1] # Latest value in a given year
    return ((end_value - start_value) / start_value) if start_value !=0 else float('inf') # Percentage change in value

def summaryscreen(portfolio_equity, startdate, enddate):
    pre_summary = portfolio_equity

    # Retrive daily riskfree rate and calculate daily returns
    pre_summary['RF'] = yf.download('^IRX', start=startdate, end=enddate)['Close'] # Retreive riskfree rate from yfinance
    # List of different RF tickers for use: ^IRX: 13 WEEK TREASURY BILL, ^FVX: TREASURY YIELD 5 YEAR, ^TYX: TREASURY YIELD 30 YEAR

    # Isolate the year of each datapoint and calculate the mean of each year
    pre_summary.index = pd.to_datetime(pre_summary.index) # Convert the date index to datetime
    pre_summary['Year'] = pre_summary.index.year # Exctract year from each row
    summary = pre_summary.groupby('Year').mean() # Calculate mean of each column of each year except for value Total Equity

    # Calculate the change in equity per year
    percent_change_per_year = pre_summary.groupby('Year').apply(yearly_total_equity_change) # Calculate change in equity
    summary['Return%'] = percent_change_per_year * 100 # Merge with summary dataframe

    # Calculate Sharpe-Ratio
    summary['Sharpe'] = ((summary['Return%']/100) - (summary['RF']/100)) / summary['Vol']

    # Remove unnecessary columns
    columns_to_keep = ['Beta',  'Vol', 'RF', 'Return%', 'Sharpe']
    summary = summary.drop(columns=[col for col in summary.columns if col not in columns_to_keep])

    # Print summary resulting dataframe and return it
    summary = summary.round(2) # Round the values to two decimals
    print(summary)
    return summary

def apply_trading_system_to_portfolio(tickers):
    results = {}
    enddate = datetime.now() - timedelta(days=90) # Testing stops 90 days earlier than current date
    startdate = enddate - timedelta(days=3000) # Testing starts 3000 days earlier than the end date, meaning strategy rolls for a total of 3000 days

    # Fetch data for all tickers at once, avoids pushing the request limit of yfinance
    stocks = stockdata(tickers, startdate, enddate)

    for ticker in tickers:
        sma30 = SMA(stocks[ticker]['Close'], 30)
        sma200 = SMA(stocks[ticker]['Close'], 200)
        enter_pos = crossover(sma30, sma200)
        exit_pos = crossunder(sma30, sma200)

        # Parameters
        initial_capital = 10000 # Right now an investment of 10000 is made in each enter_pos, this will change as I want it to be more fluid
        costs = 0.002 # Set as decimal, right now 2% of the price
        direction = 'long' # Set as 'long' or 'short'

        trading_system = apply_trading_system(stocks, ticker, initial_capital, costs, enter_pos, exit_pos, direction)
        results[ticker] = trading_system

    # Combine results for all tickers into a single DataFrame
    portfolio_equity = pd.DataFrame(results)
    portfolio_equity['Total Equity'] = portfolio_equity.sum(axis=1)
    # Calculate metrics
    metriccalc(portfolio_equity, startdate, enddate)
    summaryscreen(portfolio_equity, startdate, enddate)

    # Remove all the unnecessary columns generated in the function
    columns_to_keep = ['Total Equity', 'portfolio_beta', 'Volatility'] # Column names are specified that appear in final dataframe
    portfolio_equity = portfolio_equity.drop(columns=[col for col in portfolio_equity.columns if col not in columns_to_keep])
    return portfolio_equity

if __name__ == "__main__":
    # Right now it will analyze only these tickers, in the final version it will be changed to analyze all stock tickers available
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'NVDA', 'JPM', 'V', 'NFLX', 'TSLA']

    portfolio_results = apply_trading_system_to_portfolio(tickers)

    # Chart which shows portfolio equity over time, should be primarily used for analysis and debugging reasons.
    plt.figure(figsize=(14, 7))
    plt.plot(portfolio_results['Total Equity'], label='Total Portfolio Equity')
    plt.title('Portfolio Equity Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Equity')
    plt.legend()
    plt.grid(True)
    plot_path = r'---ENTER YOUR PATH---'
    plt.savefig(plot_path, format='png', dpi=300) # Download the chart as a png to plot_path

    # Mann Whitney U-test
    # Monte Carlo to test for performance and risk during varying market conditions
    ## Tie this with testing on assets correlations and betas so a more "realistic market" can be simulated
