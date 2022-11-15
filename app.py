from flask import Flask, render_template
from flask import current_app as app
import json
import urllib.request
import urllib.parse
import cx_Oracle
import os
import schedule
import time

app = Flask(__name__)

abs_path = os.getcwd()
print("#################" + abs_path + "#################")

with open(abs_path+'/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']
    api_info = config['NAVERAPI']

LOCATION = r"C:\\oracle\\instantclient_21_7"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"] 

# 뉴스 데이터 INSERT
def getNewsData():
    print("################# getNewsData #################")
    connection = cx_Oracle.connect(user=db_info['username'], password=db_info['password'], dsn=db_info['dsn'])
    cursor = connection.cursor()
    sql = "insert into tb_news values (news_seq.nextval, :title, :originallink, :link, :description, :pubDate)"
    
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

# 뉴스 데이터 SELECT
@app.route('/main', methods=['GET'])
def index():
    connection = cx_Oracle.connect(user=db_info['username'], password=db_info['password'], dsn=db_info['dsn'])
    cursor = connection.cursor()
    sql = "SELECT * FROM TB_NEWS WHERE NEWS_NUM <=30"
    cursor.execute(sql)
    news_items = cursor.fetchall()
    # print("++++++++++"+ str(news_items))

    cursor.close()
    connection.close()

    return render_template('index.html', news_items=news_items)
    # return jsonify({"news": news_items})

if __name__ == '__main__':
    app.run(debug=True)