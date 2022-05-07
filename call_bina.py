import sys
from bina import store_ohlcv
import datetime
import time

if len(sys.argv) > 0:
    nam = sys.argv[1]
    name = sys.argv[2]
    año = int(sys.argv[3])
    mes = int(sys.argv[4])
    dia = int(sys.argv[5])
print(dia)
start_date=datetime.datetime(año,mes,dia)     
kk=store_ohlcv(symbol = nam,interval='30m', start_date=start_date,name=name)
print(nam)
