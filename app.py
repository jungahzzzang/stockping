from flask import Flask, render_template
from flask import current_app as app
import json
import urllib.request
import urllib.parse
import cx_Oracle
import os
import schedule
import time
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import requests
import pandas as pd

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
    dsn_info = cx_Oracle.makedsn('')
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
    sql = "SELECT * FROM TB_NEWS WHERE NEWS_NUM <=25" # 뉴스 데이터 SELECT
    cursor.execute(sql)
    news_items = cursor.fetchall()
    # print("++++++++++"+ str(news_items))

    cursor.close()
    connection.close()
    
    # 지수 데이터 크롤링
    index_url = "https://finance.naver.com/sise/"
    index_taget = urllib.request.urlopen(index_url)
    source = index_taget.read()
    index_taget.close()
    
    soup = bs(source, 'html.parser', from_encoding='euc-kr')
    kospi_value = soup.find("span", id="KOSPI_now")
    kosdaq_value = soup.find("span", id="KOSDAQ_now")
    kospi_change = soup.find("span", id='KOSPI_change').text
    kosdaq_change = soup.find("span", id='KOSDAQ_change').text

    # 거래 순위 데이터 크롤링
    target_url = 'https://finance.naver.com/sise/sise_market_sum.naver'
    #target_url = 'https://finance.naver.com/sise/'
    target_res = requests.get(target_url)
    target_soup = bs(target_res.text, 'html.parser')
    # tbody = target_soup.find('tbody')
    # trs = tbody.find_all('tr', attrs={'onmouseover': 'mouseOver(this)'})
    data_rows = target_soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    # data_rows = target_soup.find_all('tr',attrs={"id" : "siselist_tab_7"})
    for row in data_rows:
        # 각 row마다 td를 가지고옴
        columns = row.find_all("td")
        # td가 1개인 것(데이터 없는 것)은 skip
        if len(columns)<=1:
            continue
        top_stock=[]
        # data = []
        for column in columns:
            origin = column.get_text().strip()
            top_stock.append(origin)
            del top_stock[5:]
        
        for i in range(0, top_stock.__len__()):
            data = [top_stock[i:i+5] for i in range(0, len(top_stock), 5)]
            print(data)        
        df = pd.DataFrame([top_stock], columns=['Num', 'Name', 'Today', 'Yesterday', 'High'])
        json_output = df.to_json()
        json_output = json.loads(json_output.replace("\'", '"'))
        #print(json_output)
    
        
        # startPos = 0
        # dataLength = top_stock.__len__()
        # for i in range(startPos, dataLength):
        #     after = [top_stock[i:i+5] for i in range(0, len(top_stock), 5)]
        #     print('****'+str(after))
        
        #top_stock = [data[i:i+5] for i in range(0, len(data), 5)]
        
        
        
        # print('최종최종최종최종'+str(top_stock))
        # top_stock.append([name, today, yesterday, high])
    
    
    
          
    return render_template('index.html', news_items=news_items, kospi_value=kospi_value.text, kosdaq_value = kosdaq_value.text, kospi_change=kospi_change, kosdaq_change=kosdaq_change, top_stock=data)
    
if __name__ == '__main__':
    app.run(debug=True)