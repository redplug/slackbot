# -*- coding: utf-8 -*-
import string

import requests
from bs4 import BeautifulSoup


def get_covid():
    req = requests.get('http://ncov.mohw.go.kr/')

    html = req.text

    soup = BeautifulSoup(html, 'html.parser')
    
    # 접종기준날짜
    # vaccinDate = soup.select('#content > div > div > div.liveboard_layout > div.liveToggleOuter > div > div.live_left > div.vaccineNum > h2 > span')[0].text.strip(string.punctuation).split(",")[0]
    firstInoculation = soup.select('#content > div > div > div.liveboard_layout > div.liveToggleOuter > div > div.live_left > div.vaccineNum > div > div > div:nth-child(1) > ul:nth-child(1) > li.percent')[0].text.strip(string.punctuation)
    clearInoculation = soup.select('#content > div > div > div.liveboard_layout > div.liveToggleOuter > div > div.live_left > div.vaccineNum > div > div > div:nth-child(2) > ul:nth-child(1) > li.percent')[0].text.strip(string.punctuation)
    covidDate = soup.select('#content > div > div > div.liveboard_layout > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > h2 > span')[0].text.strip(string.punctuation).split(",")[0]
    dailyCovidCount = soup.select('#content > div > div > div.liveboard_layout > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_graph > table > tbody > tr:nth-child(1) > td:nth-child(5) > span')[0].text.strip(string.punctuation)
    totalCovidCount = soup.select('#content > div > div > div.liveboard_layout > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_num > div:nth-child(2)')[0].text.strip(string.punctuation).replace('누적)확진','').replace('다운로드','')

    username = '여울이COVID19알람'
    icon_emoji = ':nocovid19:'
    attachements = {
        'pretext': ':alert:여울이COVID-19 현황판:alert:',
        "fallback": "여울이COVID-19 현황판",
        "text": f"발생현황날짜 : {covidDate}\n" \
                f"일일확진 : {dailyCovidCount}\n" \
                f"누적확진 : {totalCovidCount}\n"                
                f"1차접종 : {firstInoculation}%\n" \
                f"접종완료 : {clearInoculation}%\n",
        "fields": [
            {
                "value": "",
                "short": False
            }
        ],
        "color": "good",
    }

    
    return attachements, username, icon_emoji


if __name__ == '__main__':
    test1,test2,test3 = get_covid()
    print(test1)
