import numpy as np
from datetime import datetime
import pandas as pd
from sklearn.metrics import classification_report

######################################################################################################
# name generator

def name_col(rows, k = 2):

    ind_row = rows + 1
    index_ = list()
    for cin in range(ind_row):

        index_.append(f"volume_{cin}")
        index_.append(f"mart_{cin}")
        index_.append(f"mart_inv_{cin}")
        index_.append(f"ampl_2{cin}")
        index_.append(f"rsi_{cin}")
        index_.append(f"macd_{cin}")
        index_.append(f"macd_h{cin}")
        index_.append(f"macd_s{cin}")

    if k == 2:

        return index_

    if k == 1:

        index_.append("date")
        index_.append("close")
        index_.append("slope_prev")
        index_.append("slope_prev_short")
        index_.append("mean_rel_15_30")
        index_.append("mean_rel_30_60")
        index_.append("mean_rel_60_100")
        index_.append("buy")

        return index_

    if k == 3:
        index_.append("slope_prev")
        index_.append("slope_prev_short")
        index_.append("mean_rel_15_30")
        index_.append("mean_rel_30_60")
        index_.append("mean_rel_60_100")

        return index_

    if k == 4:
        index_.append("date")
        index_.append("slope_prev")
        index_.append("slope_prev_short")
        index_.append("mean_rel_15_30")
        index_.append("mean_rel_30_60")
        index_.append("mean_rel_60_100")
    
        return index_
######################################################################################################


######################################################################################################
def RSI(t, periods=10):

# extracted from https://programmerclick.com/article/34731200625/
    length = len(t)
    rsies = [np.nan]*length
    
         # La longitud de los datos no excede el período y no se puede calcular;

    if length <= periods:
        return rsies

         #Utilizado para cálculos rápidos;

    up_avg = 0
    down_avg = 0
 
         # Primero calcule el primer RSI, use los períodos anteriores + 1 dato para formar una secuencia de períodos;
    first_t = t[:periods+1]
    for i in range(1, len(first_t)):
                 #Precio aumentado;
        if first_t[i] >= first_t[i-1]:
            up_avg += first_t[i] - first_t[i-1]
                 #caída de los precios; 
        else:
            down_avg += first_t[i-1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsies[periods] = 100 - 100/(1+rs)
 
         # Lo siguiente utilizará cálculo rápido;
    for j in range(periods+1, length):
        up = 0
        down = 0
        if t[j] >= t[j-1]:
            up = t[j] - t[j-1]
            down = 0
        else:
            up = 0
            down = t[j-1] - t[j]
                 # Fórmula de cálculo similar a la media móvil;
        up_avg = (up_avg*(periods - 1) + up)/periods
        down_avg = (down_avg*(periods - 1) + down)/periods
        rs = up_avg/down_avg
        rsies[j] = 100 - 100/(1+rs)
    return rsies

######################################################################################################

######################################################################################################

def macd(file):

    # A DataFrame is received

    df=file
    k = df['close'].ewm(span=12, adjust=False, min_periods=12).mean()

    # Get the 12-day EMA of the closing price

    d = df['close'].ewm(span=26, adjust=False, min_periods=26).mean()

    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD

    macd = k - d

    # Get the 9-Day EMA of the MACD for the Trigger line

    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()

    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value

    macd_h = macd - macd_s

    # Add all of our new values for the MACD to the dataframe

    df['macd'] = df.index.map(macd)
    df['macd_h'] = df.index.map(macd_h)
    df['macd_s'] = df.index.map(macd_s)

    return df

######################################################################################################

######################################################################################################

# name generator for the backtest

def name_col_2(in_):
    ind_row = in_
    index_ = list()
    for cin in range(ind_row):
        index_.append(f"salida_{cin}")
    for cin in range(ind_row):
        index_.append(f"salidam_{cin}")
    return index_

######################################################################################################

######################################################################################################

# hour and day converter through the date

def weekday_convert(row):
    date_time_obj = datetime. strptime(row[0:20], '%Y-%m-%d %H:%M:%S')
    return date_time_obj.weekday()


def hour_convert(row):
    date_time_obj = datetime. strptime(row[0:20], '%Y-%m-%d %H:%M:%S')
    return date_time_obj.hour
    

######################################################################################################

######################################################################################################
# cut_labels make a continuos variable to a categorical one

def cut_labels(df,columns_cut_dummi):

    list_dummies = list()

    for i in columns_cut_dummi:

        sep = (df[i].max() - df[i].min()) / 11

        list_dummies.append(f"{i}_cut")

        df[f"{i}_cut"] = pd.cut(x=df[i],
                                bins=[df[i].min() + k * sep for k in range(0,12) ],
                                labels=[-5,-4,-3,-2,-1,0, 1, 2, 3,4,5]
                                )

    list_dummies.extend(["hour","day"])

    return df,list_dummies

######################################################################################################

######################################################################################################
def edit_df(df, rows,prop = 1):

    # Take off the values outliers, or that ones that aren't frequent
    # this option is used for amplitudes.py
    if prop == 1:

        df = df[ df["close"] < 0.1]

        df = df[ df["close"] > -0.1]

    # columns to use to run the rfc

    features = name_col(rows, 3)

    # cut_labels make a continuos variable to a categorical one

    df,list_dummies= cut_labels(df,features)

    # add the day and hour columns

    df["day"] = df["date"].apply(weekday_convert)

    df["hour"] = df["date"].apply(hour_convert)

    return df,list_dummies

######################################################################################################

######################################################################################################
def print_results(names,p,periods,in_,B,rows,vol_p,st,predictions, y_test):

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
    print(f"rows: {rows}")
    print(f"Candels used to calculate volume: {vol_p}")