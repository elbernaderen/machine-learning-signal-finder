import sys
import pandas as pd
import datetime

from tools.tools import name_col, RSI, macd, name_col_2

from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
from scipy.stats import linregress

######################################################################################################
# PROGRAM DEFINITIONS

# in_ is the number of candles we consider to know if the price rises or fall

in_ = int(
    input(
        "Enter the number of candels (Y) considered in the model for the prediction: \n"
    )
)
rows = int(
    input(
        "Enter the number of candels (X) considered in the model for the prediction:: \n"
    )
)
periods = int(
    input("Enter the amount of periods for rsi calculation (14 recomended): \n")
)
a = int(
    input("Enter how much to increase the mean volume value: \n")
    )
rsi_ = int(
    input("Enter the rsi value to consider (30 recomended): \n")
    )
nam = input("Enter the name of the symbol, ex BTCUSDT:\n")
interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")
slope_ = int(
    input("Enter the slope to take in reference, (0 recomended):\n")
    )
p = rows + in_
# in_ is the number of candles we consider to know if the price rises or fall

######################################################################################################

######################################################################################################
# MAIN PROGRAM 
 # file is a DataFrame created since the csv file with the historical Crypto-currency data

 # file is a DataFrame created since the csv file with the historical Crypto-currency data

file = pd.read_csv(f"prueba/{nam}_30m__backtest.csv")

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

# Once we have the DataFrame with the technical indicators, we call backtest function

df_actual = backtest_prepare(file)


columns_down = ["date", "close"]
columns_down.extend(name_col_2(in_))
columns_down.extend(["vale"])

df_down = df_actual[columns_down]

# if are there more than one model of predictor

for na_sav in range(1, len(sys.argv)):

    print(str(sys.argv[na_sav]))
    exc = str(sys.argv[na_sav])
    filename = f"{exc}.sav"
    rfc = pickle.load(open(filename, "rb"))
    df_down[f"{exc}"] = df_actual.apply(
        lambda row: pred(row, df_actual.columns, rfc), axis=1
    )

st = str(datetime.datetime.now())

df_down.to_excel(f"data/{nam}_amp_{st[0:13]}.xlsx", sheet_name="NUMBERS")

######################################################################################################

######################################################################################################
# FUNCTIONS

def pred(row, col, rfc):
    rfc = rfc
    new = pd.DataFrame(columns=col)
    new = new.append(row, ignore_index=True)
    index_ = name_col(p, in_)
    response = float(rfc.predict(new[index_]))
    return response

def backtest_prepare(file):
    index_ = name_col(rows)
    index_.extend(["date", "close", "vale"])
    index_.extend(name_col_2(in_))
    print(len(index_))
    new = pd.DataFrame(columns=index_)
    X = [x for x in range(0, p - in_)]
    for i in range(p, len(file)):
        Y = [file["close"][t] for t in range(i - p, i - in_)]
        slope, intercept, r_value, p_value_2, std_err = linregress(X, Y)
        row = list()
        vale = 0
        vol = [file["volume"][i - x] for x in range(in_, p + 1)]
        vol_prom = np.mean(vol)
        K = len(file)
        if (
            slope < slope_
            and (
                file["volume"][K - 2] > vol_prom * a
                or file["volume"][K - 1] > vol_prom * a
            )
            and 
            (file["rsi"][i - in_] < rsi_ or file["rsi"][i - in_ - 1] < rsi_)
            ):
            vale = 1
        for t in range(in_, p + 1):
            row = row + [
                file["volume"][i - t] / float(file["volume"][i - p]),
                (file["open"][i - t] - file["close"][i - t]) / file["low"][i - t],
                (file["close"][i - t] - file["open"][i - t]) / file["high"][i - t],
                (file["high"][i - t]) / (file["low"][i - t]),
                file["rsi"][i - t],
                file["macd"][i - t],
                file["macd_h"][i - t],
                file["macd_s"][i - t],
            ]

        row = row + [file["date"][i - in_], file["close"][i - in_], vale]
        for t in reversed(range(in_)):
            row = row + [
                (file["high"][i - t] - file["close"][i - in_]) / file["close"][i - in_]
            ]
        for t in reversed(range(in_)):
            row = row + [
                (file["low"][i - t] - file["close"][i - in_]) / file["close"][i - in_]
            ]
        new.loc[i] = row
    return new

######################################################################################################