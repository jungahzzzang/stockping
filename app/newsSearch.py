from app import *
import json
import os
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import datetime
import requests
import schedule
import time
from flask import Blueprint, jsonify

app = Flask(__name__)
blueprint = Blueprint("home", __name__, url_prefix="/")

abs_path = os.getcwd()

news_querys = []

with open(abs_path+'/app/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']
    api_info = config['NAVERAPI'];

def get_news(keywords, client_id, client_secret):
    
    news_items = []
    
    for keyword in keywords:
        url = "https://openapi.naver.com/v1/search/news.json"
        sort="date"
        display_num = 50
        start_num = 1

        params = {"query": keyword.encode("utf-8"), "display": display_num,
                  "start": start_num, "sort": sort}
        headers = {'X-Naver-Client-Id': client_id,
                   'X-Naver-Client-Secret': client_secret}
        r = requests.get(url, headers=headers, params=params)
        
        if r.status_code == requests.codes.ok:
            result_response = json.loads(r.content.decode('utf-8'))
            result = result_response["items"] 
            
            for item in result:
                title = item['title']
                originallink = item['originallink']
                link = item['link']
                description = item['description']
                pubDate = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
                pubDate = pubDate.strftime('%Y-%m-%d %H:%M:%S')
                title = title.replace("'", "")
                description = description.replace("'", "")
        else:
            print('request 실패!!')
            failed_msg = json.loads(r.content.decode('utf-8'))
            print(failed_msg)

        news_items.extend(result)
        
        #print(news_items)

    return news_items

def save_to_db(db_name, collection_name, docs):
    db_result = {'result':"success"}
    
    #몽고디비 연결   
    #client = MongoClient(host=my_ip, port=27017, username=username, password=password)
    client = MongoClient(db_info['MONGO_URI'])
    db = client[db_name]
    collection = db[collection_name]

    collection.create_index([("link", 1)], unique=True)
    
    try:
        collection.insert_many(docs, ordered=False)
        print("!!!!!!!!!!!!!!!!!!!inset 진행 중!!!!!!!!!!!!!!!!!!!!!!!!!")
    except BulkWriteError as bwe:
        db_result["result"] = "insert and ignore duplictated data"

    return db_result


@blueprint.route('/api/news')
def send_news():

    client = MongoClient(db_info['MONGO_URI'])   
    db = client[db_name]
    collection = db[collection_name] 
    data = list(collection.find({}).sort("pubDate",-1).limit(10)); # 최근 10개
    news_data = []
    for _data in data:
        if _data not in news_data:
            _data['_id'] = str(_data['_id'])
            news_data.append(_data)

    return jsonify({"news":news_data})
    
client_id = api_info['CLIENT_ID']
client_secret = api_info['CLIENT_SECRET']
keywords = ["경제", "주식"]

host='127.0.0.1'
username = db_info['username']
password = db_info['password']
db_name = db_info['db_name']
collection_name = db_info['news_collection']
docs = get_news(keywords, client_id, client_secret)
result = save_to_db(host, username, password, db_name, collection_name, docs)

print("I'm working...");
schedule.every().day.at("10:30").do(get_news);   #매일 10:30 실행
schedule.every().day.at("10:30").do(save_to_db);   #매일 10:30 실행

while True:
    schedule.run_pending()
    time.sleep(1)
        