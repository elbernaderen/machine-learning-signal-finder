import sys
import pandas as pd
import datetime
import time
from tools.tools import RSI, name_col_2, macd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from scipy.stats import linregress

in_ = int(input("Enter the number of candels (Y) that come after the prediction: \n"))
rows = int(
    input("Enter the number of candels (X) considered for the technical analysis: \n")
)
periods = int(
    input("Enter the amount of periods for rsi calculation (14 recomended): \n")
)
a = int(input("Enter how much to increase the mean volume value: \n"))
rsi_ = int(input("Enter the rsi value to consider (30 recomended): \n"))
name = input("Enter the name of the symbol, ex BTCUSDT:\n")
interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")
slope_ = int(input("Enter the slope to take in reference, (0 recomended):\n"))
p = rows + in_


def actual(file):
    X = [x for x in range(0, rows)]
    index_ = name_col_2(in_)
    index_.extend(["date", "close", "rsi", "VOLUME", "macd_h", "vale"])
    new = pd.DataFrame(columns=index_)
    for i in range(rows + in_, len(file)):
        Y = [file["close"][t] for t in range(i - p, i - in_)]
        slope, intercept, r_value, p_value_2, std_err = linregress(X, Y)
        row = list()
        vale = 0
        vol = [file["volume"][i - x] for x in range(in_, rows + in_ + 1)]
        vol_prom = np.mean(vol)
        for t in reversed(range(in_)):
            row.append(
                (file["high"][i - t] - file["close"][i - in_]) / file["close"][i - in_]
            )
        for t in reversed(range(in_)):
            row.append(
                (file["low"][i - t] - file["close"][i - in_]) / file["close"][i - in_]
            )
        row.append(file["date"][i - in_])
        row.append(file["close"][i - in_])
        row.append(file["rsi"][i - in_])
        row.append(file["volume"][i - in_])
        row.append(file["macd_h"][i - in_])
        if (
            slope < slope_
            and (
                file["volume"][i - in_] > vol_prom * a
                or file["volume"][i - in_ - 1] > vol_prom * a
            )
            and (
                file["rsi"][i - in_] < rsi_
                or file["rsi"][i - in_ - 1] < rsi_
                or file["rsi"][i - in_ - 2] < rsi_
            )
        ):
            vale = 1
        row.append(vale)
        new.loc[i] = row
    return new


file = pd.read_csv(f"prueba/{name}_30m_prueba.csv")
rsi = RSI(file["close"], periods)
file["rsi"] = rsi
file = macd(file)
file.drop(index=file.index[:95], axis=0, inplace=True)
file = file.reset_index()
df_actual = actual(file)
index_ = name_col_2(in_)
index_.extend(["date", "close", "rsi", "VOLUME", "vale"])

df_down = df_actual[index_]

st = str(datetime.datetime.now())

df_down.to_excel(f"data/{name}strategy_{a}_{rsi_}.xlsx", sheet_name="NUMBERS")
