from flask import Flask

app = Flask(__name__)

# index.py 불러오기
from app.main.index import main as main

# index.py를 main page로 연동해줌
app.register_blueprint(main)