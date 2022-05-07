import sys
import pandas as pd
import datetime
import time
from tools import RSI, name_col_2,macd
#from bina import store_ohlcv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
from scipy.stats import linregress

periods = 14
p = 11
in_ = 4
b = 1
a=3
rsi_=30
def actual(file):
    X = [x for x in range(0,p-in_)]
    index_ = name_col_2(in_)
    index_.extend(["date","close","rsi","VOLUME","macd_h","vale"])
    new = pd.DataFrame(columns = index_)
    for i in range(p,len(file)):
        Y = list()
        for t in range(i-p,i-in_):
            Y.append(file["close"][t])
        slope,intercept, r_value, p_value_2, std_err = linregress(X, Y)
        row = list()
        vale = 0
        vol = [file["volume"][i-x] for x in range(in_ ,p+1)]
        vol_max =  max(vol)
        vol_prom = np.mean(vol)
        for t in reversed(range(in_)):
            row.append((file["high"][i-t] - file["close"][i-in_]) / file["close"][i-in_])
        for t in reversed(range(in_)):
            row.append((file["low"][i-t] - file["close"][i-in_]) / file["close"][i-in_])
        row.append(file["date"][i-in_])
        row.append(file["close"][i-in_])
        row.append(file["rsi"][i-in_])
        row.append(file["volume"][i-in_])
        row.append(file["macd_h"][i-in_])

        if slope < 0 and (file["volume"][i-in_] > vol_prom * a or file["volume"][i-in_-1] > vol_prom * a) and (file["rsi"][i-in_] < rsi_ or file["rsi"][i-in_- 1] < rsi_ or file["rsi"][i-in_-2] < rsi_):
            vale = 1
        row.append(vale)
        new.loc[i] = row
    return new


name = str(sys.argv[1])
file =  pd.read_csv(f"{name}_30m_prueba.csv") 
rsi = RSI(file["close"],periods)
file["rsi"] = rsi
file = macd(file)
file.drop(index=file.index[:95], 
    axis=0, 
    inplace=True)
file = file.reset_index()
df_actual = actual(file)
index_ = name_col_2(in_)
index_.extend(["date","close","rsi","VOLUME","vale"])

df_down = df_actual[index_]

st = str(datetime.datetime.now())

df_down.to_excel(f"{name}_{a}_{b}_{rsi_}.xlsx", sheet_name='NUMBERS')
