import sys
from tkinter import N
import pandas as pd
import datetime
import winsound
import time
from bina import store_ohlcv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import pickle
import telegram
from tools import RSI,name_col,macd
import numpy as np
from scipy.stats import linregress

api_key = '5187902884:AAHN_f_MFNHLwX_50X7Gu2LPJDOrlZPCkoY'
user_id = '1883463708'

bot = telegram.Bot(token=api_key)

p = 9
in_ = 2
rows = 7
periods = 14
a=4
rsi_=30
def make_prediction(file):
    index_ = name_col(p,in_)
    index_.append("date")
    index_.append("close")
    new = pd.DataFrame(columns = index_)                            
    i = len(file)-1
    row = list()
    for t in range(rows+1):
        row.append(file["volume"][i-t] / float(file["volume"][i-rows]))
        row.append((file["open"][i-t] - file["close"][i-rows]) / file["low"][i-rows])
        row.append((file["close"][i-t] - file["open"][i-rows]) / file["high"][i-rows])
        row.append((file["high"][i-t]) / (file["low"][i-rows]))
        row.append(file["rsi"][i-t])
        row.append(file["macd"][i-t])
        row.append(file["macd_h"][i-t])
        row.append(file["macd_s"][i-t])
    row.extend([file["date"][i],file["close"][i]])
    new.loc[1] = row
    return new

nam = str(sys.argv[1])
exc_1 = str(sys.argv[2])

filename_1 = f'{exc_1}.sav'
rfc_1 = pickle.load(open(filename_1, 'rb'))
X = [x for x in range(0,p-in_)]
while True:
    hour = datetime.timedelta(hours = 100)
    hour_ = datetime.datetime.utcnow()
    tt = hour_- hour
    print(tt)
    try:
        kk = store_ohlcv(symbol = nam,interval='30m',start_date = tt,name="_mensajero")
    except ConnectionError:
        time.sleep(60)
        kk = store_ohlcv(symbol = nam,interval='30m',start_date = tt,name="_mensajero")
    time.sleep(30)
    file =  pd.read_csv(f"{nam}_30m_mensajero.csv")
    

    rsi = RSI(file["close"],periods)
    file["rsi"] = rsi
    file = macd(file)
    file.drop(index=file.index[:95], 
    axis=0, 
    inplace=True)
    file = file.reset_index()
    rsi = RSI(file["close"],periods)
    file["rsi"] = rsi
    Y = list()
    for t in range(len(file)-rows,len(file)):
        Y.append(file["close"][t])
    slope,intercept, r_value, p_value_2, std_err = linregress(X, Y)
    vol = 0
    for t in range(len(file)-rows,len(file)):
        
        Y.append(file["close"][t])
    vol_prom = vol/(p+in_)
    new = make_prediction(file)
    response_1 = rfc_1.predict(new.drop(columns = ["date","close"]))  

    print(response_1,new["date"]," ",new["close"])
    coef_1 = float(response_1)
    print(coef_1)
    if coef_1 > 0 and slope < -0.01 and (file["volume"][len(file)-1]> vol_prom * a or file["volume"][len(file)-2]> vol_prom * a) and file["rsi"][len(file)-1] < rsi_:
        coef = coef_1
        t= f'{nam} \n BUY: {float(new["close"])} \n TAKEPROFIT: {float(new["close"])*(1+coef)} \n STOPLOSS: {float(new["close"])*(1-.005)} \n cero: {float(new["close"])*(1+0.0015)} \n {datetime.datetime.now()} '
        print(t)
        bot.send_message(chat_id=user_id, text=t)
    time.sleep(1770)
        