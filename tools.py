import numpy as np
import pandas as pd
from sklearn.neighbors import radius_neighbors_graph
def name_col(p,in_):
    ind_row = p - in_ + 1
    index_ = list()
    for cin in range(ind_row):
        index_.append(f"open_{cin}")
        index_.append(f"high_{cin}")
        index_.append(f"low_{cin}")
        index_.append(f"close_{cin}")
        index_.append(f"volume_{cin}")
        index_.append(f"mart_{cin}")
        index_.append(f"mart_inv_{cin}")
        index_.append(f"ampl_2{cin}")
        index_.append(f"rsi_{cin}")
        index_.append(f"macd_{cin}")
        index_.append(f"macd_h{cin}")
        index_.append(f"macd_s{cin}")
    return index_
    # extracted from https://programmerclick.com/article/34731200625/

def RSI(t, periods=10):
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
def macd(file):
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