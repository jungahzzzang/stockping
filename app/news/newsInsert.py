import os
# import sys
# 위 두 import는 필수 아님
import urllib.request
import urllib.parse
import json
import requests
import pandas as pd
import cx_Oracle
from flask import Flask, render_template, request
from requests.exceptions import SSLError
from bs4 import BeautifulSoup

def main(args):
    keywords = args.get('keywords', ['경제', '주식'])
    display_num = args.get('display_num', 100)
    client_id = args.get('client_id')
    client_secret = args.get('client_secret')

    docs = get_news(keywords, client_id, client_secret, display_num)

    result = insert_news()

    return result

def get_news(keywords, client_id, client_secret, display_num=50):
    """
    - 네이버 검색 뉴스 API를 활용해 특정 키워드들의 뉴스 검색
    - 수집 데이터를 기반으로 뉴스 item 항목에 추가
    """
    client_id="CD_wYAn2Fncz2V0cVhh0"
    client_secret="W_TLk3pV43"
    encText = urllib.parse.quote("주식")    
    news_list = []

    for i in range(1, 101+1, 100):
        # API Request
        # 1. 준비하기 - 설정값 세팅
        url = 'https://openapi.naver.com/v1/search/news.json?query='+encText # json 결과
        request = urllib.request.Request(url.format(i))
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)

        # 2.API Request
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        # Response 결과
        # 응답 결과값(JSON) 가져옥
        # Request(요청) 성공하면
        if rescode.status_code == requests.codes.ok:
            response_body = response.read()
            result_response = json.loads(response_body.decode('utf-8'))
            
            result = result_response['items']
            for item in result:
                title = item['title']
                originallink = item['originallink']
                link = item['link']
                description = item['description']
                pubDate = item['pubDate']
                title = title.replace("'", "")
                description = description.replace("'", "")
                print(description)
        # Request(요청) 실패 시        
        else:
            failed_msg = json.loads(response_body.decode('utf-8'))

        news_list.append(tuple([title, originallink, link, description, pubDate]))

        # 데이터 프레임 (df로 보면 한 눈에 확인하기 편해서)
        df = pd.DataFrame(news_list, columns=['title', 'originallink', 'link', 'description', 'pubDate'])

    return news_list

def insert_news(news_list):
    # Instant Client 경로 입력
    # LOCATION = r"C:\\oracle\\instantclient_21_7" # 윈도우

    # 환경변수 등록
    os.putenv()
    # os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"] # 윈도우

    # 오라클 클라우드 DB 사용자 이름, 비밀번호, dsn 입력
    connection = cx_Oracle.connect(user='admin', password='Tmxhrvld1234!', dsn='stockping_high') # 윈도우
   
   # 커서 생성
    cursor = connection.cursor()
    # DB 저장
    sql = "insert into tb_news values(news_seq.nextval, '{}','{}','{}','{}','{}')"
    
    cursor.executemany(sql, news_list)

    # cursor.execute(sql.format(title, originallink, link, description, pubDate))
    
    connection.commit()
    connection.close()

def scrape_image_url(url):
    """
    웹 페이지에서 og:image 링크 scraping
    :param url: 웹 페이지 url
    :return:  og:image 링크
    :rtype: str
    """

    # 기본 이미지 url  설정 / ref : https://unsplash.com/photos/1zO4O3Z0UJA
    image_url = 'https://images.unsplash.com/photo-1604594849809-dfedbc827105?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1170&q=80'

    # 1. GET Request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    try:
        data = requests.get(url, headers=headers)
    except SSLError as e :
        print(e)
        data = requests.get(url, headers=headers, verify=False)

    # 2. 특정 요소 접근하기
    # BeautifulSoup4 사용해서 html 요소에 각각 접근하기 쉽게 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # image URL 가져오기
    og_img_el = soup.select_one('meta[property="og:image"]')
    # 만약 해당 tag가 없으면 바로 기본 image_url 을 반환하고 함수 종료
    if not og_img_el:
        return image_url

    image_url = og_img_el['content']
    # 예외 - http 없는 경우 앞에 붙여주기
    if 'http' not in image_url:
        image_url = 'http:' +image_url

    return image_url

def scrape_content(url):
    """
    네이버 뉴스에서 기사 본문 scraping 해오기
    :param url: 네이버 뉴스 기사 url
    :return content 기사 본문 없으면 빈 문자열
    """

    content = ''

    # 1. GET Request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    try:
        data = requests.get(url, headers=headers)
    except SSLError as e:
        print(e)
        data = requests.get(url, headers=headers, verify=False)
    
    # 2. 특정 요소 접근하기
    soup = BeautifulSoup(data.text, 'html.parser')
    content = ''

    if 'news.naver.com' in url:
        # news naver
        naver_content = soup.select_one(
            '#articeBody') or soup.select_one('#articleBodyContents')
        
        # 해당 tag가 존재하지 않으면 기본 content return 하고 함수 종료
        if not naver_content:
            return content
        
        for tag in naver_content(['div', 'span', 'p', 'br', 'script']):
            tag.decompose()
        content = naver_content.text.strip()
    
    return content




