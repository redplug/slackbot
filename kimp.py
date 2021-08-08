import ccxt
import os
import datetime
import time
from currency_converter import CurrencyConverter


def kimp():
    c = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
    exchange_rate = round(c.convert(1, 'USD', 'KRW'),2) #환율
    #print(exchange_rate)

    binance = ccxt.binance()
    markets_binance = binance.fetch_tickers()
    #print(markets_binance.keys())
    binance_BTC = binance.fetch_ticker('BTC/USDT')
    binance_BTC_close = binance_BTC['close']
    #print(binance_BTC_close)

    upbit = ccxt.upbit()
    markets_upbit = upbit.fetch_tickers()
    #print(markets_upbit.keys())
    upbit_BTC = upbit.fetch_ticker('BTC/KRW')
    upbit_BTC_close = upbit_BTC['close']
    #print(upbit_BTC_close)
    kimp_BTC = round(((upbit_BTC_close/(binance_BTC_close*exchange_rate) - 1) * 100),2)

    binance_ETH = binance.fetch_ticker('ETH/USDT')
    binance_XRP = binance.fetch_ticker('XRP/USDT')
    binance_ADA = binance.fetch_ticker('ADA/USDT')
    binance_ETH_close = binance_ETH['close']
    binance_XRP_close = binance_XRP['close']
    binance_ADA_close = binance_ADA['close']

    upbit_ETH = upbit.fetch_ticker('ETH/KRW')
    upbit_XRP = upbit.fetch_ticker('XRP/KRW')
    upbit_ADA = upbit.fetch_ticker('ADA/KRW')
    upbit_ETH_close = upbit_ETH['close']
    upbit_XRP_close = upbit_XRP['close']
    upbit_ADA_close = upbit_ADA['close']

    kimp_ETH = round(((upbit_ETH_close / (binance_ETH_close * exchange_rate) - 1) * 100))
    kimp_XRP = round(((upbit_XRP_close / (binance_XRP_close * exchange_rate) - 1) * 100))
    kimp_ADA = round(((upbit_ADA_close / (binance_ADA_close * exchange_rate) - 1) * 100))

    format_upbit_BTC_close = format(upbit_BTC_close, ",")[:-2]
    format_upbit_ETH_close = format(upbit_ETH_close, ",")[:-2]
    format_upbit_XRP_close = format(upbit_XRP_close, ",")[:-2]
    format_upbit_ADA_close = format(upbit_ADA_close, ",")[:-2]

    # now = datetime.datetime.now().time()
    now = time.strftime('%y-%m-%d %H:%M:%S')

    s = f"현재시간 : {now} <br><br>\n" \
        f"BTC : {format_upbit_BTC_close} ({kimp_BTC}%) <p> \n" \
        f"ETH : {format_upbit_ETH_close} ({kimp_ETH}%) <p> \n" \
        f"XRP : {format_upbit_XRP_close} ({kimp_XRP}%) <p> \n" \
        f"ADA : {format_upbit_ADA_close} ({kimp_ADA}%)"
    return s

if __name__ == '__main__':
    print(kimp())