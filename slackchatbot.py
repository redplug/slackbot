# -*- coding: utf-8 -*-

import os

import json

from slacker import Slacker

from flask import Flask, request, make_response

import random

import requests

from bs4 import BeautifulSoup

import atexit

import string

import pyupbit

from selenium import webdriver

from urlshort import url_short

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

import datetime

bob = "밥"

covid = "코로나"

weather = "날씨"

coin = "코인"

currency = "환율"

surl = "주소단축"

slack = Slacker(os.environ.get('SLACK_BOT_TOKEN'))
botid = os.environ.get('SLACK_BOT_ID')

app = Flask(__name__)


def get_answer():
    food = ['<https://map.naver.com/v5/search/%ED%9D%AC%EB%9E%98%EB%93%B1/place/31398765?c=14141304.0776130,4508977.3027141,13,0,0,0,dh|*희래등*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%96%8C%EC%83%98%EA%B9%80%EB%B0%A5/place/1411505334?placeSearchOption=fromNxList=true%26noredirect=1%26entry=pll&c=14141012.6614427,4510515.5979084,13,0,0,0,dh&placePath=%2Fhome%3Fentry=pll|*얌샘*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EB%B6%80%EC%82%B0%EC%95%84%EC%A7%80%EB%A7%A4/place/1161628944?c=14143649.7389185,4509919.6279535,15,0,0,0,dh|*부산아지매*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EB%82%A8%EC%82%B0%EC%98%A5/place/20259836?c=14143649.7389185,4509919.6279535,15,0,0,0,dh|*남산옥*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EB%9D%BD%EC%8A%A4%ED%94%8C%EB%A0%88%EC%9D%B4%ED%8A%B8/place/19536440?c=14143649.7389185,4509919.6279535,15,0,0,0,dh|*락스플레이트*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EA%B5%90%EB%8F%99%EC%A0%84%EC%84%A0%EC%83%9D/place/36160929?c=14143936.3777746,4508912.8089715,14,0,0,0,dh|*교동전선생*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EA%B8%B8%EB%86%8D%EC%9B%90/place/34520779?c=14143936.3777746,4508912.8089715,14,0,0,0,dh|*길농원*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EB%AA%85%EB%8F%99%EC%B9%BC%EA%B5%AD%EC%88%98/place/1551854356?c=14143926.8231461,4510237.3193523,15,0,0,0,dh|*명동칼국수*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EB%8F%99%ED%95%B4%ED%9A%9F%EC%A7%91?c=14144464.2710012,4509907.6846678,15,0,0,0,dh|*동해횟집*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EB%82%A8%EC%9B%90%EC%B6%94%EC%96%B4%ED%83%95/place/20624013?c=14144486.9632440,4510261.8030879,16,0,0,0,dh|*남원추어탕*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EB%B0%B1%EA%B5%AC%EC%8B%9D%EB%8B%B9/place/12884436?c=14144563.4002722,4510162.6738168,16,0,0,0,dh|*백구식당*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%82%BC%EA%B5%B0%EA%B9%80%EC%B9%98%EC%B0%8C%EA%B0%9C/place/757870494?c=14144024.7580885,4510270.7605521,15,0,0,0,dh&placePath=%3F%2526|*삼군김치찌개*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%82%BC%EC%84%B1%EA%B3%A8/place/495083414?c=14143871.8840320,4510215.8214381,15,0,0,0,dh&placePath=%3F%2526|*삼성골*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%86%A1%EB%8B%B4%EC%B6%94%EC%96%B4%ED%83%95/place/1951213845?c=14141031.7706998,4510563.3710510,13,0,0,0,dh&placePath=%3F%2526|*송담추어탕*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%98%88%EC%9E%90%EB%84%A4%EB%B0%A5%EC%83%81/place/37997070?c=14141241.9725275,4510458.2701372,13,0,0,0,dh|*예자네밥상*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%9A%B0%EB%A6%AC%EC%A7%91/place/18824809?c=14143874.2726891,4510256.4286093,15,0,0,0,dh|*우리집*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%9D%B4%ED%83%9C%EB%A6%AC%EB%B6%80%EB%8C%80%EC%B0%8C%EA%B0%9C/place/1763681004?c=14143076.4612064,4510350.7805661,14,0,0,0,dh|*이태리부대찌개*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%9E%84%EA%B3%A0%EC%A7%91%ED%95%9C%EC%9A%B0/place/13192719?c=14143076.4612064,4510350.7805661,14,0,0,0,dh|*임고집한우*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%A0%84%EC%A3%BC%EC%BD%A9%EB%82%98%EB%AC%BC%EA%B5%AD%EB%B0%A5/place/32602528?c=14143100.3477777,4510374.6671375,14,0,0,0,dh|*전주콩나물국밥*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%A1%B1%EB%B0%9C%EB%B3%B4%EC%8C%88%EB%A7%88%EC%9D%84/place/32594023?c=14143100.3477777,4510374.6671375,14,0,0,0,dh|*족발보쌈마을*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%B9%B4%EB%A0%88%EB%A7%88%EC%B9%98/place/37130941?c=14143100.3477777,4510374.6671375,14,0,0,0,dh|*카레마치*>', \
        '<http://freshville.co.kr/|*후레쉬빌*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%EC%82%AC%EC%A1%B0%EC%B0%B8%EC%B9%98/place/13175130?c=14144574.1492293,4510556.8022439,16,0,0,0,dh|*사조참치*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%ED%8F%AC%ED%8F%AC%EB%B9%88/place/1215767360?c=14144574.1492293,4510556.8022439,16,0,0,0,dh|*포포빈*>', \
        '<https://map.naver.com/v5/search/%EB%8C%80%EC%B9%98%EB%8F%99%20%ED%81%AC%EB%9D%BC%EC%9D%B4%EB%B2%84%EA%B1%B0/place/587929920?c=14144574.1492293,4510556.8022439,16,0,0,0,dh|*크라이*>', \
        '<|*배달*>', \
        '<|*여울이도 밥주세오*>', \
        '<https://map.naver.com/v5/entry/place/13172001?c=14143887.9251101,4509407.0234595,15,0,0,0,dh&placePath=%3Fentry=plt|*희래등*>']

    random.shuffle(food)
    return food


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

