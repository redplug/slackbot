# -*- coding:utf-8 -*-

import requests

from bs4 import BeautifulSoup

coins = ["KRW-BTC","BTC-META"]
urlbase = "https://upbit.com/exchange?code=CRIX.UPBIT."

for coin in coins:
    url = urlbase + coin
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    name_coin = soup.find('div > div > section > article > div > span')
    print(name_coin)


#UpbitLayout >

"https://upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC"
"https://upbit.com/exchange?code=CRIX.UPBIT.BTC-META"