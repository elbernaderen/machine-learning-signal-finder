import sys
import pandas as pd
import datetime
import time
from bina.bina import store_ohlcv
import pickle
import telegram
from tools.tools import RSI, name_col, macd
import numpy as np
from scipy.stats import linregress
import yaml

######################################################################################################
# PROGRAM DEFINITIONS

# Telegram user id and api_key

config = yaml.load(open("ignore/telconfig.yml"), Loader=yaml.FullLoader)

api_key = config["api_key"]
user_id = config["user_id"]

bot = telegram.Bot(token=api_key)

# Number of candels to consider for the prediction

rows = int(
    input(
        "Enter the number of candels (X) considered in the model for the prediction: \n"
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

# interval_ will save the interval value, and inter_ will be changing in the while loop.

interval_ = inter_  

######################################################################################################

######################################################################################################
# MAIN PROGRAM

# First we open the .sav file with the model generated with amplitudes
#  which name was entered as an argument, using pickle

exc_1 = str(sys.argv[1])
filename_1 = f"{exc_1}.sav"
rfc_1 = pickle.load(open(filename_1, "rb"))

def main():

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
                symbol = name, 
                interval = interval,
                start_date = tt, 
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

        # Then, the df must be edited and the RSI and macd columns must be appended

        # rsi is a list with each candel RSI value

        rsi = RSI(file["close"], periods)

        # Here the RSI list is added to the dataframe file

        file["rsi"] = rsi

        # The macd function receives a DataFrame and add to it the
        # macd, macd_h and macd_s columns

        file = macd(file)

        # Here we delete the first 95 columns because the firts RSI values are 
        # erroneous

        file.drop(index=file.index[:95], axis=0, inplace=True)

        # Reset the index after the first 95 rows are been deleted

        file = file.reset_index()

        # Generate a list to analize the slope with linear regression whit the close values

        Y = [file["close"][t] for t in range(len(file) - rows, len(file))]

        # The slope of the candels is calculated

        slope, intercept, r_value, p_value_2, std_err = linregress(X, Y)

        # generate a list with every volume value of the rows

        vol = [file["volume"][x] for x in range(len(file) - rows, len(file))]

        # calculate the mean value of the volume list

        vol_prom = np.mean(vol)

        # Here we call the function make_prediction that receive a DataFrame
        #  and return a one row df with the technical indicators of n = rows candles.

        new = make_prediction(file)

        # Here we calculate the prediction using the model rfc_1 and the one row DataFrame new,
        # where the columns date and close are dropped

        response_new = rfc_1.predict(new.drop(columns=["date", "close"]))

        # This print in console the response of the model, 
        # that can be 0 or the value predicted with amplitudes.py (buy_decide)

        print(response_new, new["date"], " ", new["close"])

        # 

        coef_1 = float(response_new)
        
        # Here we apply the filter diffined before. 
        # Then, if the data fit the filter and 
        # the response of the predictor is bigger than 0,
        #  the bot sends a message by Telegram with:
        #  PRICE 
        # TAKEPROFIT 
        # STOPLOSS 
        # ZERO LOSS PRICE 
        # DATE

        if (
            coef_1 > 0
            and slope < -0.01
            and (
                file["volume"][len(file) - 1] > vol_prom * a
                or file["volume"][len(file) - 2] > vol_prom * a
            )
            and file["rsi"][len(file) - 1] < rsi_compare
        ):
            coef = coef_1
            t = f'{name} \n BUY: {float(new["close"])} \n TAKEPROFIT: {float(new["close"])*(1+coef)} \n STOPLOSS: {float(new["close"])*(1-.005)} \n cero: {float(new["close"])*(1+0.0015)} \n {datetime.datetime.now()} '
            print(t)
            bot.send_message(chat_id=user_id, text=t)

        # If the price or the values don't fit the filter, 
        # a message is sent through Telegram to wait until the next analysis
        else:
            t = f"{name}  \n don't buy, wait {inter_}"
            print(t)

        time.sleep(inter_)

######################################################################################################

######################################################################################################
# FUNCTIONS
    
def make_prediction(file):

    # this function generates a row with the candels choosen, so the predictor can make the prediction

    index_ = name_col(rows)
    index_.append("date")
    index_.append("close")
    new = pd.DataFrame(columns = index_)
    i = len(file) - 1
    row = list()
    for t in range(rows + 1):
        # volume relation normalized with the first element of the row
        row.append(file["volume"][i - t] / float(file["volume"][i - rows]))
        # value amplitude relation 1
        row.append(
            (file["open"][i - t] - file["close"][i - rows]) / file["low"][i - rows]
        )
        # value amplitude relation 2
        row.append(
            (file["close"][i - t] - file["open"][i - rows]) / file["high"][i - rows]
        )
        # value amplitude relation 3
        row.append((file["high"][i - t]) / (file["low"][i - rows]))
        row.append(file["rsi"][i - t])
        row.append(file["macd"][i - t])
        row.append(file["macd_h"][i - t])
        row.append(file["macd_s"][i - t])
    row.extend([file["date"][i], file["close"][i]])
    new.loc[1] = row
    return new

main()

######################################################################################################
