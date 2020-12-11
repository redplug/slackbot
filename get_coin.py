# -*- coding: utf-8 -*-

import pyupbit

def get_coin(coin):
    if coin == None:
        pass
        # tickers = pyupbit.get_tickers()
        # return tickers
    elif coin != None:
        coin = coin.replace(" ","")
        ticker = coin.replace("코인","")
        price = format(pyupbit.get_current_price(ticker), ',')
        pricelow = pyupbit.get_current_price(ticker)
        df = pyupbit.get_ohlcv(ticker, count=2, interval="day")
        df.drop(['volume', 'high', 'low'], axis=1, inplace=True)
        df['N'] = ['1', '2']
        df['Date'] = df.index
        df.set_index('N', inplace=True)
        df["open"] = [format(df['open'][0], ','), format(df['open'][1], ',')]
        df["close"] = [format(df['close'][0], ','), format(df['close'][1], ',')]
        yesterdaylow = float(df['close'][0].replace(",", ""))
        pricefloat = float(pricelow)
        per = (pricefloat / yesterdaylow * 100) - 100
        per = "%.2f%%" %per
        return df, price, per