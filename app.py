from flask import Flask, jsonify, render_template
from flask import current_app as app
import json
import cx_Oracle
import os
# 추가할 모듈이 있다면 추가

app = Flask(__name__)

# config_file = os.path.join('../settings/','config.json')

# simp_path = '../settings/'
abs_path = os.getcwd()
print("#################" + abs_path + "#################")

LOCATION = r"C:\\oracle\\instantclient_21_7"
    # 환경변수 등록
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

with open(abs_path+'/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']

@app.route('/main', methods=['GET'])
def index():
    # 뉴스 데이터 가져오기

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