
# mensajero_d.py
## Introduction:
Here we have a signal bot trading, using telegram (https://python-telegram-bot.readthedocs.io/en/stable/),
that finds signals with a predictor made with Machine Learning, trained with a some cryptho/usdt database, obtained
with the Binance library (https://resilient-quant-trader.medium.com/scraping-crypto-currency-historical-data-from-binance-using-python-9c0e77c04df7).

# amplitudes_rsi_vol_rsi.py
## Introduction:

With this script, we run through each historical asset like BTCUSDT or ETHUSDT and generate numerous rows with a determinated number of candels, and for each candel add some technical indicators like, macd, macd histogram, macd signal, rsi and some indicators that express the amplitude of high and low values, open and closure values, normalized volume and the open, close, high and low normalized values. With all those indicators, we try to find a pattern in prices movement that allow us to know if the prices are going to rise or fall. Then, with a determinated number of candels that come next of the last one of the generated row, we know if the price have risen or fallen. If the price increase its value in an determinated percent, we assign this row or sequence as a forecast or prevision of value rise with the determinated "increase", and for any other case we consider that is not allowing us to predict anything and assign it as "0".
Once we have ran over all the historical assets we determined and generated the mentionated rows with its assigned values, it's time to train the Random Tree Forest model.
Then, with the model we can predict if the prices will rise and send a signal with the telegram bot.
How to Install and Run the Project:
Install Binance library:
pip install python-binance
Install Pandas library
