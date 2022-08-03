import sys
import pandas as pd
from tools.tools import name_col, RSI, macd, edit_df,print_results
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
# The number of the previous candlesticks (periods) is the main setting 
# of the indicator called a period. By default Period = 14; this is the value the author used.

periods = int(
    input("Enter the amount of periods for rsi calculation (14 recomended): \n")
)

p = rows + in_

# slope_ will be used to compare the candels slope (if it is negative is falling
#  and if it is positive is rising) 

# interval is the interval to consider, ex: 1d or 1h or 30m or 15m or 5m for each candlestick

interval = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")

# vol_p is the number that will be used to calculate the volume mean

vol_p = int(
    input("Enter how many candels consider to calculate the volume mean: \n"
    )
)

# List that'll be filled with the different Crypto-currency used

names = ["LISTA:"]





######################################################################################################

######################################################################################################
# MAIN PROGRAM 

# This for will read each historical Crypto-currency data added as an argument
def main():

    

    count = 0

    # counter is used in the main program to count the number of historical Crypto-currency data
    # added as argument

    for nam in range(1, len(sys.argv)):

        # file is a DataFrame created since the csv file with the historical Crypto-currency data

        file = pd.read_csv(f"base/{str(sys.argv[nam])}_{interval}_base.csv")

        # First need to add macd and rsi to the DataFrame
        
        file = add_rsi_macd(file)
        
    
        # if it is the first historical Crypto-currency data, then:

        if count == 0:

        # The funtion that generates the rows with the sequence of candels
        # named verify is called.
        # verify requires the DataFrame with the historical Crypto-currency data
        # and returns a DataFrame where each row is a sequence of candels determinated (rows), its
        #  technical indicators (rsi,macd, etc), other parameters like slope and finaly if the consecutives candels (in_)
        # have shown an increase or not (buy_decide) of its value in a the determinated percent (B) 

            df = verify(file)

            count += 1

            # if it's not the first historical Crypto-currency data, then:

        else:

            df_ = verify(file)

            # After we call verify, we append the new DataFrame of the new historical Crypto-currency data
            # to the previusly generated.

            df = pd.concat([df, df_], ignore_index = True)

        # add the name of the historical Crypto-currency in the names list

        names.append( str( sys.argv[nam]))

    # Make a last edition to the DataFrame

    df,list_dummies = edit_df(df, rows)

    df = df.drop(columns = ["date"], axis = 1)

    # get_dummies convert categorical variable into dummy/indicator variables 

    X = pd.get_dummies(df[list_dummies])

    y = df.buy

    X_train, X_test, y_train, y_test = train_test_split(
                                    X, y, test_size=0.3, 
                                    random_state=10
                                    )

    rfc = RandomForestClassifier(n_estimators=100,
                                    max_depth = 90)

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

    # This function prints the results

    print_results(names,p,periods,in_,B,rows,vol_p,st,predictions, y_test)

######################################################################################################

######################################################################################################


# FUNCTIONS

def verify(file):
    # verify requires a DataFrame and use the values defined before

    # create the index of the df

    index_ = name_col(rows,1)

    dataframe = pd.DataFrame(columns = index_)

    # Generate the  x-axis list to analize the slope with linear regression from cero to rows

    X = [x for x in range(0, rows)]
    X_long = [x for x in range(0, vol_p)]

    for i in range(p + vol_p, len(file.index)):

        Y_long = [file["close"][t] for t in range(i - vol_p - in_, i - in_)]
        Y = [file["close"][t] for t in range(i - p, i - in_)]

        slope_prev_short, intercept, r_value, p_value_2, std_err = linregress(X, Y)
        slope_prev, intercept, r_value, p_value_2, std_err = linregress(X_long, Y_long)
   
        close = np.mean([(file["close"][i - t] - file["close"][i - in_]) / file["close"][i - in_] for t in range(in_ )])

        # Generate the y-axis list to analize the slope with linear regression from cero to rows candels close values


        # Here creates a list with the RSI of the candels involved to find the minimun one 
        # and compare with the stablished before

        # The slope of the candels is calculated


        # Mean volume calculate

        vol = [file["volume"][i - x] for x in range(in_, in_ + 1 + vol_p)]
        vol_prom = np.mean(vol)

        mean_15 = np.mean([file["close"][t] for t in range(i - 15-in_, i-in_)])
        mean_30 = np.mean([file["close"][t] for t in range(i - 30 - in_, i- in_)])
        mean_60 =  np.mean([file["close"][t] for t in range(i - 60 - in_, i- in_)])
        mean_100 = np.mean([file["close"][t] for t in range(i - 100 - in_, i- in_)])

        mean_rel_15_30 = mean_15 / mean_30
        mean_rel_30_60 = mean_30 / mean_60
        mean_rel_60_100 = mean_60 / mean_100

        # hi is the list with variaton of the candles we consider to know if the price rises or fall

        high_candel = [(file["high"][i - t] - file["close"][i - in_]) / file["close"][i - in_] for t in range(in_ )]

        # If the candles that come after to the first candles considered (rows) 
        # are bigger than the B established value, buy decide will be B, otherwise it will be 0

        if max(high_candel) > B:

            buy_decide = f"{B}"

        else:

            buy_decide = "0"

        # either cero or B, if the row was considered, is will be added to the DataFrame to then execute the predictor

        row = list()

        for t in range(in_, p + 1):
            row = row + [
                file["volume"][i - t] / float(vol_prom),
                (file["open"][i - t] - file["close"][i - t]) / file["low"][i - t],
                (file["close"][i - t] - file["open"][i - t]) / file["high"][i - t],
                (file["high"][i - t]) / (file["low"][i - t]),
                file["rsi"][i - t],
                file["macd"][i - t],
                file["macd_h"][i - t],
                file["macd_s"][i - t],
                ]
        row = row + [file["date"][i - in_],
                close,
                slope_prev,
                slope_prev_short,
                mean_rel_15_30,
                mean_rel_30_60,
                mean_rel_60_100,
                buy_decide]

        dataframe.loc[len(dataframe.index)] = row

        # The Nan values must be dropped
        dataframe = dataframe.dropna()
    return dataframe

def add_rsi_macd(file_):
    # rsi is a list with each candel RSI value
    file = file_

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

    return file

main()
######################################################################################################
