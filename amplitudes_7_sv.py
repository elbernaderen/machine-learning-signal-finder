import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import time


file =  pd.read_csv("XRPUSDT_15m.csv")
t = file.drop(columns= "time")


def verify(file):
    n = p = l = 0
    k = pd.DataFrame(columns =[ "open_1","high_1","low_1","close_1","mart_1","mart_inv_1",
                                "open_2","high_2","low_2","close_2","mart_2","mart_inv_2",
                                "open_3","high_3","low_3","close_3","mart_3","mart_inv_3",
                                "open_4","high_4","low_4","close_4","mart_4","mart_inv_4",
                                "open_5","high_5","low_5","close_5","mart_5","mart_inv_5",
                                "open_6","high_6","low_6","close_6","mart_6","mart_inv_6",
                                "date","buy"])
    for i in range(9,len(file.index)):
        si_no = 1
        if ((file["close"][i] - file["close"][i-4]) / file["close"][i-4]) > 0.01 or ((file["close"][i-1] - file["close"][i-4]) / file["close"][i-4]) > 0.01 or  ((file["close"][i-2] - file["close"][i-4]) / file["close"][i-4]) > 0.02 or((file["close"][i] - file["close"][i-4]) / file["close"][i-4]) > 0.02:
            si_no ="comprar"
            n +=1
        else:
            p+=1
            if l <= n*1.2:
                si_no = "nada"
                l += 1
        if si_no != 1:
            k.loc[len(k.index)] = [ file["open"][i-4] / file["close"][i-9], file["high"][i-4] / file["close"][i-9], file["low"][i-4] / file["close"][i-9], file["close"][i-4] / file["close"][i-9],(file["open"][i-4] - file["close"][i-4]) / file["low"][i-4],(file["close"][i-4] - file["open"][i-4]) / file["high"][i-4], 
                                    file["open"][i-5] / file["close"][i-9], file["high"][i-5] / file["close"][i-9], file["low"][i-5] / file["close"][i-9], file["close"][i-5] / file["close"][i-9],(file["open"][i-5] - file["close"][i-5]) / file["low"][i-5],(file["close"][i-5] - file["open"][i-5]) / file["high"][i-5],
                                    file["open"][i-6] / file["close"][i-9], file["high"][i-6] / file["close"][i-9], file["low"][i-6] / file["close"][i-9], file["close"][i-6] / file["close"][i-9],(file["open"][i-6] - file["close"][i-6]) / file["low"][i-6],(file["close"][i-6] - file["open"][i-6]) / file["high"][i-6],
                                    file["open"][i-7] / file["close"][i-9], file["high"][i-7] / file["close"][i-9], file["low"][i-7] / file["close"][i-9], file["close"][i-7] / file["close"][i-9],(file["open"][i-7] - file["close"][i-7]) / file["low"][i-7],(file["close"][i-7] - file["open"][i-7]) / file["high"][i-7],
                                    file["open"][i-8] / file["close"][i-9], file["high"][i-8] / file["close"][i-9], file["low"][i-8] / file["close"][i-9], file["close"][i-8] / file["close"][i-9],(file["open"][i-8] - file["close"][i-8]) / file["low"][i-8],(file["close"][i-8] - file["open"][i-8]) / file["high"][i-8],
                                    file["open"][i-9] / file["close"][i-9], file["high"][i-9] / file["close"][i-9], file["low"][i-9] / file["close"][i-9], file["close"][i-9] / file["close"][i-9],(file["open"][i-9] - file["close"][i-9]) / file["low"][i-9],(file["close"][i-9] - file["open"][i-9]) / file["high"][i-9],
                                    file["date"][i-4],si_no]
            if si_no == "comprar":
                i+=6       
    print(n,p)     
    return k

v = verify(file)
y = v.buy
shib_features = [ "open_1","high_1","low_1","close_1","mart_1","mart_inv_1",
                "open_2","high_2","low_2","close_2","mart_2","mart_inv_2",
                "open_3","high_3","low_3","close_3","mart_3","mart_inv_3",
                "open_4","high_4","low_4","close_4","mart_4","mart_inv_4",
                "open_5","high_5","low_5","close_5","mart_5","mart_inv_5",
                "open_6","high_6","low_6","close_6","mart_6","mart_inv_6"]
                                
X =  v[shib_features]
# random_state=10
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=10)
rfc = RandomForestClassifier(n_estimators=1000)
rfc.fit(X_train,y_train)
predictions = rfc.predict(X_test)
print(confusion_matrix(y_test,predictions))

print(classification_report(y_test,predictions))
def pred(pred=rfc):
    rfc = pred
    return rfc