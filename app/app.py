from flask import Flask
# 추가할 모듈이 있다면 추가

app = Flask(__name__)

@app.route('/')
def hello_world() :
    return 'Hello World!'
app.run()