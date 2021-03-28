import requests
from bs4 import BeautifulSoup
import os
import time

import telegram


bot = telegram.Bot(token='1009313312:AAGgVkPz_bTHnUMYN0lW9Td_W-iYmR3jut4')
# 우선 테스트 봇이니까 가장 마지막으로 bot에게 말을 건 사람의 id를 지정해줄게요.
chat_id = bot.getUpdates()[-1].message.chat.id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
while True:
    req = requests.get('https://www.thisisgame.com/pad/tboard/?board=25')
    req.encoding = 'utf-8' # Clien에서 encoding 정보를 보내주지 않아 encoding옵션을 추가해줘야합니다.
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select('td > a')
    latest = posts[14].text
    href = posts[14].get('href')
    url = 'https://www.thisisgame.com/pad/tboard/'
    link = url + str(href)
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        print(before)
        print(BASE_DIR)
        if before != latest:
            bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요! : ' + latest + link)
        #else: # 원래는 이 메시지를 보낼 필요가 없지만, 테스트 할 때는 봇이 동작하는지 확인차 넣어봤어요.
         #   bot.sendMessage(chat_id=chat_id, text='새 글이 없어요 ㅠㅠ')
        f_read.close()

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
        f_write.write(latest)
        print(latest)
        f_write.close()
    time.sleep(60)
