import sys
from tkinter import N
import pandas as pd
import datetime
import time
from bina.bina import store_ohlcv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
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
periods = int(
    input("Enter the amount of periods for rsi calculation (14 recomended): \n")
)
a = int(
    input("Enter how much to increase the mean volume value: \n"
    )
)

nam = input("Enter the name of the symbol, ex BTCUSDT:\n")
interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")
slope_ = int(
    input("Enter the slope to take in reference, (0 recomended):\n"
    )
)

# Interval must be seconds, so here we convert hour, day or minutes in seconds
if "d" in interval:
    inter_ = 3600 * 24
    hours = 24 * 150
elif "h" in interval:
    inter_ = 3600
    hours = 150
else:
    interval_ = 60 * int(interval.replace("m", ""))
    hours = 150
    
######################################################################################################

######################################################################################################
# MAIN PROGRAM

# First we open the .sav file with the model generated with amplitudes
#  which name was entered as an argument, using pickle

exc_1 = str(sys.argv[1])
filename_1 = f"{exc_1}.sav"
rfc_1 = pickle.load(open(filename_1, "rb"))

# Generate the  x-axis list to analize the slope with linear regression from cero to rows

X = [x for x in range(0, rows)]

while True:
    
    # The signal finder is activated, and it will keep working
    # according to the interval choosed

    inter_ = interval_
    hour = datetime.timedelta(hours = hours)
    hour_ = datetime.datetime.utcnow()
    tt = hour_ - hour
    try:
        kk = store_ohlcv(
            symbol=nam, 
            interval = interval,
            start_date = tt, 
            name = "_mensajero"
        )
    except ConnectionError:
        time.sleep(60)
        inter_ -= 60
        print("check your internet connection\n")
        kk = store_ohlcv(
            symbol=nam, interval=interval, start_date=tt, name="mensajero"
        )
    # wait to download the csv file
    time.sleep(30)
    inter_ -= 30

    file = pd.read_csv(f"mensajero/{nam}_{interval}_mensajero.csv")
    rsi = RSI(file["close"], periods)
    file["rsi"] = rsi
    file = macd(file)
    file.drop(index=file.index[:95], axis=0, inplace=True)
    file = file.reset_index()
    rsi = RSI(file["close"], periods)
    file["rsi"] = rsi
    # Generate a list to analize the slope with linear regression whit the close values
    Y = [file["close"][t] for t in range(len(file) - rows, len(file))]
    slope, intercept, r_value, p_value_2, std_err = linregress(X, Y)
    # generate a list with every volume value of the rows
    vol = [file["volume"][x] for x in range(len(file) - rows, len(file))]
    # calculate the mean value of the volume list
    vol_prom = np.mean(vol)
    new = make_prediction(file)
    response_1 = rfc_1.predict(new.drop(columns=["date", "close"]))

    print(response_1, new["date"], " ", new["close"])
    coef_1 = float(response_1)
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
        t = f'{nam} \n BUY: {float(new["close"])} \n TAKEPROFIT: {float(new["close"])*(1+coef)} \n STOPLOSS: {float(new["close"])*(1-.005)} \n cero: {float(new["close"])*(1+0.0015)} \n {datetime.datetime.now()} '
        print(t)
        bot.send_message(chat_id=user_id, text=t)
    else:
        t = f"{nam}  \n don't buy, wait {interval}"
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
    new = pd.DataFrame(columns=index_)
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



