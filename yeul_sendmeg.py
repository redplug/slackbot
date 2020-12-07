# -*- coding: utf-8 -*-

from slacker import Slacker

import os

token = Slacker(os.environ.get('SLACK_BOT_TOKEN'))

slack = Slacker(token)
slack.chat.post_message('#_it_notice_test2', "https://yanolja.com")
