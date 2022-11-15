from flask import Flask, render_template
from flask import current_app as app
import json
import urllib.request
import urllib.parse
import cx_Oracle
import os
import schedule
import time
from bs4 import BeautifulSoup
from datetime import datetime
import FinanceDataReader as fdr

app = Flask(__name__)

abs_path = os.getcwd()
# print("#################" + abs_path + "#################")

with open(abs_path+'/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']
    api_info = config['NAVERAPI']

LOCATION = r"C:\\oracle\\instantclient_21_7"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"] 

def getNewsData():
    print("################# getNewsData #################")
    connection = cx_Oracle.connect(user=db_info['username'], password=db_info['password'], dsn=db_info['dsn'])
    cursor = connection.cursor()
    sql = "insert into tb_news values (news_seq.nextval, :title, :originallink, :link, :description, :pubDate)" # 뉴스 데이터 INSERT
    
    for i in range(1, 101+1, 100):
        encText = urllib.parse.quote("주식")
        url = 'https://openapi.naver.com/v1/search/news.json?query='+encText # json 결과
        request = urllib.request.Request(url.format(i))
        request.add_header("X-Naver-Client-Id",api_info['client_id'])
        request.add_header("X-Naver-Client-Secret",api_info['client_secret'])
        
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            news_list = response_body.decode('utf-8')
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
    
    cursor.close()
    connection.close()

def job():
    print('working.....')
    
    # 매일 10:30에 실행
    schedule.every().day.at("10:30").do(getNewsData)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        
@app.route('/main', methods=['GET'])
def index():
    connection = cx_Oracle.connect(user=db_info['username'], password=db_info['password'], dsn=db_info['dsn'])
    cursor = connection.cursor()
    sql = "SELECT * FROM TB_NEWS WHERE NEWS_NUM <=30" # 뉴스 데이터 SELECT
    cursor.execute(sql)
    news_items = cursor.fetchall()
    print("++++++++++"+ str(news_items))

    cursor.close()
    connection.close()
    
    # 지수 데이터 크롤링
    index_url = "https://finance.naver.com/sise/"
    index_taget = urllib.request.urlopen(index_url)
    source = index_taget.read()
    index_taget.close()
    
    soup = BeautifulSoup(source, 'html.parser', from_encoding='euc-kr')
    kospi_value = soup.find("span", id="KOSPI_now")
    kosdaq_value = soup.find("span", id="KOSDAQ_now")
    kospi_change = soup.find("span", id='KOSPI_change').text
    kosdaq_change = soup.find("span", id='KOSDAQ_change').text
    
    # 거래 순위 데이터 크롤링
    rank_url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0"
    rank_target = urllib.request.urlopen(rank_url)
    source = rank_target.read()
    rank_target.close()
    
    soup = BeautifulSoup(source, 'html.parser', from_encoding='euc-kr')
    #event_name 
    #current_price =
    #previous =
    #fluctu =
    
    
    return render_template('index.html', news_items=news_items, kospi_value=kospi_value.text, kosdaq_value = kosdaq_value.text, kospi_change=kospi_change, kosdaq_change=kosdaq_change)
    # return jsonify({"news": news_items})
    
if __name__ == '__main__':
    app.run(debug=True)