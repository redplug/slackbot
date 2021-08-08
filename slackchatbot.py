# -*- coding: utf-8 -*-

import os
import json
from slacker import Slacker
from flask import Flask, request, make_response
from urlshort import url_short
from bob_recommend import food_answer
from get_weather import get_weather
from get_covid import get_covid
import kimp

currency = "환율"
surl = "주소단축"
slack = Slacker(os.environ.get('SLACK_BOT_TOKEN'))
botid = os.environ.get('SLACK_BOT_ID')

app = Flask(__name__)

# 이벤트 핸들하는 함수
def event_handler(event_type, slack_event, event_message):
    if event_type == "app_mention":

        print("여울이 이벤트 메세지 : " + event_message)

        # bob_recommand
        if event_message.find("밥") > -1:

            channel = slack_event["event"]["channel"]

            #slack.chat.post_message(channel, f"여울이의 추천메뉴는 {food_answer()} 입니다. 월월")

            slack.chat.post_message(channel, f"여울이가 추천해줘도 안먹을꺼 잖아요...")

            return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )

        # covid check
        elif event_message.find("코로나") > -1:

            channel = slack_event["event"]["channel"]

            attachements, username, icon_emoji = get_covid()
            print(attachements)
            print(username)
            print(icon_emoji)

            slack.chat.post_message(channel, attachments=[attachements], username=username, icon_emoji=icon_emoji)

            return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )

        # weather check
        elif event_message.find("날씨") > -1:

            channel = slack_event["event"]["channel"]

            attachements, username, icon_emoji = get_weather()

            slack.chat.post_message(channel, attachments=[attachements], username=username, icon_emoji=icon_emoji)

            return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )

        #  url shortcut
        elif event_message.find("주소단축") > -1:
            channel = slack_event["event"]["channel"]
            orignalurl = event_message.replace("주소단축 ","")
            if event_message.replace(" ","") == "주소단축":
                slack.chat.post_message(channel, f"주소단축 뒤에 주소를 넣어주시면 여울이가 줄여줄게요")

            elif event_message != surl:
                ssurl = url_short(orignalurl)
                username = '여울이가 주소를 줄여줘요!'
                icon_emoji = ''
                attachement = {
                    'pretext': '여울이의 ShortUrl',
                    "fallback": "여울이 ShortUrl",
                    "text": f"여울이가 주소를 줄였어요.  {ssurl}\n",
                    "fields": [
                        {
                            "value": "",
                            "short": False
                        }
                    ],
                    "color": "good",
                }

                slack.chat.post_message(channel, attachments=[attachement], username=username, icon_emoji=icon_emoji)

            return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )

        else:

            channel = slack_event["event"]["channel"]

            slack.chat.post_message(channel, f":welsh_corgi:여울이 명령어에오:welsh_corgi: \n밥, 코로나, 날씨, 주소단축")

            return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )

        message = "[%s] 이벤트 핸들러를 찾을 수 없습니다." % event_type

        return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/slack", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]

        event_message = slack_event["event"]["text"].replace(botid, "")

        return event_handler(event_type, slack_event, event_message)

    return make_response("슬랙 요청에 이벤트가 없습니다.", 404, {"X-Slack-No-Retry": 1})

@app.route("/kimp")
def hear():
    kimp_message = kimp.kimp()
    return kimp_message

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
