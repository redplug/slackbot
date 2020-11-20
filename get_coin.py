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
        df = pyupbit.get_ohlcv(ticker, count=1, interval="day")
        del df['volume']
        # del df['low']
        # del df['high']
        df['Date'] = df.index
        return df, price