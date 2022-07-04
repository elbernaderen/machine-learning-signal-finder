import sys
import pandas as pd
import datetime
import time
from bina.bina import store_ohlcv
import telegram
from tools.tools import RSI
import numpy as np
from scipy.stats import linregress
import yaml

######################################################################################################
# PROGRAM DEFINITIONS

# Telegram user id and api_key

config = yaml.load(open("ignore/telconfig.yml"), Loader=yaml.FullLoader)

# Telegram configuration

api_key = config["api_key"]
user_id = config["user_id"]
bot = telegram.Bot(token=api_key)

# Number of candels to consider for the prediction

rows = int(
    input("Enter the number of candels to analize: \n"
    )
)

# The relative strength index (RSI) is a momentum indicator
# used in technical analysis that measures the magnitude 
# of recent price changes to evaluate overbought or oversold 
# conditions in the price of a stock or other asset 

rsi_compare = int(
    input("Enter the rsi value to consider (30 recomended): \n"
    )
)

# The number of the previous candlesticks (periods) is the main setting 
# of the indicator called a period. By default Period = 14; this is the value the author used.

periods = int(
    input("Enter the amount of periods for rsi calculation (14 recomended): \n")
)

# a will allow us know if the volume of the candels is "a" times bigger than the mean volume
# of the previus candels

a = int(
    input("Enter how much to increase the mean volume value: \n"
    )
)

# name of the Crypto-currency to analyze

name = input("Enter the name of the symbol, ex BTCUSDT:\n")

# interval is the interval to consider, ex: 1d or 1h or 30m or 15m or 5m for each candlestick

interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")

# slope_ will be used to compare the candels slope (if it is negative is falling
#  and if it is positive is rising) 

slope_ = int(
    input("Enter the slope to take in reference, (0 recomended):\n"
    )
)

# The time interval must be seconds, so here we convert hour, day or minutes in seconds

if "d" in interval:
    inter_ = 3600 * 24
    hours = 24 * 150
elif "h" in interval:
    inter_ = 3600
    hours = 150
else:
    inter_ = 60 * int(interval.replace("m", ""))
    hours = 150

interval_ = inter_  

######################################################################################################

######################################################################################################
# MAIN PROGRAM 

# Generate the  x-axis list to analize the slope with linear regression from cero to rows
X = [x for x in range(0, rows)]

while True:
    # The signal finder is activated, and it will keep working
    # according to the interval choosed

    inter_ = interval_

    # To make an analysis and determine if we have to buy or just wait, 
    # we need to download several seconds before the last candle, 
    # so the variable tt will be the start date of the data to download

    hour = datetime.timedelta(hours = hours)
    hour_ = datetime.datetime.utcnow()
    tt = hour_ - hour

    # If at the moment of download the historical data, 
    # the internet is gone, the program will fail. 
    # So we add an Exception 

    try:
        kk = store_ohlcv(
            symbol=name,
             interval=interval, 
             start_date=tt, 
             name = "messenger"
        )

    except ConnectionError:
        # If the internet is gone, we'll wait 60 seconds, and'll try again

        time.sleep(60)

        inter_ -= 60

        print("check your internet connection\n")

        kk = store_ohlcv(
            symbol = name,
            interval = interval,
            start_date = tt,
            name = "messenger"
        )
    # wait to download the csv file
    time.sleep(30)
    inter_ -= 30

    # Every time that pass the interval of established time,
    #  the csv file with the data is download in the "messenger" directory, 
    # and this last file will replace the previous one and a DataFrame will be created

    file = pd.read_csv(f"messenger/{name}_{interval}_messenger.csv")

    # Then, the df must be edited and the RSI column must be appended

    # Generate a list to analize the slope with linear regression whit the close values

    Y = [file["close"][t] for t in range(len(file) - rows, len(file))]

    # The slope of the candels is calculated

    slope, intercept, r_value, p_value_2, std_err = linregress(X, Y)

    # rsi is a list with each candel RSI value

    rsi = RSI(file["close"], periods)

    # Here the RSI list is added to the dataframe file

    file["rsi"] = rsi

    # Here we delete the first 95 columns because the firts RSI values are 
    # erroneous

    file.drop(index=file.index[:95], axis=0, inplace=True)

    # Reset the index after the first 95 rows are been deleted

    file = file.reset_index()

    K = len(file)

    coef = float(file["close"][len(file) - 1])

    # Here a list of all the volume values is set, so we can calculate the mean volume value

    vol = [file["volume"][x] for x in range(K - rows, K)]
    vol_prom = np.mean(vol)

    # Here we apply the filter diffined before. 
    # Then, if the data fit the filter 
    #  the bot sends a message by Telegram with:
    #  PRICE 
    # TAKEPROFIT 
    # STOPLOSS 
    # ZERO LOSS PRICE 
    # DATE

    if (
        (file["volume"][K - 2] > vol_prom * a 
        or file["volume"][K - 1] > vol_prom * a)
        and slope < slope_
        and file["rsi"][K - 1] < rsi_compare
    ):
        t = f"{name}  \n BUY: {coef} \n STOPLOSS: {coef*(1-0.01)} \n \n cero: {coef*(1+0.0015)} \n {datetime.datetime.now()} "
        print(t)
        bot.send_message(chat_id = user_id, text = t)
    # If the price or the values don't fit the filter, 
    # a message is sent through Telegram to wait until the next analysis
    else:
        t = f"{name}  \n don't buy, wait {interval}"
        print(t)

    time.sleep(inter_)

######################################################################################################