# 코인 계산 함수
def get_coin(coin):
    if coin == None:
        tickers = pyupbit.get_tickers()
        return tickers
    elif coin != None:
        coin = coin.replace(" ","")
        ticker = coin.replace("코인","")

        price = pyupbit.get_current_price(ticker)
        df = pyupbit.get_ohlcv(ticker, count=3, interval="day")
        del df['volume']
        df['Date'] = df.index
        return df, price

def _close_chrome(chrome: webdriver):
    """
    크롬 종료

    :param chrome: 크롬 드라이버 인스턴스
    """
    def close():
        chrome.close()
    return close

# 환율 계산 함수
# def currency_dollar_won(date):
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=chrome_options)
#     driver.get('http://www.smbs.biz/ExRatePop/ExRateCalc.jsp')
#     if date == None:
#         pass
#     # elif date != None:
#     #     driver.find_element_by_id('searchDate').send_keys(Keys.CONTROL + "a");
#     #     driver.find_element_by_id('searchDate').send_keys(Keys.DELETE);
#     #     driver.find_element_by_name('searchDate').send_keys(date)
#     #     driver.find_element_by_css_selector('a').send_keys('\n')
#
#     ##환율(원)
#     currency_won = driver.find_element_by_xpath('//*[@id="tblRate"]/tbody/tr[1]/td[2]')
#     print(f'currency_won : {currency_won.text}')
#     atexit.register(_close_chrome(driver))
#
#     return currency_won

# 이벤트 핸들하는 함수
def event_handler(event_type, slack_event, event_message):
    if event_type == "app_mention":

        print("여울이 이벤트 메세지 : " + event_message)

        if event_message.find(bob) > -1:

            channel = slack_event["event"]["channel"]

            foodanswer = get_answer()

            slack.chat.post_message(channel, f"여울이의 추천메뉴는 {foodanswer[0]} 입니다. 월월")

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
                df, price = get_coin(event_message)
                print(event_message)
                print(df[["open","high","low","close"]].style.hide_index())
                print(price)
                username = '여울이COIN 알람'
                icon_emoji = ':coin:'
                attachement = {
                    'pretext': ':coin:여울이COIN 알람:coin:',
                    "fallback": "여울이COIN 알람",
                    "text": f"현재가격은 : {price}\n {df.to_string(index=False)}",
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