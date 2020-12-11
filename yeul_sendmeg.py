# -*- coding: utf-8 -*-

from slacker import Slacker

import os

token = Slacker(os.environ.get('SLACK_BOT_TOKEN'))
print(token)
slack = Slacker(token)
slack.chat.post_message('#채널명', ":이모지:제목:이모지: \n 내용 \n https://naver.com")
