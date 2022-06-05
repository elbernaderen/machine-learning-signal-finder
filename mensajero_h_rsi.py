#import sys
from tkinter import N
import pandas as pd
import datetime
import time
from bina import store_ohlcv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import telegram
from tools import RSI
import numpy as np
from scipy.stats import linregress
import yaml

config = yaml.load(open('ignore/telconfig.yml'), Loader=yaml.FullLoader)
# Telegram configuration
api_key = config['api_key']
user_id = config['user_id']
bot = telegram.Bot(token=api_key)

rows =int(input("Enter the number of candels to analize: \n"))
periods = int(input("Enter the amount of periods for rsi calculation (14 recomended): \n"))
a = int(input("Enter how much to increase the mean volume value: \n"))
rsi_ = int(input("Enter the rsi value to consider (30 recomended): \n"))
nam = input("Enter the name of the symbol, ex BTCUSDT:\n")
interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")
slope_ = int(input("Enter the slope to take in reference, (0 recomended):\n"))
if "d" in interval:
    inter_ = 3600*24
    hours = 24 * 150
elif "h" in interval:
    inter_ = 3600
    hours = 150
else:
    interval_ = 60 * int(interval.replace("m",""))
    hours = 150
X = [x for x in range(0,rows)]
while True:
    inter_ = interval_
    hour = datetime.timedelta(hours = hours)
    hour_ = datetime.datetime.utcnow()
    tt = hour_ - hour
    try:
        kk = store_ohlcv(symbol = nam, interval = interval, start_date = tt, name="_mensajero")
    except ConnectionError:
        time.sleep(60)
        inter_-=60
        print("check your internet connection\n")
        kk = store_ohlcv(symbol = nam, interval = interval, start_date = tt, name="_mensajero")
    # wait to download the csv file
    time.sleep(30)
    inter_-=30 
    file =  pd.read_csv(f"{nam}_{interval}_mensajero.csv")
    Y = [file["close"][t] for t in range(len(file)-rows,len(file))]
    slope,intercept, r_value, p_value_2, std_err = linregress(X, Y)
    rsi = RSI(file["close"],periods)
    file["rsi"] = rsi
    rsi = RSI(file["close"],periods)
    file["rsi"] = rsi
    file.drop(index=file.index[:95], 
        axis=0, 
        inplace=True)
    file = file.reset_index()
    K = len(file)
    coef = float(file["close"][len(file) - 1])
    vol =  [file["volume"][x] for x in range(len(file)-rows,len(file))]
    vol_prom = np.mean(vol)
    if (file["volume"][K - 2]> vol_prom * a or file["volume"][K - 1] > vol_prom * a) and slope < slope_ and file["rsi"][K - 1] < rsi_:
        t= f'{nam}  \n BUY: {coef} \n STOPLOSS: {coef*(1-0.01)} \n \n cero: {coef*(1+0.0015)} \n {datetime.datetime.now()} '
        print(t)
        bot.send_message(chat_id=user_id, text=t)
    else:
        t= f"{nam}  \n don't buy, wait {interval}"
        print(t)
    time.sleep(inter_)
        