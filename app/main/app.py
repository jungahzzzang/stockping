#from flask import Blueprint, Flask, request, render_template, flask, redirect, url_for
from flask import Flask, render_template
# 추가할 모듈이 있다면 추가

# main = Blueprint('main', __name__, url_prefix='/') # url_prefix : '/'로 url을 붙여라
main = Flask(__name__)

@main.route('/')
def index() :
    return render_template('/main/index.html')

if __name__ == "__main__":
    main.run(debug=True)

