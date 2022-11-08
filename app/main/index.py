from flask import Blueprint, jsonify, render_template
from flask import current_app as app
import json
import cx_Oracle
import os
# 추가할 모듈이 있다면 추가

main = Blueprint('main', __name__, url_prefix='/')
# index 파일을 들어갔을 때, 이름을 어떻게 할 지, url_prefix는 url을 뒤에 어떻게 붙일지 결정

# config_file = os.path.join('../settings/','config.json')

# simp_path = '../settings/'
# abs_path = os.getcwd()
# print("#################" + abs_path + "#################")

LOCATION = r"C:\\oracle\\instantclient_21_7"
    # 환경변수 등록
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

with open('C:/workspace-stockping/app/settings/config.json', 'r') as f:
    config = json.load(f)
db_info = config['DB']

@main.route('/main', methods=['GET'])
def index():
    # 뉴스 데이터 가져오기

    connection = cx_Oracle.connect(user=db_info['username'], password=db_info['password'], dsn=db_info['dsn'])
    cursor = connection.cursor()
    sql = "SELECT TITLE , ORIGINALLINK FROM TB_NEWS WHERE NEWS_NUM <=30"
    cursor.execute(sql)
    news_items = cursor.fetchall()
    print("++++++++++"+ str(news_items))

    cursor.close()
    connection.close()

    return render_template('index.html', news_items=news_items)
    # return jsonify({"news": news_items})
