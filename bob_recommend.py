# -*- coding:utf-8 -*-

import os


dbid = os.environ.get('DATABASE_ID')
dbpassword = os.environ.get('DATABASE_PASSWORD')



import mysql.connector
config = {
    "user": dbid,
    "password": dbpassword,
    "host": "127.0.0.1", #local
    "database": "bob", #Database name
    "port": "3306" #port는 최초 설치 시 입력한 값(기본값은 3306)
}

try:

    conn = mysql.connector.connect(**config)
    print(conn)
    # db select, insert, update, delete 작업 객체
    cursor = conn.cursor()
    # 실행할 select 문 구성
    sql = "SELECT * FROM bob_db ORDER BY 1 DESC"
    # cursor 객체를 이용해서 수행한다.
    cursor.execute(sql)
    # select 된 결과 셋 얻어오기
    resultList = cursor.fetchall()  # tuple 이 들어있는 list
    print(resultList)
    # DB 에 저장된 rows 출력해보기

    for result in resultList:
        seq = result[0]  # seq
        title = result[1]  # title
        content = result[2]  # content
        info = "seq:{}, title :{}, content :{}".format(seq, title, content)

        print(info)

except mysql.connector.Error as err:

    print(err)