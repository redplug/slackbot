import string

import requests
from bs4 import BeautifulSoup


def get_covid():
    req = requests.get(
        'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=')

    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    covid_date = soup.select('div > h5 > span')[0].text.strip(string.punctuation)

    KoreaDailyCount = soup.select('div > div > div > ul > li > dl > dd > ul > li > p')[0].text.strip(string.punctuation).strip()

    KoreaAccumulateCount = soup.select('div > div > div > ul > li > dl > dd')[0].text.strip(string.punctuation)

    username = '여울이COVID19알람'
    icon_emoji = ':nocovid19:'
    attachements = {
        'pretext': ':alert:여울이COVID-19 현황판:alert:',
        "fallback": "여울이COVID-19 현황판",
        "text": f"날짜             : {covid_date}\n \
                    신규확진자 : {KoreaDailyCount}\n \
                    누적확진자 : {KoreaAccumulateCount}",
        "fields": [
            {
                "value": "",
                "short": False
            }
        ],
        "color": "good",
    }


    return attachements, username, icon_emoji, KoreaDailyCount, KoreaAccumulateCount


if __name__ == '__main__':
    print(get_covid()[0])
    print(get_covid()[1])
    print(get_covid()[2])
