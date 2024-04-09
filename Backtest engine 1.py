import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


# Get stock data function
def stockdata(ticker, startdate, enddate):
    stock = yf.download(ticker, start=startdate, end=enddate)
    return stock

# Define investment startegy
def SMA(stock_data, period):
    return stock_data['Close'].rolling(window=period).mean()
def crossover(array1, array2):
    return array1 > array2
def crossunder(array1, array2):
    return array1 < array2

# Define framework for active positions
def marketposition_generator(dataset):
    # Assuming dataset already contains 'enter_pos' and 'exit_pos' as columns
    status = 0
    mp = []
    for enter, exit in zip(dataset['enter_pos'], dataset['exit_pos']):
        if status == 0 and enter:
            status = 1
        elif status == 1 and exit:
            status = 0
        mp.append(status)
    
    dataset['mp'] = mp
    dataset['mp'] = dataset['mp'].shift(1)
    dataset.iloc[0, dataset.columns.get_loc('mp')] = 0  # Adjust to set the first value correctly, if necessary
    
    return dataset

def apply_trading_system(dataset, direction, order_type, enter_level, enter_pos, exit_pos):

    # Add enter and exit series, as well as market position to the dataset
    dataset['enter_pos'] = enter_pos.apply(lambda x: 1 if x else 0)
    dataset['exit_pos'] = exit_pos.apply(lambda x: -1 if x else 0)

    # Update the dataset with market positions
    dataset = marketposition_generator(dataset)

    # Define market orders
    # Define entry price. If previous value of mp was zero and present value is 1 (signal received), the it opens a position the next day
    if order_type == "market":
        dataset['entry_price'] = np.where((dataset.mp.shift(1) == 0) &
                                            (dataset.mp == 1), dataset.Open.shift(1), np.nan)
        # Define number of stocks (amount of shares we buy as the ration between the initial capital and the entry price)
        if INSTRUMENT == 1:
            dataset['number_of_stocks'] = np.where((dataset.mp.shift(1) == 0) &
                                                    (dataset.mp == 1), OPERATION_MONEY / dataset.Open, np.nan)
    
    # Further develop entry price
    dataset['entry_price'] = dataset['entry_price'].fillna(method='ffill')

    # Round number of stocks at integer the integer value and further develop it
    if INSTRUMENT == 1:
        dataset['number_of_stocks'] = dataset['number_of_stocks']\
                                        .apply(lambda x: round(x,0)).fillna(method='ffill')
    
    # Associate lavel entry to events_in every time mp moves from 0 to 1
    dataset['events_in'] = np.where((dataset.mp == 1) & (dataset.mp.shift(1) == 0), 'entry', '')

    # Define long trades
    if direction == 'long':
        if INSTRUMENT == 1:
        # Calculate open_operations (the profit)
            dataset['open_operations'] = (dataset.Close - dataset.entry_price) * dataset.number_of_stocks
            # Adjust the profit whenever a position is exited. Whenever a signal is given, the position is closed the following day
            dataset['open_operations'] = np.where((dataset.mp == 1) & (dataset.mp.shift(-1) == 0),
                                                    (dataset.Open.shift(-1) - dataset.entry_price) * dataset.number_of_stocks - 2 * COSTS,
                                                    dataset.open_operations)
    # Define for short trades
    else:
        if INSTRUMENT == 1:
            # Calculate open_operations (the profit)
            dataset['open_operations'] = (dataset.entry_price - dataset.Close) * dataset.number_of_stocks
            # Adjust the profit whenever a position is exited. Whenever a signal is given, the position is closed the following day
            dataset['open_operations'] = np.where((dataset.mp == 1) & (dataset.mp.shift(-1) == 0),
                                                    (dataset.entry_price - dataset.Open.shift(-1)) * dataset.number_of_stocks - 2 * COSTS,
                                                    daraset.open_operations)

    # Assign open_operations equal to 0 when no trade is happening
    dataset['open_operations'] = np.where(dataset.mp == 1, dataset.open_operations, 0)
    # Associate label exit to events_out everytime mp moves from 1 to 0 (when we receive an exit signal)
    dataset['events_out'] = np.where((dataset.mp == 1) & (dataset.exit_pos == -1), 'exit', '')
    # Associate value of open_operations to operations only when exiting a position, makes data aggregation easier
    dataset['operations'] = np.where((dataset.exit_pos == -1) &
                                        (dataset.mp == 1), dataset.open_operations, np.nan)
    # Define equity_line for close operations
    dataset['closed_equity'] = dataset.operations.fillna(0).cumsum()
    # Define equity_line for open operations
    dataset['open_equity'] = dataset.closed_equity + dataset.open_operations - dataset.operations.fillna(0)

    # Save the results to a csv file
    dataset.to_csv('trading_system_report.csv')

    return dataset

# Run script
if __name__ == "__main__":
    ticker = input("Write a stock ticker").upper()

    enddate = datetime.now()
    startdate = enddate - timedelta(days=5100)
    stock = stockdata(ticker, startdate, enddate)

    sma30 = SMA(stock, 30)
    sma200 = SMA(stock, 200)

    enter_pos = crossover(sma30, sma200)
    exit_pos = crossunder(sma30, sma200)

    COSTS = 0.50
    INSTRUMENT = 1 
    OPERATION_MONEY = 10000
    DIRECTION = "long"
    ORDER_TYPE = "market"
    ENTER_LEVEL = stock['Open']
    trading_system = apply_trading_system(stock, DIRECTION, ORDER_TYPE, ENTER_LEVEL, enter_pos, exit_pos)

    net_profit = trading_system['closed_equity'][-1] - OPERATION_MONEY
    print(round(net_profit, 2))
