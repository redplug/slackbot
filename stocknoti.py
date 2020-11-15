# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

import telegram

telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
telegram_chatid = os.environ.get('TELEGRAM_CHATID')

bot = telegram.Bot(token=telegram_token)

print(telegram_chatid)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('')
req.encoding = 'utf-8'
html = req.text
soup = BeautifulSoup(html, 'html.parser')
posts = soup.select('td > a')
latest = posts[14].text
href = posts[14].get('href')
url = ''
link = url + str(href)


bot.sendMessage(chat_id=telegram_chatid, text='test')