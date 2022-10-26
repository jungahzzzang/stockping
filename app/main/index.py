from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
# 추가할 모듈이 있다면 추가

main = Blueprint('main', __name__, url_prefix='/')
# index 파일을 들어갔을 때, 이름을 어떻게 할 지, url_prefix는 url을 뒤에 어떻게 붙일지 결정

@main.route('/main', methods=['GET'])
def index():
    return render_template('/main/index.html')