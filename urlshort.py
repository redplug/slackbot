# -*- coding: utf-8 -*-

import urllib.request

import json

import html

import os

clientid = os.environ.get('NAVER_CLIENT_ID')
clientsecret = os.environ.get('NAVER_CLIENT_SECRET')

def url_short(orignalurl):
    replaceurl = html.unescape(orignalurl.replace("<", "").replace(">", "")) # 슬랙에서 링크일 경우 <> 붙여ㅓ 해당 부분 삭제
    print(replaceurl)
    index = replaceurl.find("|")  # http를 넣지 않을경우 |이후 추가적으로 문자열이 찍혀 해당 부분 삭제하기 위함
    client_id = clientid  # 개발자센터에서 발급받은 Client ID 값
    client_secret = clientsecret  # 개발자센터에서 발급받은 Client Secret 값
    encText = urllib.parse.quote(replaceurl[:index]) # index위치 이후 삭제
    data = "url=" + encText
    url = "https://openapi.naver.com/v1/util/shorturl"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        shorturl = json.loads(response_body.decode('utf-8'))
        returnurl = shorturl['result']['url']
    else:
        print("Error Code:" + rescode)

    print(returnurl)
    return html.unescape(returnurl)
