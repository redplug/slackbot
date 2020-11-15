# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

import telegram

telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
telegram_chatid = os.environ.get('TELEGRAM_CHATID')

bot = telegram.Bot(token=telegram_token)

req = requests.get('https://m.stock.naver.com/worldstock/index.html#/stock/TBC/total')
req.encoding = 'utf-8'
html = req.text
soup = BeautifulSoup(html, 'html.parser')


bot.sendMessage(chat_id=telegram_chatid, text='test')