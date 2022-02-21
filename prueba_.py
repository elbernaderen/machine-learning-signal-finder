from tkinter import Y
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import datetime
import time
from amplitudes_7_sv import pred,verify
from bina import store_ohlcv

predictions = pred()
hour = datetime.timedelta(hours = 24)
day = datetime.datetime.utcnow()
tt = day-hour

kk = store_ohlcv(start_date = tt,name = "_prueba")
time.sleep(150)
file =  pd.read_csv("XRPUSDT_15m_prueba.csv")
v = verify(file)
y = v.buy
shib_features = [ "open_1","high_1","low_1","close_1","mart_1","mart_inv_1",
                "open_2","high_2","low_2","close_2","mart_2","mart_inv_2",
                "open_3","high_3","low_3","close_3","mart_3","mart_inv_3",
                "open_4","high_4","low_4","close_4","mart_4","mart_inv_4",
                "open_5","high_5","low_5","close_5","mart_5","mart_inv_5",
                "open_6","high_6","low_6","close_6","mart_6","mart_inv_6"]

X =  v[shib_features]

response = predictions.predict(X)
print(classification_report(y,response))

print(confusion_matrix(y,response))