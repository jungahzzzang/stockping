from flask import Flask, render_template, send_from_directory
import json
import urllib.request
import urllib.parse
import cx_Oracle
import os
from bs4 import BeautifulSoup as bs
import requests
from jinja2 import Template

abs_path = os.getcwd()
# print("#################" + abs_path + "#################")

with open(abs_path+'/app/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']
    api_info = config['NAVERAPI']


cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_7") # 설치한 Instant Client 경로
connection = cx_Oracle.connect(user=db_info['username'], password=db_info['password'], dsn=db_info['dsn'])


#__init__.py 파일에선 app 객체를 선언하고 각종 모듈, 데이터베이스, 블루프린트 값을 설정한다.

# 플라스크 프레임워크에서 지정한 함수 이름
def create_app():
    
    app = Flask(__name__)
    from app.home import home
    
    app.static_folder = "../static"
    app.register_blueprint(home.blueprint)  #home.py에서 사용할 blueprint 객체를 blurprint로 설정
    
    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file("/favicon.ico")
        # return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    return app