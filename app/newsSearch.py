import json
import os
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import datetime
import schedule
import time
import urllib.request
import urllib.parse
import requests

abs_path = os.getcwd()

with open(abs_path+'/app/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']
    api_info = config['NAVERAPI'];

def main(*args):
    keywords = args.get('keywords', ['경제', '주식'])
    display_num = args.get('display_num', 50)
    client_id = args.get('client_id')
    client_secret = args.get('client_secret')
     
    docs = getNewsData(keywords, client_id, client_secret, display_num)
        
    result = save_mongo()

    return result
    
def getNewsData(keywords, client_id, client_secret, display_num=50):
    client_id = api_info['client_id']
    client_secret = api_info['client_secret']
    news_items = []
    
    for keyword in keywords:
        url = "https://openapi.naver.com/v1/search/news.json"
        sort = 'date'
        start_num = 1
        
        params = {'display': display_num, 'start': start_num,
                  'query': keyword.encode('utf-8'), 'sort': sort}
        headers = {'X-Naver-Client-Id': client_id,
                   'X-Naver-Client-Secret': client_secret, }
        
        r = requests.get(url, headers=headers, params=params)
        
        # request(요청)이 성공하면
        if r.status_code == requests.codes.ok:
            result_response = json.loads(r.content.decode('utf-8'))

            result = result_response['items']
            for item in result:
                title = item['title']
                originallink = item['originallink']
                link = item['link']
                description = item['description']
                pubDate = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
                pubDate = pubDate.strftime('%Y-%m-%d %H:%M:%S')
                title = title.replace("'", "")
                description = description.replace("'", "")
        # request(요청)이 성공하지 않으면        
        else:
            failed_msg = json.loads(r.content.decode('utf-8'))
            print(failed_msg)
            
        news_items.extend(result)
                
    return news_items

def save_mongo(docs):
   
    mongo_connect = db_info['MONGO_URI'];
    client = MongoClient(mongo_connect)
    
    db = client.db_info['db_name'];
    collection = db.db_info['collection_name'];
    db_result = {'result': 'success'}
    
    #뉴스 link field에 unique key 설정 - unique하게 유일한 row 데이터만 입력됨.
    collection.create_index([('link', 1)], unique=True)
    
    try:
        collection.insert_many(docs, ordered=False)
    except BulkWriteError as bwe:
        db_result['result'] = "Insert and Ignore duplicated data"
    
    return db_result

def job():
    print('working.....')
    
    # 매일 10:30에 실행
    schedule.every().day.at("10:30").do(getNewsData)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# if __name__ == "__main__":
#     main()