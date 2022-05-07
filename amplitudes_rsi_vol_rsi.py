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
B = float(sys.argv[1])


#number of rows,or how many candles we are goingo to analize is p minus in_ 
p = 15
periods = 14
a=4
rsi_=30
# in_ is the number of candles we consider to know if the price rises or fall
in_ = 6
def verify(file,nam):
    index_ = name_col(p,in_)
    index_.append("date")
    index_.append("buy")
    k = pd.DataFrame(columns = index_)
    X = [x for x in range(0,p-in_)]
    for i in range(p,len(file.index)):
        Y = [file["close"][t] for t in range(i-p,i-in_)]
        slope,intercept, r_value, p_value_2, std_err = linregress(X, Y)
        vol = [file["volume"][i-x] for x in range(in_ ,p+1)]
        vol_prom = np.mean(vol)
        si_no = 1
        if slope < 0 and file["rsi"][i-in_] < rsi_:
            if ((file["high"][i] - file["close"][i-in_]) / file["close"][i-in_]) > B or ((file["high"][i-1] - file["close"][i-in_]) / file["close"][i-in_]) > B or ((file["high"][i-2] - file["close"][i-in_]) / file["close"][i-in_]) > B or ((file["high"][i-3] - file["close"][i-in_]) / file["close"][i-in_]) > B or ((file["high"][i-4] - file["close"][i-in_]) / file["close"][i-in_]) > B:
                si_no = f"{B}"
            else:
                si_no = "0"
        if si_no != 1:
            row = list()
            for t in range(in_ ,p+1):
                row.append(file["volume"][i-t] / float(file["volume"][i-p]))
                row.append((file["open"][i-t] - file["close"][i-t]) / file["low"][i-t])
                row.append((file["close"][i-t] - file["open"][i-t]) / file["high"][i-t])
                row.append((file["high"][i-t]) / (file["low"][i-t]))
                row.append(file["rsi"][i-t])
                row.append(file["macd"][i-t])
                row.append(file["macd_h"][i-t])
                row.append(file["macd_s"][i-t])
            row.append(file["date"][i-in_])
            row.append(si_no)
            k.loc[len(k.index)] = row
            i+=in_
        k = k.dropna()
    return k

names=["LISTA:"]
count = 0
temp = str(sys.argv[2])
for nam in range(3,len(sys.argv)):
    file =  pd.read_csv(f"{str(sys.argv[nam])}_{temp}_basehs.csv")
    rsi = RSI(file["close"],periods)
    file["rsi"] = rsi
    file = macd(file)
    file.drop(index=file.index[:95], 
        axis=0, 
        inplace=True)
    file = file.reset_index()

    if count == 0:
        v = verify(file,nam = str(sys.argv[nam]))
        count +=1
    else:
        k = verify(file,nam = str(sys.argv[nam]))
        v = pd.concat([v,k],ignore_index=True)
    names.append(str(sys.argv[nam]))
y = v.buy

shib_features =  name_col(p,in_)
       
X =  v[shib_features]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=10)
rfc = RandomForestClassifier(n_estimators=1000)
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
loaded_model = pickle.load(open(filename, 'rb'))
comprobacion = loaded_model.predict(X_test)

