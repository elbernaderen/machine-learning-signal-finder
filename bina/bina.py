import sys
from binance import Client
import pandas as pd
import yaml
import datetime

# import config
config = yaml.load(open('ignore/config.yml'), Loader=yaml.FullLoader)

# create client
try:
    client = Client(config['api_key'], config['api_secret'])
except ConnectionError:
    print("check your internet connection\n")
    client = Client(config['api_key'], config['api_secret'])


def store_ohlcv(symbol = "LINKUSDT", interval='1h', start_date=datetime.datetime(2018,8,18), name=""):
    # import ohlcv from binance starting from date 'start_date', that has to be in a string format of the timestamp in ms
    start_str = str(1000*start_date.timestamp())
    klines = client.get_historical_klines_generator(symbol, interval, start_str)
    # create the DataFramePY
    df = pd.DataFrame(klines, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'end_time', 'quote_volume', 'nbs_trades', 'buy_base_volume', 'buy_quote_volume', 'ignore'])
    # add data
    df.loc[:,'date'] = pd.to_datetime(df.time, unit='ms')
    # remove the useless column and the last row as it is the current candle, therefore is not completed
    df = df.drop('ignore', axis=1).iloc[:-1]
    # store data as a csv file
    df.to_csv(f"{name}/{symbol}_{interval}_{name}.csv")


