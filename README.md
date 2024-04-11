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

**What is next?**
The following aspects I'm going to take a look at and work on further.

_OPTIMIZATION AND STREAMLINING_
- Data handling is going to be optimized
I received feedback that certain pandas functions like 'apply' can be optimized further. I am going to be looking at vectorized operations that could improve efficiency. When this engine is fully developed, I will be using it to analyze multiple assets at the same time (i.e. multithreading). This will mean that the need for optimization is already of great importance. 

- Make the variables actual variables (i.e. make them non-hardcoded)
Right now, the parameters are hardcoded into the code. This is suitable for now, but I want to change it as soon as some other things are fixed. I am exploring different options for implementing these changes. I will also need to take a look at the data to see if the variables are working properly since I found some irregularities with for example transaction costs.

- Error handling
This is a very important change I am looking to implement quickly. Currently, no functions in the code handle errors and adapt the process to potential mistakes. To cover those bases, I am going to implement various error-handling techniques. I am going to focus on implementing feedback protocols if the information is substandard. I will be implementing this in the main script function of the code since I believe this is the most optimal to solve these potential problems.

- Adaptability of the engine
This engine is supposed to be used for my future testing of various strategies. A big problem that I foresee coming is the limited availability of incorporating a new trading strategy. I developed the engine with a test strategy of Double Moving Averages Crossover. I will need to take precautions to make the engine more adaptable.

_READABILITY AND PERFORMANCE_
- Comments
I need to streamline the comments in the code. I am not an expert software engineer and this project is going to test my abilities heavily. Introducing more specific comments and making the code more clear and readable will make life easier for any reader, including me. Because I will learn as I go, I will need to keep track of what exactly is going on in the code. In this project, it is especially important since I will be using the engine once I am finished developing it. 

- Refactor and modularize
The function apply_trading_system is very long and complex in its current form. I believe there is value in shortening it and breaking the function down into smaller and more focused functions. This should make the code more readable and make it easier to debug and maintain. 

_NEW FEATURES_
- Market-wide investing
This is the most important planned feature of my engine. According to NYSE, there are around 8000 listed securities that are publically traded. My engine is right now only implementing the trading strategy for one given security. Looking at less than 0,0125% of the market is not a great representation of the market, so I am working to implement this change quickly. This will require a lot more computing power and therefore this development might require its own branch.

- Fluid transaction costs
The engine assumes in its current form that transaction costs are constant (i.e. 50-cent to enter position, and 50 cent to exit position). Considering the irregularities I found earlier and the constant nature of the variable, I am considering implementing a fluid transaction cost per transaction. This will require more research so I can justify whichever approach I choose to use. I will also be looking at incorporating slippage into the engine.

- Data visualization
This is more of an additional feature to the engine and strategy testing. I will implement this change when I'm happy with other factors I wish to improve and change. I am looking at matplotlib, plotly, and seaborn for this development. The visualization will be planned more thoroughly at a later stage, but the basic idea of it is to visualize performance and risk characteristics of trading strategies with the use of ex. scatterplots. 

- Different market conditions
I am looking to develop functions for the engine where strategies can be tested under specific market conditions. This is a suggestion I received that I thought sounded very cool so I will start working on that at some point. In an advanced stage, this would also include simulated scenarios in past time. Don't expect this to happen soon, but I hope at some point I will show some developments regarding this.

- Hedge strategies and portfolio insurance
These are to my understanding very commonplace in practical portfolio management practices. For the uninformed reader, a quick review of these concepts will tell you that these are easy to implement and are quite normal. This is a very important development for this code to have any validity. I will be updating this point with a dedicated research document.



