from bina import store_ohlcv
import datetime
import time

kk=store_ohlcv(symbol="LINKUSDT", start_date=datetime.datetime(2020,7,18))
print("ok")