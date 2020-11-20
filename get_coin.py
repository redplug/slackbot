# -*- coding: utf-8 -*-

import pyupbit

def get_coin(coin):
    if coin == None:
        tickers = pyupbit.get_tickers()
        return tickers
    elif coin != None:
        coin = coin.replace(" ","")
        ticker = coin.replace("코인","")
        price = format(pyupbit.get_current_price(ticker), ',')
        df = pyupbit.get_ohlcv(ticker, count=2, interval="day")
        df.drop(['volume', 'high', 'low'], axis=1, inplace=True)
        df['N'] = ['1', '2']
        df.set_index('N', inplace=True)
        return df, price