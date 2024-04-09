import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def stockdata(ticker, startdate, enddate):
    stock = yf.download(ticker, start=startdate, end=enddate)
    return stock

def SMA(stock_data, period):
    return stock_data['Close'].rolling(window=period).mean()

def crossover(array1, array2):
    return array1 > array2

def crossunder(array1, array2):
    return array1 < array2

ticker = 'AAPL'
enddate = datetime.now()
startdate = enddate - timedelta(days=5100)

stock = stockdata(ticker, startdate, enddate)
sma30 = SMA(stock, 30)
sma200 = SMA(stock, 200)

enter_pos = crossover(sma30, sma200)
exit_pos = crossunder(sma30, sma200)

print("Enter Positions (crossover):")
print(enter_pos[enter_pos == True])

print("\nExit Positions (crossunder):")
print(exit_pos[exit_pos == True])