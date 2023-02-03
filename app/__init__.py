from flask import Flask, render_template, send_from_directory
import json
from pymongo import MongoClient
import os
from bs4 import BeautifulSoup as bs
import urllib.request
import urllib.parse
import requests


abs_path = os.getcwd()

with open(abs_path+'/app/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']
    api_info = config['NAVERAPI']

    mongo_connect = db_info['MONGO_URI']
    client = MongoClient(mongo_connect)

#__init__.py 파일에선 app 객체를 선언하고 각종 모듈, 데이터베이스, 블루프린트 값을 설정한다.
# 플라스크 프레임워크에서 지정한 함수 이름
def create_app():
    
    app = Flask(__name__)
    from . import home
    from . import topfifty
    from . import board
    from . import detail
    
    app.register_blueprint(home.blueprint)  #home.py에서 사용할 blueprint 객체를 blurprint로 설정
    app.register_blueprint(topfifty.blueprint)
    app.register_blueprint(board.blueprint)
    app.register_blueprint(detail.blueprint)
    
    return app