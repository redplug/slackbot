# -*- coding:utf-8 -*-

import os

import mysql.connector

import random

def food_answer():
    dbid = os.environ.get('DATABASE_ID')
    dbpassword = os.environ.get('DATABASE_PASSWORD')

    config = {
        "user": dbid,
        "password": dbpassword,
        "host": "localhost", #local
        "database": "bob_db", #Database name
        "port": "3306" #port는 최초 설치 시 입력한 값(기본값은 3306)
    }

    try:

        conn = mysql.connector.connect(**config)
        print(conn)
        # db select, insert, update, delete 작업 객체
        cursor = conn.cursor()
        # 실행할 select 문 구성
        sql = "SELECT MAX(number) FROM bob"
        # cursor 객체를 이용해서 수행한다.
        cursor.execute(sql)
        # select 된 결과 셋 얻어오기
        resultList = cursor.fetchall()  # tuple 이 들어있는 list
        size = resultList[0][0]
        print(size)
        random_select = random.randrange(1,int(size))+1
        sql = f"SELECT name,url FROM bob where number = {random_select}"
        cursor.execute(sql)
        resultList = cursor.fetchall()  # tuple 이 들어있는 list
        result = f"<{resultList[0][1]}|*{resultList[0][0]}*>"
        return result

    except mysql.connector.Error as err:

        print(err)