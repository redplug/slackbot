# -*- coding: utf-8 -*-

import os

import json

from slacker import Slacker

from flask import Flask, request, make_response

import requests

from bs4 import BeautifulSoup

import string

from selenium import webdriver

from urlshort import url_short

from bob_recommend import food_answer

from get_coin import get_coin


bob = "밥"

covid = "코로나"

weather = "날씨"

coin = "코인"

currency = "환율"

surl = "주소단축"

slack = Slacker(os.environ.get('SLACK_BOT_TOKEN'))
botid = os.environ.get('SLACK_BOT_ID')

app = Flask(__name__)

def get_weather():
    location = "대치동"
    html = requests.get(f'https://search.naver.com/search.naver?query={location}날씨')

    soup = BeautifulSoup(html.text, 'html.parser')

    data1 = soup.find('div', {'class': 'weather_box'})
    find_address = data1.find('span', {'class': 'btn_select'}).text
    find_currenttemp = data1.find('span', {'class': 'todaytemp'}).text

    data2 = data1.findAll('dd')
    find_dust = data2[0].find('span', {'class': 'num'}).text
    find_ultra_dust = data2[1].find('span', {'class': 'num'}).text
    find_temp = soup.select('div > div > div > div > div > ul > li > p')[0].text
    find_low_temp = soup.select('div > div > ul > li > span > span > span')[0].text
    find_high_temp = soup.select('div > div > ul > li > span > span > span')[1].text
    find_windchill = soup.select('div > div > ul > li > span > em > span')[0].text

    return find_address, find_currenttemp, find_dust, find_ultra_dust, find_temp, find_low_temp, find_high_temp, find_windchill


find_address, find_currenttemp, find_dust, find_ultra_dust, find_temp, find_low_temp, find_high_temp, find_windchill = get_weather()


def get_covid():
    req = requests.get(
        'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=')

    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    coviddate = soup.select('div > h5 > span')[0].text.strip(string.punctuation)

    KoreaDailyCount = soup.select('div > div > div > ul > li > dl > dd > ul > li > p')[0].text.strip(
        string.punctuation).strip()

    KoreaAccumulateCount = soup.select('div > div > div > ul > li > dl > dd')[0].text.strip(string.punctuation)

    return coviddate, KoreaDailyCount, KoreaAccumulateCount

def _close_chrome(chrome: webdriver):
    """
    크롬 종료

    :param chrome: 크롬 드라이버 인스턴스
    """
    def close():
        chrome.close()
    return close

# 이벤트 핸들하는 함수
def event_handler(event_type, slack_event, event_message):
    if event_type == "app_mention":

        print("여울이 이벤트 메세지 : " + event_message)

        if event_message.find(bob) > -1:

            channel = slack_event["event"]["channel"]

            #foodanswer = get_answer()

            foodanswer = food_answer()

            slack.chat.post_message(channel, f"여울이의 추천메뉴는 {foodanswer} 입니다. 월월")

            return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )

        elif event_message.find(covid) > -1:

            channel = slack_event["event"]["channel"]

            covid_date, covid_dailycount, covid_accumulatecount = get_covid()

            username = '여울이COVID19알람'
            icon_emoji = ':nocovid19:'
            attachement = {
                'pretext': ':alert:여울이COVID-19 현황판:alert:',
                "fallback": "여울이COVID-19 현황판",
                "text": f"날짜             : {covid_date}\n 신규확진자 : {covid_dailycount}\n 누적확진자 : {covid_accumulatecount}",
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

        elif event_message.find(weather) > -1:

            channel = slack_event["event"]["channel"]

            find_address, find_currenttemp, find_dust, find_ultra_dust, find_temp, find_low_temp, find_high_temp, find_windchill = get_weather()

            username = '여울이 Weather'
            icon_emoji = ':sun_with_face:'
            attachement = {
                'pretext': ':sun_with_face:여울이의 날씨알람:sun_with_face:',
                "fallback": "여울이 Weather",
                "text": f" \n \
                {find_address}의 날씨정보 입니다.\n \
현재 날씨 : {find_temp}℃\n \
현재 온도 : {find_currenttemp}℃\n \
최저 기온 : {find_low_temp}℃\n \
최고 기온 : {find_high_temp}℃\n \
체감 온도 : {find_windchill}℃\n \
미세 먼지 : {find_dust}\n \
초미세 먼지 : {find_ultra_dust} \
",
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

        elif event_message.find(coin) > -1:
            channel = slack_event["event"]["channel"]
            print(event_message.replace(" ",""))
            print(coin)
            print(type(event_message.replace(" ","")))
            print(type(coin))
            if event_message.replace(" ","") == coin:
                tickers = pyupbit.get_tickers(fiat="KRW")
                slack.chat.post_message(channel, f"티커리스트(KRW) : {tickers}")
            elif event_message != coin:
                df, price, per = get_coin(event_message)
                print(event_message)
                print(df[["open","close","Date"]].style.hide_index())
                print(price)
                username = '여울이COIN 알람'
                icon_emoji = ':coin:'
                attachement = {
                    'pretext': ':coin:여울이COIN 알람:coin:',
                    "fallback": "여울이COIN 알람",
                    "text": f"현재가격은 : {price} {per}\n {df.to_string(index=False)}",
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

        elif event_message.find(surl) > -1:
            channel = slack_event["event"]["channel"]
            orignalurl = event_message.replace("주소단축 ","")
            print(surl)
            if event_message.replace(" ","") == surl:
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)