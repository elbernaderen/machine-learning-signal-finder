import sys
import pandas as pd
from tools.tools import name_col, RSI, macd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle
import datetime
import numpy as np
from scipy.stats import linregress


######################################################################################################
# PROGRAM DEFINITIONS

# B is the rise percent of the candles next to the close of the last candle
#  that we use to decide if this sequence anticipate a rise

B = float(
    input(
        "Enter the percentage that have to rise the price to consider it as a success: \n"
    )
)

# in_ is the number of candles we consider to know if the price rises or fall

in_ = int(
    input(
        "Enter the number of candels (Y) to consider in the model for the prediction: \n"
    )
)

# Number of candels to consider for the prediction

rows = int(
    input(
        "Enter the number of candels (X) consider in the model for the prediction: \n"
    )
)

# The relative strength index (RSI) is a momentum indicator
# used in technical analysis that measures the magnitude 
# of recent price changes to evaluate overbought or oversold 
# conditions in the price of a stock or other asset 

rsi_compare = int(input("Enter the rsi value to consider (30 recomended): \n"))

# The number of the previous candlesticks (periods) is the main setting 
# of the indicator called a period. By default Period = 14; this is the value the author used.

periods = int(
    input("Enter the amount of periods for rsi calculation (14 recomended): \n")
)

p = rows + in_

# slope_ will be used to compare the candels slope (if it is negative is falling
#  and if it is positive is rising) 

slope_ = float(input("Enter the slope to take in reference, (0 recomended):\n"))

# interval is the interval to consider, ex: 1d or 1h or 30m or 15m or 5m for each candlestick

interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")

# vol_p is the number that will be used to calculate the volume mean

vol_p = int(input("Enter how many candels consider to calculate the volume mean: \n"))

# a will allow us know if the volume of the candels is "a" times bigger than the mean volume
# of the previus candels

a = int(input("Enter how much to increase the mean volume value: \n"))

# List that'll be filled with the different Crypto-currency used

names = ["LISTA:"]





######################################################################################################

######################################################################################################
# MAIN PROGRAM 

# This for will read each historical Crypto-currency data added as an argument
def main():

    # counter is used in the main program to count the number of historical Crypto-currency data
    # added as argument

    count = 0

    for nam in range(1, len(sys.argv)):

        # file is a DataFrame created since the csv file with the historical Crypto-currency data

        file = pd.read_csv(f"base/{str(sys.argv[nam])}_{interval}_base.csv")

        # rsi is a list with each candel RSI value

        rsi = RSI(file["close"], periods)

        # Here the RSI list is added to the dataframe file

        file["rsi"] = rsi

        # The macd function receives a DataFrame and add to it the
        # macd, macd_h and macd_s columns

        file = macd(file)

        # Here we delete the first 95 columns because the firts RSI values are 
        # erroneous

        file.drop(index = file.index[:95], axis=0, inplace=True)

        # Reset the index after the first 95 rows are been deleted

        file = file.reset_index()
    
        # if it is the first historical Crypto-currency data, then:

        if count == 0:

        # The funtion that generates the rows with the sequence of candels
        # named verify is called.
        # verify requires the DataFrame with the historical Crypto-currency data
        # and returns a DataFrame where each row is a sequence of candels determinated (rows), its
        #  technical indicators (rsi,macd, etc), other parameters like slope and finaly if the consecutives candels (in_)
        # have shown an increase or not (buy_decide) of its value in a the determinated percent (B) 

            v = verify(file)

            count += 1

            # if it's not the first historical Crypto-currency data, then:

        else:

            k = verify(file)

            # After we call verify, we append the new DataFrame of the new historical Crypto-currency data
            # to the previusly generated.

            v = pd.concat([v, k], ignore_index=True)

        # add the name of the historical Crypto-currency in the names list

        names.append(str(sys.argv[nam]))

    y = v.buy

    # columns to use to run the rfc

    features = name_col(rows)

    X = v[features]
 
    X_train, X_test, y_train, y_test = train_test_split(
                                    X, y, test_size=0.2, random_state=10
                                    )

    rfc = RandomForestClassifier(n_estimators=2000)

    rfc.fit(X_train, y_train)

    predictions = rfc.predict(X_test)

    # To assign a name of the predictor model file we use some variables and the date and hour when it was created
    st = str(datetime.datetime.now())

    st = st.replace(" ", "_")

    st = st.replace(":", "_")

    filename_ = f"rows{rows}_periods_{periods}_in_{in_}_{B}_{st[0:16]}.sav"

    # pickle creates a .sav file with the rfc model so we can use it with the backtesting or the messenger,
    # and names it as filename_

    pickle.dump(rfc, open(filename_, "wb"))

######################################################################################################

######################################################################################################
    # RESULTS
    # name of the .sav file

    print(f"model_p_{p}_perio_{periods}_in_{in_}_{B}_{st[0:16]}.sav")

    # name is the list of the historical Crypto-currency data used

    print(names)

    # The classification report allows us to compare the precission, aquracy of different variables 
    # used like B, in_, a also the different historical Crypto-currency data.

    print(classification_report(y_test, predictions))

    # The next information is useful to know which variables were used to obtain 
    # what the classification report indicates

    print(f"periods rsi: {periods}")
    print(f"Y candels: {in_}")
    print(f"Amount that increased the volume: {a}")
    print(f"rows: {rows}")
    print(f"Candels used to calculate volume: {vol_p}")

######################################################################################################

######################################################################################################
# FUNCTIONS

def verify(file):
    # verify requires a DataFrame and use the values defined before

    # create the index of the df

    index_ = name_col(rows)
    index_.append("date")
    index_.append("buy")
    k = pd.DataFrame(columns=index_)

    # Generate the  x-axis list to analize the slope with linear regression from cero to rows

    X = [x for x in range(0, p - in_)]

    for i in range(p + vol_p, len(file.index)):

        # Generate the y-axis list to analize the slope with linear regression from cero to rows candels close values

        Y = [file["close"][t] for t in range(i - p, i - in_)]

        # Here creates a list with the RSI of the candels involved to find the minimun one 
        # and compare with the stablished before

        rsi_list = [file["rsi"][t] for t in range(i - p, i - in_)]

        # The slope of the candels is calculated

        slope, intercept, r_value, p_value_2, std_err = linregress(X, Y)

        # Mean volume calculate

        vol = [file["volume"][i - x] for x in range(in_, p + 1 + vol_p)]

        vol_prom = np.mean(vol)

        buy_decide = 1

        # If the values in the row pass the filter, they are considered to make the predictor model
        # The slope, the volume and the rsi are compared

        if (
            slope < slope_
            and (file["volume"][i - in_] or file["volume"][i - in_ - 1]) > vol_prom * a
            and min(rsi_list) < rsi_compare
        ):
            # hi is the list with variaton of the candles we consider to know if the price rises or fall

            high_candel = [(file["high"][i - t] - file["close"][i - in_]) / file["close"][i - in_] for t in range(in_ + 1)]

            # If the candles that come after to the first candles considered (rows) 
            # are bigger than the B established value, buy decide will be B, otherwise it will be 0

            if max(high_candel) > B:

                buy_decide = f"{B}"

            else:

                buy_decide = "0"

        # either cero or B, if the row was considered, is will be added to the DataFrame to then execute the predictor

        if buy_decide != 1:

            row = list()

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
            row = row + [file["date"][i - in_], buy_decide]

            k.loc[len(k.index)] = row

        # The Nan values must be dropped
        k = k.dropna()
    return k

main()
######################################################################################################
