from flask import Flask
# 추가할 모듈이 있다면 추가

app = Flask(__name__)

# 파일 이름이 index.py이므로
from app.main.index import main as main

# 위에서 추가한 파일을 연동해 주는 역할
app.register_blueprint(main)

if __name__ == '__main__' :
    app.run(debug=True)