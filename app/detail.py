from app import * # main에 선언된 모든 값을 가져온다.
from flask import Blueprint, request
from app.stock import getStock

from app.stock import getTopTen as tt
import datetime
app = Flask(__name__)
blueprint = Blueprint("detail", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@blueprint.route('/call_top_stock', methods= ['GET'])


@blueprint.route('/detail/<Jcode>', methods=['POST','GET'])
def index(Jcode):

    # time = datetime.now().strftime('%x %X')
    top_stock = getStock.call_stock("20230113","20230113",Jcode)
    
    for i in top_stock:
        print(i)
    
    # print(request.method)
    # if request.method == 'POST':
    #     stock_name = request.get("")

    # real_time = datetime.now.strftime('%H:%M:%S')
    # return render_template('subpage.html', real_time=real_time, kospi_value=kospi_value.text, kosdaq_value = kosdaq_value.text, kospi_change=kospi_change, kosdaq_change=kosdaq_change, top_stock=topten)
    return render_template('/stockdetail.html', top_stock = top_stock)
