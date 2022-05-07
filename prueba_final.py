import sys
import pandas as pd
import datetime
import winsound
import time
from tools import name_col,RSI,macd,name_col_2
#from bina import store_ohlcv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
from scipy.stats import linregress 
p = 15
periods = 14
<<<<<<< HEAD
#a=2
=======
a=2
>>>>>>> d49fae0c608cf41b1495c7add2e885d6cbff2626
rsi_=30
# in_ is the number of candles we consider to know if the price rises or fall
in_ = 6
def actual(file):
    index_ = name_col(p,in_)
    index_.extend(["date","close","vale"])
    index_.extend(name_col_2(in_))
    print(len(index_))
    new = pd.DataFrame(columns = index_)
    X = [x for x in range(0,p-in_)]

    for i in range(p,len(file)):
        Y = [file["close"][t] for t in range(i-p,i-in_)]
        slope,intercept, r_value, p_value_2, std_err = linregress(X, Y)
        row = list()
        vale = 0
        vol = [file["volume"][i-x] for x in range(in_ ,p+1)]
        vol_prom = np.mean(vol)
<<<<<<< HEAD
        #(file["volume"][i-in_-1]> vol_prom * a or file["volume"][i-in_]> vol_prom * a) and 
        if slope < -.001 and file["rsi"][i-in_] < rsi_:
=======
        if (file["volume"][i-in_-1]> vol_prom * a or file["volume"][i-in_]> vol_prom * a) and slope < -.005 and file["rsi"][i-in_] < rsi_:
>>>>>>> d49fae0c608cf41b1495c7add2e885d6cbff2626
            vale = 1
        for t in range(in_ ,p+1):
            #row.append(file["open"][i-t] / file["close"][i-p])
            #row.append(file["high"][i-t] / file["close"][i-p])
           # row.append(file["low"][i-t] / file["close"][i-p])
            #row.append(file["close"][i-t] / file["close"][i-p])
            row.append(file["volume"][i-t] / float(file["volume"][i-p]))
            row.append((file["open"][i-t] - file["close"][i-t]) / file["low"][i-t])
            row.append((file["close"][i-t] - file["open"][i-t]) / file["high"][i-t])
            row.append((file["high"][i-t]) / (file["low"][i-t]))
            row.append(file["rsi"][i-t])
            row.append(file["macd"][i-t])
            row.append(file["macd_h"][i-t])
            row.append(file["macd_s"][i-t])
        row.extend([file["date"][i-in_],file["close"][i-in_], vale])
        for t in reversed(range(in_)):
            row.append((file["high"][i-t] - file["close"][i-in_]) / file["close"][i-in_])
        for t in reversed(range(in_)):
            row.append((file["low"][i-t] - file["close"][i-in_]) / file["close"][i-in_])
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


def pred(row,col,rfc):
    rfc = rfc
    new = pd.DataFrame(columns = col)
    new = new.append(row,ignore_index=True)
    index_ = name_col(p,in_)
    response = float(rfc.predict(new[index_]))
    return response
columns_down = ["date","close"]
columns_down.extend(name_col_2(in_))
columns_down.extend(["vale"])

df_down = df_actual[columns_down]
for nam in range(2,len(sys.argv)):
    print(str(sys.argv[nam]))
    exc = str(sys.argv[nam])
    filename = f'{exc}.sav'
    rfc = pickle.load(open(filename, 'rb'))
    df_down[f"{exc}"] =  df_actual.apply(lambda row: pred(row,df_actual.columns,rfc), axis = 1)
st = str(datetime.datetime.now())

df_down.to_excel(f"{name}{st[0:13]}.xlsx", sheet_name='NUMBERS')
