from app import * # main에 선언된 모든 값을 가져온다.
from flask import Blueprint

app = Flask(__name__)

blueprint = Blueprint("topfifty", __name__, url_prefix="/")

#@blueprint.route('/main', methods=['GET'])
#def index():
   # render_template('toplist.html')