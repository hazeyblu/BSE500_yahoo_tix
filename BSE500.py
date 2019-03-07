import os
import pandas as pd
import datetime as dt
import pandas_datareader.data as web
from dateutil.relativedelta import relativedelta

end_date = dt.datetime.now()
start_date = end_date - relativedelta(years=10)
symbols_file = "YahooTix.csv"
folder_name = "BSE_500"


def get_data_from_yahoo():
    df = pd.read_csv(symbols_file)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    tix = df['Symbol']
    com = df['Company']
    for x in range(len(tix)):
        if not os.path.exists(folder_name + '/{}.csv'.format(com[x])):
            print(com[x])
            try:
                df = web.DataReader(tix[x], "yahoo", start_date, end_date)
                df.dropna()
                ema200 = df['Adj Close'].ewm(span=200, adjust=False, min_periods=200).mean()
                df['200EMA'] = ema200
                df.to_csv(folder_name + '/{}.csv'.format(com[x]))
            except Exception as e:
                print(e)
        else:
            print("Already have " + com[x] + " data")


get_data_from_yahoo()
