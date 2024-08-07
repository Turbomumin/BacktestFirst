# Base-Engine-1
This project implements a stock trading system that downloads historical stock data, calculates simple moving averages (SMAs), and applies a trading strategy to simulate portfolio performance over time. The system uses data from Yahoo Finance, analyzes multiple stock tickers, and calculates various performance metrics. A key point of the project is to be able to change the tested strategy seamlessly.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Functions](#functions)
- [Issues](#issues)
- [Data](#data)

## Description
This project tests the profitability and risk character of a given trading strategy. It does this by gathering price data for all the given stock tickers for a given timeframe. The code determines enter and exit signals and formats a dataframe to reflect these signals. It calculates returns for each stock (all past profits reinvested). Combining the dataframes of each stock, return metrics along with risk character is then calculated and presented in a summary table for the user.

This project is limited in terms of what assets can be traded in the strategies. Equities are the primary asset that is traded. Options could technically be implemented but more code is required to make that as seamless and flexible as planned. For more market-based option pricing, there is still a lot of work to be done. Trading bonds cannot be simulated with this project.

## Installation
The code uses NumPy, Pandas, Yfinance, Datetime, and MatPlotLib. When using my project, you can install the required packages with pip:
```
pip install numpy pandas yfinance matplotlib
```

Numpy is used primarily to define the enter and exit signals in the dataframe. It is used an additional time to return the lowest whole number of a given number (36.57 -> 36.0). This makes it a less important package used for the project.

The project is heavily pandas-reliant. Calculations are made based on and in dataframes, which pandas is designed for. For all formatting code, pandas is used in some way. 

Yfinance is just as crucial as pandas, since the project needs the price data from Yfinance to be able to make the necessary calculations. Yfinance could be switched out for another package that returns price data, but the project is built around Yfinance.

Datetime is used to define the period of testing, along with calculating the means of variables in specific years. Datetime is therefore very important in the project.

MatPlotLib is just used for plotting the returns of the trading strategy. It is not very important as of now but this will change when more complex metrics are presented as part of strategy summary results. Might explore seaborn.

## Functions
`stockdata(tickers, startdate, enddate)`
Downloads historical close-price data for the given tickers and date range.

`SMA(stockdata, period)`
Calculates the Simple Moving Average (SMA) for the given period. The variables are created in multiple instances in the project. The function calculates the mean of stock prices during a given period before the day in question. This creates a lower and higher SMA.

`crossover(data1, data2)`
Determines if a crossover has occurred (data1 > data2).

`crossunder(data1, data2)`
Determines if a crossunder has occurred (data1 < data2).

`apply_trading_system(stocks, ticker, initial_capital, costs, enter_pos, exit_pos, direction)`
Applies the trading system to each specific ticker. Uses the enter and exit signals to create the market_position column in the data frame. Creates the entry_price and exit_price columns so returns can be more easily calculated during the entire timeframe.

`update_signals(sma30, sma200, direction)`
Updates entry and exit signals based on the direction ('long' or 'short').

`compute_positions_and_operations(ticker_data, initial_capital, costs)`
Computes positions and operations for the trading system. Four columns are calculated (Shares_owned, Invested, Univnested, and Balance). Returns the daily balance ( Uninvested + Invested) for each stock.

`metriccalc(portfolio_equity, startdate, enddate)`
Calculates various performance metrics for the portfolio.

`yearly_total_equity_change(group)`
Calculates the yearly percentage change in total equity.

`summaryscreen(portfolio_equity, startdate, enddate)`
Generates a summary screen with key performance metrics.

`apply_trading_system_to_portfolio(tickers)`
Applies the trading system to multiple tickers and generates a combined portfolio performance. Timeframe along with key parameters (initial investment per stock, transaction costs, and direction) are defined here.

## Issues
### Current issues
- The project is slow right now, I am looking at ways to make it faster.
- Changing parameters and strategy is right now tedious. They are spread out over the script and one would have to read the readme file to find each spot where changes should be made. A cleaner way to adjust parameters is needed.
- The results are to be presented in a cleaner format. Strategy analysis and alpha-seeking require looking at a lot of different metrics and measurements, so I will need to find a clean way to present all findings.
- In testing, I encountered problems when there was not sufficient stock data for the given period. I have not encountered this problem since but it is still an anomaly, will need to take a look at this at some point.
- The backtesting project is supposed to work by gathering tickers from a CSV file. This should be implemented ASAP.

### Future add-ons
- Measures of risk: A cornerstone of modern finance is more risk equals more rewards. I want to account for this in my project. I have implemented portfolio beta and Sharpe as measures of risk. Other than the Sharpe ratio, I would include metrics such as volatility, drawdown, Value at Risk, expected shortfall, Sortino ratio, tail risk, and liquidity risk. These are a lot of measures but I will take a look at each one to determine the best way to visualize the risk profile of the trading strategy.
- Statistical testing: A trading strategy can't be purely evaluated based on the returns it would have generated in historical periods. Statistical testing as part of the backtesting could reveal important insights into a strategy to an investor. Mann-Whitney U-test and regression could for example be used.

## Data
Modern literature and discussions with industry professionals have highlighted the importance of data validation and verification when it comes to a system like the one I am attempting to create. Any aspiring trader who wishes to backtest their strategies and gain insight into using them in real markets will need to understand the limitations that come with the certain packages and techniques that I have employed in the creation of this engine.

### Yfinance for price data
Key limitations of finance:
- The limit of the public API is 2000 requests/day.
- <1d data is available for the last 60 days only, and 1m data is available only for the last 7 days
- HTML scrapping gives exposure to getting blacklisted or rate limited
These limitations have to be considered when configuring the program

### Retreiving stock tickers
In testing and developing I am using a shorter list of equities to trade with. This is only so that runtime is short while still providing the full testing potential. As of 7th August 2024, there are 7105 stocks that my source can provide. This is quite a large amount and therefore I aim to optimize the runtime fully before I start testing regularly with all the stocks. The data on currently traded stocks is found on the [NASDAQ website](https://www.nasdaq.com/market-activity/stocks/screener).
