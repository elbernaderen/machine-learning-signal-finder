import pandas as pd
import datetime
import time
from amplitudes_7_sv import pred
from bina import store_ohlcv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
#print(datetime.datetime())
def make_prediction(file):

    new = pd.DataFrame(columns = [  "open_1","high_1","low_1","close_1","mart_1","mart_inv_1",
                                    "open_2","high_2","low_2","close_2","mart_2","mart_inv_2",
                                    "open_3","high_3","low_3","close_3","mart_3","mart_inv_3",
                                    "open_4","high_4","low_4","close_4","mart_4","mart_inv_4",
                                    "open_5","high_5","low_5","close_5","mart_5","mart_inv_5",
                                    "open_6","high_6","low_6","close_6","mart_6","mart_inv_6",
                                    "date","close"])                            
    i = len(file)-1
    new.loc[1] = [  file["open"][i] /   file["close"][i-6], file["high"][i] /   file["close"][i-6], file["low"][i] /   file["close"][i-6],    file["close"][i] / file["close"][i-6],(file["open"][i] - file["close"][i]) / file["low"][i],(file["close"][i] - file["open"][i]) / file["high"][i],
                    file["open"][i-1] / file["close"][i-6], file["high"][i-1] / file["close"][i-6], file["low"][i-1] / file["close"][i-6], file["close"][i-1] / file["close"][i-6],(file["open"][i-1] - file["close"][i-1]) / file["low"][i-1],(file["close"][i-1] - file["open"][i-1]) / file["high"][i-1], 
                    file["open"][i-2] / file["close"][i-6], file["high"][i-2] / file["close"][i-6], file["low"][i-2] / file["close"][i-6], file["close"][i-2] / file["close"][i-6],(file["open"][i-2] - file["close"][i-2]) / file["low"][i-2],(file["close"][i-2] - file["open"][i-2]) / file["high"][i-2],
                    file["open"][i-3] / file["close"][i-6], file["high"][i-3] / file["close"][i-6], file["low"][i-3] / file["close"][i-6], file["close"][i-3] / file["close"][i-6],(file["open"][i-3] - file["close"][i-3]) / file["low"][i-3],(file["close"][i-3] - file["open"][i-3]) / file["high"][i-3],
                    file["open"][i-4] / file["close"][i-6], file["high"][i-4] / file["close"][i-6], file["low"][i-4] / file["close"][i-6], file["close"][i-4] / file["close"][i-6],(file["open"][i-4] - file["close"][i-4]) / file["low"][i-4],(file["close"][i-4] - file["open"][i-4]) / file["high"][i-4],
                    file["open"][i-5] / file["close"][i-6], file["high"][i-5] / file["close"][i-6], file["low"][i-5] / file["close"][i-6], file["close"][i-5] / file["close"][i-6],(file["open"][i-5] - file["close"][i-5]) / file["low"][i-5],(file["close"][i-5] - file["open"][i-5]) / file["high"][i-5],
                    file["date"][i], file["close"][i]]
    return new

predictions = pred()
while True:
    hour = datetime.timedelta(hours = 5)
    day = datetime.datetime.utcnow()
    tt = day-hour
    time.sleep(20)
    kk = store_ohlcv(start_date = tt,name = "_prueba")
    file =  pd.read_csv("XRPUSDT_15m_prueba.csv")  
    new = make_prediction(file)
    response = predictions.predict(new.drop(columns = ["date","close"]))
    #predictions = rfc.predict(new.drop(columns = ["date","close"]))
    print(response,new["date"]," ",new["close"])
    time.sleep(430)