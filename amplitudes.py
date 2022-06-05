import sys
import pandas as pd
from tools import name_col,RSI,macd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import time
import pickle
import datetime
import numpy as np
from scipy.stats import linregress

# B is the rise percent of the candles next to the close of the last candle
#  that we use to decide if this sequence anticipate a rise

B = float(input("Enter the percentage that have to rise the price to consider it as a success: \n"))
# in_ is the number of candles we consider to know if the price rises or fall
in_ = int(input("Enter the number of candels (Y) to consider in the model for the prediction: \n"))
rows =int(input("Enter the number of candels (X) consider in the model for the prediction: \n"))
periods = int(input("Enter the amount of periods for rsi calculation (14 recomended): \n"))
rsi_ = int(input("Enter the rsi value to consider (30 recomended): \n"))
p = rows + in_
a = int(input("Enter how much to increase the mean volume value: \n"))
slope_ = int(input("Enter the slope to take in reference, (0 recomended):\n"))
temp = input("Enter the interval to consider, ex: 1d or 1h or 30m or 15m or 5m \n")
def verify(file):
    # create the index of the df
    index_ = name_col(p,in_)
    index_.append("date")
    index_.append("buy")
    k = pd.DataFrame(columns = index_)
    #Generate a list to analize the slope with linear regression from cero to rows
    X = [x for x in range(0,p-in_)]
    for i in range(p,len(file.index)):
        Y = [file["close"][t] for t in range(i-p,i-in_)]
        rsi_list = [file["rsi"][t] for t in range(i-p,i-in_)]
        slope,intercept, r_value, p_value_2, std_err = linregress(X, Y)
        vol = [file["volume"][i-x] for x in range(in_ ,p+1)]
        vol_prom = np.mean(vol)
        si_no = 1
        #if the values in the row pass the filter, they are considered to make the predictor model
        if slope < slope_ and (file["volume"][i-in_] or file["volume"][i-in_-1]) > vol_prom * a and min(rsi_list) < rsi_:
            # hi is the list with variaton of the candles we consider to know if the price rises or fall
            hi = [(file["high"][i-t] - file["close"][i-in_]) / file["close"][i-in_] for t in range(in_ + 1)]
            if max(hi) > B:
                si_no = f"{B}"
            else:
                si_no = "0"
        # eithercero or B, if the row was considered, is will be added to the df to then execute the predictor
        if si_no != 1:
            row = list()
            for t in range(in_ ,p+1):
                row = row +[file["volume"][i-t] / float(file["volume"][i-p]),
                (file["open"][i-t] - file["close"][i-t]) / file["low"][i-t],
                (file["close"][i-t] - file["open"][i-t]) / file["high"][i-t],
                (file["high"][i-t]) / (file["low"][i-t]),
                file["rsi"][i-t],
                file["macd"][i-t],
                file["macd_h"][i-t],
                file["macd_s"][i-t]] 
            row = row + [file["date"][i-in_],si_no] 
            k.loc[len(k.index)] = row
        k = k.dropna()
    return k

names=["LISTA:"]
count = 0

for nam in range(1,len(sys.argv)):
    file =  pd.read_csv(f"{str(sys.argv[nam])}_{temp}_basehs.csv")
    
    rsi = RSI(file["close"],periods)
    file["rsi"] = rsi
    file = macd(file)
    file.drop(index=file.index[:95], 
        axis=0, 
        inplace=True)
    file = file.reset_index()

    if count == 0:
        v = verify(file)
        count +=1
    else:
        k = verify(file)

        v = pd.concat([v,k],ignore_index=True)

    names.append(str(sys.argv[nam]))
y = v.buy
#columns to use to run the rfc
features =  name_col(p,in_)
X =  v[features]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=10)
rfc = RandomForestClassifier(n_estimators=2000)
rfc.fit(X_train,y_train)
predictions = rfc.predict(X_test)
st = str(datetime.datetime.now())
st = st.replace(" ","_")
st = st.replace(":","_")
filename = f'model_p_{p}_perio_{periods}_in_{in_}_{B}_{st[0:16]}.sav'
pickle.dump(rfc, open(filename, 'wb'))
print(f'model_p_{p}_perio_{periods}_in_{in_}_{B}_{st[0:16]}.sav' )
print(names)
print(classification_report(y_test,predictions))
print(f"periods rsi: {periods}")
print(f"in_: {in_}")
print(f"p: {p}")
print(f"rows: {rows}")

