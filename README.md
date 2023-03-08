
# amplitudes.py
Fit a crypto trade predictor model with a determined sequence of candels from different Cryptocurrency. [(read jupyter_analisis also, for a better interpretation)](https://github.com/elbernaderen/jupyter_analysis#btcusdt_adausdt_xmrusdt_ethusdt_bnbusdt_30m_hour_dayipynb)

With this script, we run through each Crypto-currency Historical Data like BTCUSDT or ETHUSDT and generate numerous rows with a determinated number of candels. For each candel add technical indicators like:
* macd 
* macd histogram 
* macd signal 
* RSI 

It also include indicators that express:
* amplitude of high and low values 
* open and closure values 
* normalized volume . 

With all those indicators, we try to find a pattern in prices movement that allow us to know if the prices are going to rise or fall. Then, with a determinated number of candels that come next of the last one of the generated row, we know if the price have risen or fallen. 

If the price increase its value in an determinated percent, we assign this row or sequence as a forecast or prevision of value rise with the determinated "increase", and for any other case we consider that is not allowing us to predict anything and assign it as "0".

Once we have ran over all the Cryptocurrency Historical Data we determined and generated the mentionated rows with its assigned values, it's time to train the Random Tree Forest model.

Then, with the model we can predict if the prices will rise and send a signal with the telegram bot, and so we'll know if have to buy or not an Cryptocurrency determined.

Before we create the rows, first we filter them taking in count the slope of the candels (rising or falling market, this is adjusted to falling market but it can be easily changed), the rsi value and the volume of the last candels, and just if the candel sequence fit the requirements the row mentionated is created and considered for the predictor.

## Must install
[pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/install/) and [scipy](https://scipy.org/install/) libraries are used to work with data frames and lists. 

[sklearn](https://scikit-learn.org/stable/install.html) is a library used to create and train the machine learning model.

[pickle](https://docs.python.org/3/library/pickle.html#:~:text=%E2%80%9CPickling%E2%80%9D%20is%20the%20process%20whereby,back%20into%20an%20object%20hierarchy.) is needed to save the model in a .sav file, so we can use it in a easy way with the backtester [backtest_amplitudes.py](https://github.com/elbernaderen/machine-learning-signal-finder#backtest_strategypy) or the signal sender [messenger_d.py](https://github.com/elbernaderen/machine-learning-signal-finder#messenger_dpy).


## Usage
Once we have downloaded the Cryptocurrency Historical Data (one or more) with the same interval in the same directory of the program, we call the program with the Crypto-currency  as command line arguments in capital letters as:

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
Enter the number of candels (X) considered in the model for the prediction:
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
The interval of the Crypto-currency Historical Data to consider.
```bash
Enter how many candels consider to calculate the volume mean:
```
To calculate the mean volume,so it can know if the volume has a increment or in other words if there are big participants, ex: 300.
Once the program have finished, a classification report will be printed in console, with the accuracy, precission, etc of the model, and a .sav file will be created with the model ready for be used.


![tempsnip](https://user-images.githubusercontent.com/65098903/178709836-f52c5451-a3dc-410a-9404-ed0b931e587e.png)



# backtest_strategy.py
This program, as it's name says is a backtest for a strategy with a determinated Crypto-currency Historical Data.
## Description
With a Crypto-currency Historical Data, that has been download with **call_bina.py**, this program creates an .xlsx spreadsheet where is the data and the decision of the stratrategy, buy or do nothing.
Taking in count the slope of the candels (rising or falling market, this is adjusted to falling market but it can be easily changed), the rsi value and the volume of the last candels, if the strategy set fits with the sequence, the column "vale" will be the value of the increment predicted. In all the other cases the value will be 0. Further, a determined number of candles that come next to the sequence analyzed will be added, with the highest and lowest values, so we can know if the strategy is acerted, and with this information we can improve it.
## Must install
[pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/install/) and [scipy](https://scipy.org/install/) libraries are used to work with data frames and lists. 
## Usage
Once we have downloaded the Crypto-currency Historical Data in the same directory, we call the program:

```bash
py backtest_strategy.py
```
Then, the program will ask the next variables:
```bash
Enter the number of candels (Y) that come after the prediction:
```
The increment before mentionated has to be between the Y candels
```bash
Enter the number of candels (X) considered for the technical analysis:
```
```bash
Enter the amount of periods for rsi calculation (14 recomended):
```
A period for rsi calculation can be better for a candle interval analysis, and not for other one, so, it can be modificated if want it
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
The interval of the Crypto-currency Historical Data to consider.
Once the program has finished, a .xlsx spreadsheet will be created with a column with the found signals and the consecutive variations of the high and low candels value respect the close value of the X's last candel, so we can verify if prices had rises or fell and modificate the strategy to improve the prediction.




# backtest_amplitudes.py
With this program,the user can make a backtest for one or more models created with [amplitudes](https://github.com/elbernaderen/machine-learning-signal-finder/blob/main/README.md#amplitudespy) with a determinated Crypto-currency Historical Data.
## Description
With a Crypto-currency Historical Data, that has been download with **call_bina.py**, this program creates an .xlsx spreadsheet where is the data and the decision (buy or do nothing) of one or more models created with [amplitudes](https://github.com/elbernaderen/machine-learning-signal-finder/blob/main/README.md#amplitudespy), where these models could be created with different criteria, like the percentage that have to rise the price to consider it as a success  RSI, volume, etc.
Using the .sav model/s files, the program predict if the price will increase it's value to achieve the increment predict, and this will be added in a column with the model name.
Taking in count the slope of the candels (rising or falling market, this is adjusted to falling market but it can be easily changed), the rsi value and the volume of the last candels, if the variables set fits with the sequence, the column "vale" will be 1 and otherwise will be 0, so it can be used as a filter.the value of the increment predicted. In all the other cases the value will be 0. Further, a determined number of candles that come next to the sequence analyzed will be added, with the highest and lowest values, so we can know if the strategy is acerted, and with this information we can improve it.
## Must install
[pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/install/) and [scipy](https://scipy.org/install/) libraries are used to work with data frames and lists.
[Binance](https://pypi.org/project/python-binance/) is needed to download the crypto-currency historical data.
with [sklearn](https://scikit-learn.org/stable/install.html) we can use the model with the predictor.

[pickle](https://docs.python.org/3/library/pickle.html#:~:text=%E2%80%9CPickling%E2%80%9D%20is%20the%20process%20whereby,back%20into%20an%20object%20hierarchy.) is needed to open the .sav file with the predictor model.
## Usage
Once we have downloaded the Crypto-currency Historical Data in the same directory, we call the program:

```bash
py backtest_amplitudes.py
```
Then, the program will ask the next variables:
```bash
Enter the number of candels (Y) that come after the prediction:
```
The increment before mentionated has to be between the Y candels
```bash
Enter the number of candels (X) considered for the technical analysis:
```
```bash
Enter the amount of periods for rsi calculation (14 recomended):
```
A period for rsi calculation can be better for a candle interval analysis, and not for other one, so, it can be modificated if want it

```bash
Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m 
```
The interval of the Crypto-currency Historical Data to consider.
```bash
Enter how many candels consider to calculate the volume mean:
```
To calculate the mean volume,so it can know if the volume has a increment or in other words if there are big participants, ex: 300.
Once the program have finished, a classification report will be printed in console, with the accuracy, precission, etc of the model, and a .sav file will be created with the model ready for be used.

Once the program has finished, a .xlsx spreadsheet will be created with a column with the found signals and the consecutive variations of the high and low candels value respect the close value of the X's last candel, so we can verify if prices had rises or fell and modificate the strategy to improve the prediction.




# messenger_d.py
## Description
Here we have a signal bot trading, that using [telegram](https://python-telegram-bot.readthedocs.io/en/stable/) sends signals found with a [predictor](https://github.com/elbernaderen/machine-learning-signal-finder/blob/main/README.md#amplitudespy) made with Machine Learning, trained with a some crypto-currency historical database, obtained
with the [Binance](https://resilient-quant-trader.medium.com/scraping-crypto-currency-historical-data-from-binance-using-python-9c0e77c04df7) library.
## Must install
[pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/install/) and [scipy](https://scipy.org/install/) libraries are used to work with data frames and lists. 
With [sklearn](https://scikit-learn.org/stable/install.html) we can use the model with the predictor. 

Will use [bina.py](https://github.com/elbernaderen/machine-learning-signal-finder#binapy) to download the actualized data to make the prediction. 

Also need [yaml](https://pypi.org/project/PyYAML/) to save and read the api data in a yml file.
[Binance](https://pypi.org/project/python-binance/) is needed to download the crypto-currency historical data.
## Usage:
As this bot use Telegram to send messagess, we'll need the user id of the receiver and the API key from the count of telegram that we'll use, and this data will be set in the yml file **telconfig** that is in the ignore folder. 

Also, before calling the program, we must have the sav file of the predictor [model](https://github.com/elbernaderen/machine-learning-signal-finder#amplitudespy) created, because it has to be entered as an argumet in console. 

With the predictor model created, we must be call the program in console as continue:

```bash
py messenger_d.py model_p_15_perio_14_in_6_0.05_2022-05-24_17_44
```
Where **model_p_15_perio_14_in_6_0.05_2022-05-24_17_44** is the name of the model created.

Then the program will ask to enter the next variables:
```bash
Enter the number of candels (X) considered in the model for the prediction:
```
The number of candels that will be used to make the prediction, must be equal to the number used in the [model](https://github.com/elbernaderen/machine-learning-signal-finder#amplitudespy) 
```bash
Enter the amount of periods for rsi calculation (14 recomended):
```
A period for rsi calculation can be better for a candle interval analysis, and not for other one, so, it can be modificated if want it

```bash
Enter how much to increase the mean volume value:
```
This is a filter to consider just the candles with a bigger volume than the mean volume of a determined amount of candles
```bash
Enter the rsi value to consider (30 recomended):
```
The RSI value is a indicator for some strategies in crypto-trading, so it also can be modificated as a superior limit (the script can be easily changeable)

```bash
Enter the name of the symbol, ex BTCUSDT:
```
The symbol of the crypto-currency from which we want the signals.
```bash
Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m 
```
This is the interval of time between each analysis of the bot. For example, if we choose 1h, the bot will download an historical data to predict if to buy or not, every hour. 
```bash
Enter the slope to take in reference, (0 recomended):
```
The slope of the close value of the candels indicates if the market (in this sequence) is bullish or bearish.




# messenger_h_rsi.py
## Description
Here we have a signal bot trading, that using [telegram](https://python-telegram-bot.readthedocs.io/en/stable/) sends signals obtained 
from some technical analysis, taking in count the slope of the candels (rising or falling market, this is adjusted to falling market but it can be easily changed), the rsi value and the volume of the last candels. If the strategy set fits with the sequence obtained with the [Binance](https://resilient-quant-trader.medium.com/scraping-crypto-currency-historical-data-from-binance-using-python-9c0e77c04df7) library.
## Must install
[Pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/install/) and [scipy](https://scipy.org/install/) libraries are used to work with data frames and lists. 

Will use [bina.py](https://github.com/elbernaderen/machine-learning-signal-finder#binapy) to download the actualized data to make the prediction. 
Also need [yaml](https://pypi.org/project/PyYAML/) to save and read the api data in a yml file.
## Usage:
As this bot use Telegram to send messagess, we'll need the user id of the receiver and the API key from the count of telegram that we'll use, and this data will be set in the yml file **telconfig** that is in the ignore folder. 
We must be call the program in console as continue:

```bash
py messenger_h_rsi.py
```
Then the program will ask to enter the next variables:
```bash
Enter the number of candels (X) considered in the model for the prediction:
```
The number of candels that will be used to make the prediction, must be equal to the number used in the [model](https://github.com/elbernaderen/machine-learning-signal-finder#amplitudespy) 
```bash
Enter the amount of periods for rsi calculation (14 recomended):
```
A period for rsi calculation can be better for a candle interval analysis, and not for other one, so, it can be modificated if want it

```bash
Enter how much to increase the mean volume value:
```
This is a filter to consider just the candles with a bigger volume than the mean volume of a determined amount of candles
```bash
Enter the rsi value to consider (30 recomended):
```
The RSI value is a indicator for some strategies in crypto-trading, so it also can be modificated as a superior limit (the script can be easily changeable)

```bash
Enter the name of the symbol, ex BTCUSDT:
```
The symbol of the crypto-currency from which we want the signals.
```bash
Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m 
```
This is the interval of time between each analysis of the bot. For example, if we choose 1h, the bot will download an historical data to predict if to buy or not, every hour. 
```bash
Enter the slope to take in reference, (0 recomended):
```
The slope of the close value of the candels indicates if the market (in this sequence) is bullish or bearish.








# bina.py
## Description
This script contains **store_ohlcv** function, that is used to download the Crypto-currency Historical Data.
## Must install
[Binance](https://resilient-quant-trader.medium.com/scraping-crypto-currency-historical-data-from-binance-using-python-9c0e77c04df7) library to download Crypto-currency Historical Data and [pandas](https://pandas.pydata.org/) to work with data frames. 
Also need [yaml](https://pypi.org/project/PyYAML/) to save and read the api data in a yml file.
## Usage:
To use it, we need to have a Binance account. If you don't have one, can create a account following [this](https://www.binance.com/es/activity/referral-entry?fromActivityPage=true&ref=LIMIT_MYXYAGGF) and by doing that will be my refered and also colaborate with this project. Once that you have an account, you need to generate an API, as [follows](https://resilient-quant-trader.medium.com/scraping-crypto-currency-historical-data-from-binance-using-python-9c0e77c04df7). Then, have to set the API_key and the API_ secret in the config yml file located in the ignore folder.

# call_bina.py
Interface to download the Crypto-currency Historical Data to use them as base for [amplitudes.py](https://github.com/elbernaderen/machine-learning-signal-finder#amplitudespy) or to make a backtest with [backtest_amplitudes.py](https://github.com/elbernaderen/machine-learning-signal-finder#backtest_amplitudespy).
## Description
This script calls the function **store_ohlcv** from [bina.py](https://github.com/elbernaderen/machine-learning-signal-finder#binapy), that is used to download the Crypto-currency Historical Data, setting the name of the Crypto-currency in capital letters, name of the file that will be created, year, month and day since when take in count.
## Usage:
To download a Crypto-currency Historical Data for [amplitudes.py](https://github.com/elbernaderen/machine-learning-signal-finder#amplitudespy) and a Crypto-currency, for example ETHUSDT since a determinated date, must be called the program in console as continue:

```bash
py call_bina.py ETHUSDT base 2019 1 1
```
To download a Crypto-currency Historical Data for [backtest_amplitudes.py](https://github.com/elbernaderen/machine-learning-signal-finder#backtest_amplitudespy) and a Crypto-currency, for example  BTCUSDT since a determinated date, must be called the program in console as continue:
```bash
py call_bina.py BTCUSDT backtest 2022 3 5
```
# References:
* [Scraping Crypto-currency Historical Data from Binance using python](https://resilient-quant-trader.medium.com/scraping-crypto-currency-historical-data-from-binance-using-python-9c0e77c04df7)
* [RSI value](https://programmerclick.com/article/34731200625/) 
* [macd with PANDAS](https://www.alpharithms.com/calculate-macd-python-272222/)
# license:
MIT [Bernardo Derendinger](https://github.com/elbernaderen)

# Disclaimer:
This project is for informational purposes only. You should not construe any such information or other material as legal, tax, investment, financial, or other advice. Nothing contained here constitutes a solicitation, recommendation, endorsement, or offer by me or any third party service provider to buy or sell any securities or other financial instruments in this or in any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such jurisdiction.

If you plan to use real money, USE AT YOUR OWN RISK.

Under no circumstances will I be held responsible or liable in any way for any claims, damages, losses, expenses, costs, or liabilities whatsoever, including, without limitation, any direct or indirect damages for loss of profits.
