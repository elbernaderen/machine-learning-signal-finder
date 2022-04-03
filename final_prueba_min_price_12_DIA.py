import sys
import pandas as pd
import datetime
import winsound
import time
from bina import store_ohlcv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import pickle

def name_col(p,in_):
    ind_row = p - in_ + 1
    index_ = list()
    for cin in range(ind_row):
        index_.append(f"open_{cin}")
        index_.append(f"high_{cin}")
        index_.append(f"low_{cin}")
        index_.append(f"close_{cin}")
        index_.append(f"mart_{cin}")
        index_.append(f"mart_inv_{cin}")
        index_.append(f"ampl_1{cin}")
        index_.append(f"ampl_2{cin}")
    return index_
p = 15
in_ = 2
def actual(file):
    index_ = name_col(p,in_)
    index_.extend(["date","close","salida_1","salida_2","salida_m1","salida_m2"])
    print(len(index_))
    new = pd.DataFrame(columns = index_)
    for i in range(p,len(file)):
        row = list()
        for t in range(in_ ,p+1):
            row.append(file["open"][i-t] / file["close"][i-p])
            row.append(file["high"][i-t] / file["close"][i-p])
            row.append(file["low"][i-t] / file["close"][i-p])
            row.append(file["close"][i-t] / file["close"][i-p])
            row.append((file["open"][i-t] - file["close"][i-t]) / file["low"][i-t])
            row.append((file["close"][i-t] - file["open"][i-t]) / file["high"][i-t])
            row.append((file["open"][i-t] - file["close"][i-t]) / (file["high"][i-t]-file["low"][i-t]))
            row.append((file["high"][i-t]) / (file["low"][i-t]))
        row.extend([file["date"][i-in_],file["close"][i-in_],
                (file["high"][i-1] - file["close"][i-2]) / file["close"][i-2],
                (file["high"][i] - file["close"][i-2]) / file["close"][i-2],
                (file["low"][i-1] - file["close"][i-2]) / file["close"][i-2],
                (file["low"][i] - file["close"][i-2]) / file["close"][i-2]])
        new.loc[i] = row
    return new


name = str(sys.argv[1])
file =  pd.read_csv(f"{name}_1d_prueba.csv") 
df_actual = actual(file)


def pred(row,col,rfc):
    rfc = rfc
    new = pd.DataFrame(columns = col)
    new = new.append(row,ignore_index=True)
    index_ = name_col(p,in_)
    response = rfc.predict(new[index_])
    return response
columns_down=["date","close","salida_1","salida_2","salida_m1","salida_m2"]
df_down = df_actual[columns_down]
for nam in range(2,len(sys.argv)):
    print(str(sys.argv[nam]))
    exc = str(sys.argv[nam])
    filename = f'{exc}.sav'
    rfc = pickle.load(open(filename, 'rb'))
    df_down[f"{exc}"] =  df_actual.apply(lambda row: pred(row,df_actual.columns,rfc), axis = 1)
st = str(datetime.datetime.now())

df_down.to_excel(f"{name}{st[0:13]}.xlsx", sheet_name='NUMBERS')