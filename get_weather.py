import requests
from bs4 import BeautifulSoup as bs


def get_weather(location="대치동"):
    # 값이 없을경우 대치동 날씨 정보를 불러옴.

    #네이버 날씨
    html = requests.get(f'https://search.naver.com/search.naver?query={location}날씨')

    # bs로 페이지 파싱
    soup = bs(html.text, 'html.parser')

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

    username = '여울이 Weather'
    icon_emoji = ':sun_with_face:'
    attachements = {
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


    return attachements, username, icon_emoji

if __name__ == '__main__':
    print(get_weather())
