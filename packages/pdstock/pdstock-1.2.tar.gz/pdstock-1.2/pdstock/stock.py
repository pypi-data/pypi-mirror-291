#define function to generate stock data

import datetime
import pandas as pd
import time
import requests

def stockdata(stock_ticker, number_of_years):
    period1 = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=number_of_years*365)).timetuple()))
    period2 = int(time.mktime(datetime.datetime.now().timetuple()))
    interval = '1d' # 1d, 1m

    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{stock_ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_string)
    df['Date'] = pd.to_datetime(df['Date'])
    #df.reset_index('Date', drop=True)
    #earliest_date = df['Date'].min()
    #intended_start_date = datetime.datetime.fromtimestamp(period1)
    #if earliest_date > intended_start_date:
     #   print(f"The available data stops at {earliest_date.date()} instead of the requested {intended_start_date.date()}")
    return df
