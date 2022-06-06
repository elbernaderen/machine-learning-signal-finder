# amplitudes.py
Fit a crypto trade predictor model with a determined sequence of candels from different assets.
## Description
With this script, we run through each historical asset like BTCUSDT or ETHUSDT and generate numerous rows with a determinated number of candels, and for each candel add some technical indicators like, macd, macd histogram, macd signal, rsi and some indicators that express the amplitude of high and low values, open and closure values, normalized volume and the open, close, high and low normalized values (added as a comment). With all those indicators, we try to find a pattern in prices movement that allow us to know if the prices are going to rise or fall. Then, with a determinated number of candels that come next of the last one of the generated row, we know if the price have risen or fallen. If the price increase its value in an determinated percent, we assign this row or sequence as a forecast or prevision of value rise with the determinated "increase", and for any other case we consider that is not allowing us to predict anything and assign it as "0".
Once we have ran over all the historical assets we determined and generated the mentionated rows with its assigned values, it's time to train the Random Tree Forest model.
Then, with the model we can predict if the prices will rise and send a signal with the telegram bot, and so we'll know if have to buy or not an asset determined.
Before we create the rows, first we filter them taking in count the slope of the candels (rising or falling market, this is adjusted to falling market but it can be easily changed), the rsi value and the volume of the last candels, and just if the candel sequence fit the requirements the row mentionated is created and considered for the predictor.

## Must install
[pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/install/) and [scipy](https://scipy.org/install/) libraries are used to work with data frames and lists. 

[sklearn](https://scikit-learn.org/stable/install.html) is a library used to create and train the machine learning model.

[pickle](https://docs.python.org/3/library/pickle.html#:~:text=%E2%80%9CPickling%E2%80%9D%20is%20the%20process%20whereby,back%20into%20an%20object%20hierarchy.) is needed to save the model in a .sav file, so we can use it in a easy way with the backtester **prueba_final.py** or the signal sender **mensajero_d.py**.


## Usage
Once we have downloaded the historical assets (one or more) with the same interval in the same directory of the program, we call the program with the historical assets as command line arguments in capital as:

```bash
py amplitudes_rsi_vol_rsi.py BTCUSDT ETHUSDT ADAUSDT
```
Then, the program will ask the next variables:
```bash
Enter the percentage that have to rise the price to consider it as a success:
```
This is the increment that we look for predict, ex: 0.01
```bash
Enter the number of candels (Y) to consider in the model for the prediction:
```
The increment before mentionated has to be between the Y candels
```bash
Enter the number of candels (X) consider in the model for the prediction:
```
These will be the candels we use to predict
```bash
Enter the amount of periods for rsi calculation (14 recomended):
```
A period for rsi calculation can be better for a candle interval analysis, and not for other one, so, it can be modificated if want it
```bash
Enter the rsi value to consider (30 recomended):
```
The RSI value is a indicator for some strategies in crypto-trading, so it also can be modificated as a superior limit (the script can be easily changeable)
```bash
Enter how much to increase the mean volume value:
```
This is a filter to consider just the candles with a bigger volume than the mean volume of a determined amount of candles
```bash
Enter the slope to take in reference, (0 recomended):
```
The slope of the close value of the candels indicates if the market (in this sequence) is bullish or bearish.
```bash
Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m 
```
The interval of the historical assets to consider.
```bash
Enter how many candels consider to calculate the volume mean:
```
To calculate the mean volume,so it can know if the volume has a increment or in other words if there are big participants, ex: 300.
Once the program have finished, a classification report will be printed in console, with the accuracy, precission, etc of the model, and a .sav file will be created with the model ready for be used.
# backtest_strategy.py
This program, as it's name says is a backtest for a strategy with a determinated historical asset.
## Description
With a historical asset, that has been download with **call_bina.py**, this program creates an .xlsx spreadsheet where is the data and the decision of the stratrategy, buy or don't do nothing.
Taking in count the slope of the candels (rising or falling market, this is adjusted to falling market but it can be easily changed), the rsi value and the volume of the last candels, if the strategy set fits with the sequence, the column "vale" will be the value of the increment predicted. In all the other cases the value will be 0. Further, a determined number of candles that come next to the sequence analyzed will be added, with the highest and lowest values, so we can know if the strategy is acerted, and with this information we can improve it.
## Must install
[pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/install/) and [scipy](https://scipy.org/install/) libraries are used to work with data frames and lists. 
## Usage
Once we have downloaded the historical asset in the same directory, we call the program:

```bash
py backtest_strategy.py
```
Then, the program will ask the next variables:
```bash
Enter the number of candels (Y) to consider in the model for the prediction:
```
The increment before mentionated has to be between the Y candels
```bash
Enter the number of candels (X) consider in the model for the prediction:
```
```bash
Enter the amount of periods for rsi calculation (14 recomended):
```
A period for rsi calculation can be better for a candle interval analysis, and not for other one, so, it can be modificated if want it
```bash
Enter how much to increase the mean volume value:
```
This is a filter to consider just the candles with a bigger volume than the mean volume of a determined amount of candles
# mensajero_d.py
## Introduction:
Here we have a signal bot trading, using telegram (https://python-telegram-bot.readthedocs.io/en/stable/),
that finds signals with a predictor made with Machine Learning, trained with a some cryptho/usdt database, obtained
with the Binance library (https://resilient-quant-trader.medium.com/scraping-crypto-currency-historical-data-from-binance-using-python-9c0e77c04df7).
How to Install and Run the Project:
Install Binance library:
pip install python-binance
Install Pandas library
