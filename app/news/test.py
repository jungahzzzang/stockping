import os
# import sys
# 위 두 import는 필수 아님
import urllib.request
import urllib.parse
import json
import pandas as pd
import cx_Oracle

# Instant Client 경로 입력
LOCATION = r"C:\\oracle\\instantclient_21_7"

# 환경변수 등록
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

# 오라클 클라우드 DB 사용자 이름, 비밀번호, dsn 입력
connection = cx_Oracle.connect(user='admin', password='Tmxhrvld1234!', dsn='stockping_high')

# 커서 생성
cursor = connection.cursor()

# DB 저장
sql = "insert into tb_news values(news_seq.nextval, '{}','{}','{}','{}','{}')"

client_id="CD_wYAn2Fncz2V0cVhh0"
client_secret="W_TLk3pV43"
encText = urllib.parse.quote("주식")

for i in range(1, 101+1, 100):

    url = 'https://openapi.naver.com/v1/search/news.json?query='+encText # json 결과
    request = urllib.request.Request(url.format(i))
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        news_list = json.loads(response_body.decode('utf-8'))
        print(news_list)
        items = news_list['items']
        for item in items:
            title = item['title']
            originallink = item['originallink']
            link = item['link']
            description = item['description']
            pubDate = item['pubDate']
            title = title.replace("'", "")
            description = description.replace("'", "")
            print(description)
            cursor.execute(sql.format(title, originallink, link, description, pubDate))
    else:
        print("Error Code:"+rescode)

connection.commit()
connection.close()






