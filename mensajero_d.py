import sys
from tkinter import N
import pandas as pd
import datetime
import winsound
import time
from bina import store_ohlcv
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import pickle
import telegram




api_key = '5187902884:AAHN_f_MFNHLwX_50X7Gu2LPJDOrlZPCkoY'
user_id = '1883463708'

bot = telegram.Bot(token=api_key)
def name_col(p,in_):
    ind_row = p - in_ + 1
    index_ = list()
    for cin in range(ind_row):
        index_.append(f"open_{cin}")
        index_.append(f"high_{cin}")
        index_.append(f"low_{cin}")
        index_.append(f"close_{cin}")
        index_.append(f"mart_{cin}")
        index_.append(f"mart_inv_{cin}")
    return index_
p = 9
in_ = 2
rows = 7
def make_prediction(file):
    index_ = name_col(p,in_)
    index_.append("date")
    index_.append("close")
    new = pd.DataFrame(columns = index_)                            
    i = len(file)-1
    row = list()
    for t in range(rows+1):
        row.append(file["open"][i-t] / file["close"][i-rows])
        row.append(file["high"][i-t] / file["close"][i-rows])
        row.append(file["low"][i-t] / file["close"][i-rows])
        row.append(file["close"][i-t] / file["close"][i-rows])
        row.append((file["open"][i-t] - file["close"][i-t]) / file["low"][i-t])
        row.append((file["close"][i-t] - file["open"][i-t]) / file["high"][i-t])
    row.extend([file["date"][i],file["close"][i]])
    new.loc[1] = row
    return new

nam = str(sys.argv[1])
exc_1 = str(sys.argv[2])
exc_2 = str(sys.argv[3])
exc_3 = str(sys.argv[4])
print(exc_3)
filename_1 = f'{exc_1}.sav'
filename_2 = f'{exc_2}.sav'
filename_3 = f'{exc_3}.sav'
rfc_1 = pickle.load(open(filename_1, 'rb'))
rfc_2 = pickle.load(open(filename_2, 'rb'))
rfc_3 = pickle.load(open(filename_3, 'rb'))

while True:
    hour = datetime.timedelta(days = 11)
    day = datetime.datetime.utcnow()
    tt = day-hour
   
    kk = store_ohlcv(symbol = nam,interval='1d',start_date = tt,name="_mensajero")
    
    time.sleep(30)
    file =  pd.read_csv(f"{nam}_1d_mensajero.csv")  
    new = make_prediction(file)
    response_1 = rfc_1.predict(new.drop(columns = ["date","close"]))  
    response_2 = rfc_2.predict(new.drop(columns = ["date","close"]))
    response_3 = rfc_3.predict(new.drop(columns = ["date","close"]))      
    print(response_1,response_2,response_3,new["date"]," ",new["close"])
    coef_1 = float(response_1)
    coef_2 = float(response_2)
    coef_3 = float(response_3)
    if coef_1 > 0 or coef_2 > 0 or coef_3 > 0:
        coef = max([coef_1,coef_2,coef_3])
        t= f'{nam} \n value {coef} \n BUY: {float(new["close"])} \n TAKEPROFIT: {float(new["close"])*(1+coef*.8)} \n STOPLOSS: {float(new["close"])*(1-coef/2)} \n 1% : {float(new["close"])*(1.0115)}\n 2% : {float(new["close"])*(1.0215)} \n cero: {float(new["close"])*(1+0.0015)} \n {datetime.datetime.now()} '
        print(t)
        bot.send_message(chat_id=user_id, text=t)
    time.sleep(86370)
        