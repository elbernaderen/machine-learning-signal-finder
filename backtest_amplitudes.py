import sys
import pandas as pd
import datetime

from tools.tools import name_col, RSI, macd, name_col_2,edit_df

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
# Number of candels to consider for the prediction

rows = int(
    input(
        "Enter the number of candels (X) considered in the model for the prediction:: \n"
    )
)

# The relative strength index (RSI) is a momentum indicator
# used in technical analysis that measures the magnitude 
# of recent price changes to evaluate overbought or oversold 
# conditions in the price of a stock or other asset 
# The number of the previous candlesticks (periods) is the main setting 
# of the indicator called a period. By default Period = 14; this is the value the author used.

periods = int(
    input("Enter the amount of periods for rsi calculation (14 recomended): \n")
)

# a will allow us know if the volume of the candels is "a" times bigger than the mean volume
# of the previus candels

# name of the Crypto-currency to analyze

name = input("Enter the name of the symbol, ex BTCUSDT:\n")

# interval is the interval to consider, ex: 1d or 1h or 30m or 15m or 5m for each candlestick

interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")

# vol_p is the number that will be used to calculate the volume mean

vol_p = int(input("Enter how many candels to consider if the market is ascending or descending: \n"))

# p represents all the candles involved

p = rows + in_


######################################################################################################

######################################################################################################
# MAIN PROGRAM 

def main():

    # file is a DataFrame created since the csv file with the historical Crypto-currency data

    file = pd.read_csv(f"backtest/{name}_30m_backtest.csv")

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

    # Once we have the DataFrame with the technical indicators, we call backtest_prepare function
    # that generates

    df_actual = backtest_prepare(file)

    columns_down = ["date"]
    columns_down.extend(name_col_2(in_))


    df_down = df_actual[columns_down]

    # if are there more than one model of predictor

    df_actual, list_dummies= edit_df(df_actual, rows, prop = 2)

    df_predict = pd.get_dummies(df_actual[list_dummies])
    

    for na_sav in range(1, len(sys.argv)):

        print(str(sys.argv[na_sav]))

        exc = str(sys.argv[na_sav])
        filename = f"{exc}.sav"
        rfc = pickle.load(open(filename, "rb"))
        
        df_down[f"{exc}"] = pd.to_numeric(rfc.predict(df_predict))

    st = str(datetime.datetime.now())

    df_down.to_excel(f"data/{name}_amp_{st[0:13]}.xlsx", sheet_name="NUMBERS")

######################################################################################################

######################################################################################################
# FUNCTIONS

def backtest_prepare(file):
    index_ = name_col(rows,4)

    index_.extend(name_col_2(in_))

    df = pd.DataFrame(columns=index_)

    X = [x for x in range(0, rows)]
    X_long = [x for x in range(0, vol_p)]

    for i in range(p + vol_p, len(file)):

        # Generate the y-axis list to analize the slope with linear regression from cero to rows candels close values

        Y_long = [file["close"][t] for t in range(i - vol_p - in_, i - in_)]

        Y = [file["close"][t] for t in range(i - p, i - in_)]

        # The slope of the candels is calculated

        slope_prev_short, intercept, r_value, p_value_2, std_err = linregress(X, Y)
        slope_prev, intercept, r_value, p_value_2, std_err = linregress(X_long, Y_long)

        vol = [file["volume"][i - x] for x in range(in_, in_ + 1 + vol_p)]


        row = list()

        vol_prom = np.mean(vol)

        mean_15 = np.mean([file["close"][t] for t in range(i - 15-in_, i-in_)])
        mean_30 = np.mean([file["close"][t] for t in range(i - 30 - in_, i- in_)])
        mean_60 =  np.mean([file["close"][t] for t in range(i - 60 - in_, i- in_)])
        mean_100 = np.mean([file["close"][t] for t in range(i - 100 - in_, i- in_)])

        mean_rel_15_30 = mean_15 / mean_30
        mean_rel_30_60 = mean_30 / mean_60
        mean_rel_60_100 = mean_60 / mean_100

        for t in range(in_, p + 1):
            row = row + [
                file["volume"][i - t] / float(vol_prom),
                (file["open"][i - t] - file["close"][i - t]) / file["low"][i - t],
                (file["close"][i - t] - file["open"][i - t]) / file["high"][i - t],
                (file["high"][i - t]) / (file["low"][i - t]),
                file["rsi"][i - t],
                file["macd"][i - t],
                file["macd_h"][i - t],
                file["macd_s"][i - t]
                ]

        row = row + [file["date"][i - in_],
                        slope_prev,
                        slope_prev_short,
                        mean_rel_15_30,
                        mean_rel_30_60,
                        mean_rel_60_100]

        for t in reversed(range(in_)):
            row = row + [
                (file["high"][i - t] - file["close"][i - in_]) / file["close"][i - in_]
            ]
        for t in reversed(range(in_)):
            row = row + [
                (file["low"][i - t] - file["close"][i - in_]) / file["close"][i - in_]
            ]
        df.loc[i] = row

    return df

main()
######################################################################################################