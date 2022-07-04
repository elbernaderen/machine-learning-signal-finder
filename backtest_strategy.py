import pandas as pd
import datetime
from tools.tools import RSI, name_col_2, macd
import numpy as np
from scipy.stats import linregress

######################################################################################################
# PROGRAM DEFINITIONS

# in_ is the number of candles we consider to know if the price rises or fall

in_ = int(input("Enter the number of candels (Y) that come after the prediction: \n"))

# Number of candels to consider for the prediction

rows = int(
    input("Enter the number of candels (X) considered for the technical analysis: \n")
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

# temp is the interval to consider, ex: 1d or 1h or 30m or 15m or 5m for each candlestick

interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")

# slope_ will be used to compare the candels slope (if it is negative is falling
#  and if it is positive is rising) 

slope_ = int(
    input("Enter the slope to take in reference, (0 recomended):\n"
    )
)
p = rows + in_

######################################################################################################

######################################################################################################
# MAIN PROGRAM 

# file is a DataFrame created since the csv file with the historical Crypto-currency data

file = pd.read_csv(f"prueba/{name}_{interval}_backtest.csv")

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

df_actual = backtest(file)

# Here we generate the list with the columns of the DataFrame that will be download
# name_col_2 is function that generates the names of the columns with the higher and lowest value
# of each candle predicted
  
index_ = name_col_2(in_)

index_.extend(["date", "close", "rsi", "VOLUME", "vale"])

df_down = df_actual[index_]

# To assign a name of the spread sheet file we use some variables and the date and hour when it was created

st = str(datetime.datetime.now())

# A .xlsx file is download in the data folder

df_down.to_excel(f"data/{name}_stg_{st[0:13]}_{rsi_compare}.xlsx", sheet_name="NUMBERS")

######################################################################################################

######################################################################################################
# FUNCTIONS

def backtest(file):
    # backtest requires a DataFrame and use the values defined before
    
    # Generate the  x-axis list to analize the slope with linear regression from cero to rows
    X = [x for x in range(0, rows)]

    # Name the columns for each candle

    index_ = name_col_2(in_)

    # Add name the columns for each final row

    index_.extend(["date", "close", "rsi", "VOLUME", "macd_h", "vale"])

    # The DataFrame that will be filled with the Backtest is created

    new = pd.DataFrame(columns=index_)

    for i in range(rows + in_, len(file)):
        # Generate the y-axis list to analize the slope with linear regression from cero to rows candels close values
        Y = [file["close"][t] for t in range(i - p, i - in_)]
        slope, intercept, r_value, p_value_2, std_err = linregress(X, Y)
        row = list()

        # satisfy is a variable that shows if the sequence pass the filter, 
        # it will be 1 if the conditions are the required and 0 if they don't

        satisfy = 0

        vol = [file["volume"][i - x] for x in range(in_, rows + in_ + 1)]
        vol_prom = np.mean(vol)

        # Here the predicted consecutive candles are added, so we can know 
        # if the price rises or fall

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

        # Here is the filter to asign a value to satisfy

        if (
            slope < slope_
            and (
                file["volume"][i - in_] > vol_prom * a
                or file["volume"][i - in_ - 1] > vol_prom * a
            )
            and (
                file["rsi"][i - in_] < rsi_compare
                or file["rsi"][i - in_ - 1] < rsi_compare
                or file["rsi"][i - in_ - 2] < rsi_compare
            )
        ):
            satisfy = 1
        row.append(satisfy)

        new.loc[i] = row
    return new

######################################################################################################