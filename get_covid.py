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

    print(KoreaDailyCount)
    print(KoreaAccumulateCount)

    username = '여울이COVID19알람'
    icon_emoji = ':nocovid19:'
    attachements = {
        'pretext': ':alert:여울이COVID-19 현황판:alert:',
        "fallback": "여울이COVID-19 현황판",
        "text": f"날짜 : {covid_date}\n" \
                f"신규확진자 : {KoreaDailyCount}\n" \
                f"누적확진자 : {KoreaAccumulateCount}",
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

