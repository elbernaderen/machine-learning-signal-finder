import sys
from bina.bina import store_ohlcv
import datetime
import time

if len(sys.argv) > 0:
    name = sys.argv[1]
    file_name = sys.argv[2]
    year = int(sys.argv[3])
    month = int(sys.argv[4])
    day = int(sys.argv[5])
print(dia)
start_date = datetime.datetime(year, month, day)
kk = store_ohlcv(symbol = name,
                interval = "30m",
                start_date = start_date,
                 name = file_name)
print(name)
