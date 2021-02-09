import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd

import os
path = os.getcwd()
print(path)

path = '../data/ETH_OHLCV.csv'
temp = os.path.join(os.path.dirname(__file__), path)
path = os.path.normpath(temp)

print(path)

df = pd.read_csv(path)
df.rename(columns={'Price': 'Close'}, inplace=True)
df.drop(columns='Change %')


def func(strings):
    if ', 2020' in strings:
        strings.replace(', 2020', '')
        strings = '2020-' + strings
    elif ', 2019' in strings:
        strings.replace(', 2019', '')
        strings = '2019-' + strings
    elif ', 2018' in strings:
        strings.replace(', 2019', '')
        strings = '2019-' + strings
    return strings


df["Date"] = df["Date"].map(func)
print(df)

df.to_csv('../data/processed_ETH_OHLCV.csv', encoding='utf-8')


# data = btfeeds.YahooFinanceCSVData(dataname='wheremydatacsvis.csv')
# print(data)
