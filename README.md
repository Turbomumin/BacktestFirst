# Base-Engine-1
This is version 1 of a backtesting engine I am developing. The desired result of this project is to build a backtesting environment that I can use for my future projects. Please let me know If you have any suggestions regarding the project. 

The idea is to first create this backtesting environment, and then use this engine as it is for any other projects. In this first version, I will simply develop a script that requires the user to manually enter the trading strategy that it tests. One day I hope to update the code so it can be applied as a program, which could allow for more simplicity and readability.

**Structure of the code**
1. Libraries
2. Stock data
3. Define a trading strategy
4. Define a market position function
5. Define a backtesting function

Steps 1-3 are relatively simple in nature and thus don't contain too many comments. For additional knowledge about the libraries used in this project, please consult the documentation by the authors of these libraries.

For this project I am using the yf.download command of yfinance. In its current form, it returns the daily stock prices as far back as 5100 days from the startdate, which is the current date of the operator. It pulls the daily price data of the stock ticker that it is given in the input function. 
Yfinance is suitable for now but might need some adjustment when I start implementing wider markets into this engine. Stay tuned for this update, as it will scale up the hardware requirements of this project. My idea is to introduce multithreading features to the engine so data pull requests are streamlined, I will also need to consider if I should switch to for example AlphaVantage's API when the size of pull requests starts getting larger. I will also for formailty's sake change the enddate of the engine to be 60 days backwards from the current date.

The trading strategy that is used in the current code is a Double Moving Averages Crossover strategy. I won't go into detail in this version of the readme what this strategy is. It is simply a placeholder strategy. The short explanation of the stratgy is that a long-position is entered when the SMA (Simple Moving Average) of the shorter time period (in this case 30 days) is higher than the longer time period SMA (200 days). It exits this position when the opposite is true. The idea is that a operator will be able to code in their desired trading strategy and the engine will run and create a report. This will be further implemented in a future update.

Step 4 implements active trading and holding, since the strategies will often mean multiple different enter and exit signals. I will need to refine this when multiple different assets are analysed simultaneously.

Step 5 formats the data to create the final backtesting environment. I will need to refine this further as there some inefficiencies in the apply_trading_system function. The backtesting is especially implemented in this function since the transaction costs, type of asset, starting available capital, long or short, order type, and enter levels are incorporated into the simulated performance.

**What is next?**
The following aspects im going to take a look at and work on further.
- Data handling is going to be optimized
  To be updated!
