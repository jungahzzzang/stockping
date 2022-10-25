from flask import Blueprint, request, render_template, flask, redirect, url_for
from flask import current_app as app
# 추가할 모듈이 있다면 추가

main = Blueprint('main', __name__, url_prefix='/') # url_prefix : '/'로 url을 붙여라

@main.route('/main', methods=['GET'])
def index() :
    return render_template('/main/index.html')

# if __name__ == '__main__':
    # app.run(port="9999", debug = True)
#app.run()