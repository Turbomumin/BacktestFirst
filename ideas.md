# Test
**What is next?** The following aspects I'm going to take a look at and work on further.

_OPTIMIZATION AND STREAMLINING_

Data handling is going to be optimized I received feedback that certain pandas functions like 'apply' can be optimized further. I am going to be looking at vectorized operations that could improve efficiency. When this engine is fully developed, I will be using it to analyze multiple assets at the same time (i.e. multithreading). This will mean that the need for optimization is already of great importance.

Make the variables actual variables (i.e. make them non-hardcoded) Right now, the parameters are hardcoded into the code. This is suitable for now, but I want to change it as soon as some other things are fixed. I am exploring different options for implementing these changes. I will also need to take a look at the data to see if the variables are working properly since I found some irregularities with for example transaction costs.

Error handling This is a very important change I am looking to implement quickly. Currently, no functions in the code handle errors and adapt the process to potential mistakes. To cover those bases, I am going to implement various error-handling techniques. I am going to focus on implementing feedback protocols if the information is substandard. I will be implementing this in the main script function of the code since I believe this is the most optimal to solve these potential problems.

Adaptability of the engine This engine is supposed to be used for my future testing of various strategies. A big problem that I foresee coming is the limited availability of incorporating a new trading strategy. I developed the engine with a test strategy of Double Moving Averages Crossover. I will need to take precautions to make the engine more adaptable.

_READABILITY AND PERFORMANCE_

Comments I need to streamline the comments in the code. I am not an expert software engineer and this project is going to test my abilities heavily. Introducing more specific comments and making the code more clear and readable will make life easier for any reader, including me. Because I will learn as I go, I will need to keep track of what exactly is going on in the code. In this project, it is especially important since I will be using the engine once I am finished developing it.

Refactor and modularize The function apply_trading_system is very long and complex in its current form. I believe there is value in shortening it and breaking the function down into smaller and more focused functions. This should make the code more readable and make it easier to debug and maintain.

_NEW FEATURES_

Market-wide investing : This is the most important planned feature of my engine. According to NYSE, there are around 8000 listed securities that are publically traded. My engine is right now only implementing the trading strategy for one given security. Looking at less than 0,0125% of the market is not a great representation of the market, so I am working to implement this change quickly. This will require a lot more computing power and therefore this development might require its branch.

Fluid transaction costs : The engine assumes in its current form that transaction costs are constant (i.e. 50-cent to enter position, and 50 cent to exit position). Considering the irregularities I found earlier and the constant nature of the variable, I am considering implementing a fluid transaction cost per transaction. This will require more research so I can justify whichever approach I choose to use. I will also be looking at incorporating slippage into the engine.

Data visualization : This is more of an additional feature to the engine and strategy testing. I will implement this change when I'm happy with other factors I wish to improve and change. I am looking at matplotlib, plotly, and seaborn for this development. The visualization will be planned more thoroughly at a later stage, but the basic idea of it is to visualize performance and risk characteristics of trading strategies with the use of ex. scatterplots.

Different market conditions : I am looking to develop functions for the engine where strategies can be tested under specific market conditions. This is a suggestion I received that I thought sounded very cool so I will start working on that at some point. In an advanced stage, this would also include simulated scenarios in past time. Don't expect this to happen soon, but I hope at some point I will show some developments regarding this.

Hedge strategies and portfolio insurance : These are to my understanding very commonplace in practical portfolio management practices. For the uninformed reader, a quick review of these concepts will tell you that these are easy to implement and are quite normal. This is a very important development for this code to have any validity. I will be updating this point with a dedicated research document.
