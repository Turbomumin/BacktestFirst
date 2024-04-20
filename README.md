# Base-Engine-1
This is version 1 of a backtesting engine I am developing. The desired result of this project is to build a backtesting environment that I can use for my future projects. Please let me know If you have any suggestions regarding the project. 

The idea is to first create this backtesting environment, and then use this engine as it is for any other projects. In this first version, I will simply develop a script that requires the user to manually enter the trading strategy that it tests. One day I hope to update the code so it can be applied as a program, which could allow for more simplicity and maintenance.

The code uses four different libraries and is broken down into six different defined functions. I have chosen to include a specific run script because I have been taught it makes the code more readable. In its current form, the script requires a stock ticker to be entered in a prompt, and six other variables are defined in the run script. 

**Purpose of the engine**
The purpose of the engine is simple. A strategy is defined and the engine calculates the net profit from this strategy. Currently, the operator will need to enter a stock ticker which the strategy can invest in. Please 

**Structure of the code**
1. Libraries
2. Stock data
3. Define a trading strategy
4. Define a market position function
5. Define a backtesting function

Steps 1-3 are relatively simple and thus don't contain too many comments. For additional knowledge about the libraries used in this project, please consult the documentation by the authors of these libraries.

For this project, I am using the yf.download command of yfinance. In its current form, it returns the daily stock prices as far back as 5100 days from the start date, which is the current date of the operator. It pulls the daily price data of the stock ticker that is given in the input function. 
Yfinance is suitable for now but might need some adjustments when I start implementing wider markets into this engine. Stay tuned for this update, as it will scale up the hardware requirements of this project. My idea is to introduce multithreading features to the engine so data pull requests are streamlined, I will also need to consider if I should switch to for example AlphaVantage's API when the size of pull requests starts getting larger. I will also for formality's sake change the end date of the engine to be 60 days backwards from the current date.

The trading strategy that is used in the current code is a Double Moving Averages Crossover strategy. I won't go into detail in this version of the readme what this strategy is. It is simply a placeholder strategy. The short explanation of the strategy is that a long position is entered when the SMA (Simple Moving Average) of the shorter period (in this case 30 days) is higher than the longer period SMA (200 days). It exits this position when the opposite is true. The idea is that an operator will be able to code in their desired trading strategy and the engine will run and create a report. This will be further implemented in a future update.

Step 4 implements active trading and holding since the strategies will often mean multiple different enter and exit signals. I will need to refine this when multiple different assets are analyzed simultaneously.

Step 5 formats the data to create the final backtesting environment. I will need to refine this further as there are some inefficiencies in the apply_trading_system function. Backtesting is especially implemented in this function since the transaction costs, type of asset, starting available capital, long or short, order type, and entry levels are incorporated into the simulated performance.

# Notes on data used

Modern literature and discussions with industry professionals have highlighted the importance of data validation and verification when it comes to a system like the one I am attempting to create. Any aspiring trader who wishes to backtest their strategies and gain insight into using them in real markets will need to understand the limitations that come with the certain packages and techniques that I have employed in the creation of this engine.

## Yfinance
The limit of the public API is 2000 requests per day. I will need to analyze the exact implications of this for my project. No matter the result I will need to consider this specifically for the engine when writing the code. Furthermore, the request limit might cause problems when strategies become more complex and more assets and types of derivatives are considered for investment. 

A problem with the use of yfinance is that intraday data is very limited. 1m data is available only for the last 7 days, and <1d data is available for the last 60 days only. This means that any testing of ex. HFT strategies would have a very limited timeframe. Therefore, one might conclude that as long as yfinance is used to retrieve price data, the engine is very limited in backtesting HFT strategies. 

A problem with yfinance is that it retrieves data through HTML scraping on Yahoo Finance. The accuracy of the price data can be compromised by changes on the Yahoo Finance website. There is also the risk of getting rate limited or blacklisted. This is a risk with any web scraping method but this engine retrieves 36,414 million data points and therefore the risk becomes considerably bigger.

## Retreiving stock tickers
I have decided to for the time being use a CSV file that contains currently traded stocks on public markets. I chose this method so my engine would be utilizing the whole market and not just a compiled list of more popular stocks (i.e. S&P500 or DJI). The data on currently traded stocks is found on the NASDAQ website (accessible from https://www.nasdaq.com/market-activity/stocks/screener). A CSV file was downloaded on the 16th of April 2024 and I only removed price-related information since the engine is getting that from Yfinance.

In total, 7140 stocks are included in the list and information is included on ticker, name, market cap, country of origin, IPO year, volume, sector, and industry. This data is included since it could be used for creating potential strategies. The list includes stocks from 12 different sectors and 150 different industries. 833 stocks don't have an associated sector or industry. All stocks in the file are traded on either NASDAQ, NYSE, or AMEX. The stocks are originally based in 59 different countries.
