
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import time
import pickle
import datetime

B = sys.argv[0]

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
        index_.append(f"ampl_1{cin}")
        index_.append(f"ampl_2{cin}")
    return index_
p = 15
in_ = 2
def verify(file,nam):
    
    index_ = name_col(p,in_)
    index_.append("date")
    index_.append("buy")
    t = file.drop(columns= "time")
    
    k = pd.DataFrame(columns = index_)
    for i in range(p,len(file.index)):
        
        si_no = 1
        
        if ((file["high"][i] - file["close"][i-in_]) / file["close"][i-in_]) > B or ((file["high"][i-1] - file["close"][i-in_]) / file["close"][i-in_]) > B :
            si_no = f"{B}"
        else:
            si_no = "0"
        if si_no != 1:
            row = list()
            for t in range(in_ ,p+1):
                row.append(file["open"][i-t] / file["close"][i-p])
                row.append(file["high"][i-t] / file["close"][i-p])
                row.append(file["low"][i-t] / file["close"][i-p])
                row.append(file["close"][i-t] / file["close"][i-p])
                row.append((file["open"][i-t] - file["close"][i-t]) / file["low"][i-t])
                row.append((file["close"][i-t] - file["open"][i-t]) / file["high"][i-t])
                row.append((file["open"][i-t] - file["close"][i-t]) / (file["high"][i-t]-file["low"][i-t]))
                row.append((file["high"][i-t]) / (file["low"][i-t]))
            row.append(file["date"][i-in_])
            row.append(si_no)
            k.loc[len(k.index)] = row
    #i+=5
    return k

names=["LISTA:"]
count = 0
for nam in range(1,len(sys.argv)):
    print(str(sys.argv[nam]))
    file =  pd.read_csv(f"{str(sys.argv[nam])}_1d_basehs.csv")

    if count == 0:
        v = verify(file,nam = str(sys.argv[nam]))
        count +=1
    else:
        k = verify(file,nam = str(sys.argv[nam]))
        v = v.append(k,ignore_index=True)
    names.append(str(sys.argv[nam]))

print(len(v))
y = v.buy

shib_features =  name_col(p,in_)
       
X =  v[shib_features]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=10)
rfc = RandomForestClassifier(n_estimators=1000)
rfc.fit(X_train,y_train)
predictions = rfc.predict(X_test)
print(confusion_matrix(y_test,predictions))

st = str(datetime.datetime.now())
st = st.replace(" ","_")
st = st.replace(":","_")
filename = f'model_alta{B}_{st[0:15]}.sav'
print("rows: ",p-in_)
pickle.dump(rfc, open(filename, 'wb'))
print(f'model_alta{B}_{st[0:15]}.sav' )
print(names)
print(classification_report(y_test,predictions))
loaded_model = pickle.load(open(filename, 'rb'))
comprobacion = loaded_model.predict(X_test)

