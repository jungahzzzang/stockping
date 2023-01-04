from app import * # main에 선언된 모든 값을 가져온다.
from flask import Blueprint

app = Flask(__name__)

blueprint = Blueprint("topfifty", __name__, template_folder="templates", static_folder="static", url_prefix="/")

@blueprint.route('/topfifty', methods=['GET'])
def index():
       
# 거래 순위 데이터 크롤링
   target_url = 'https://finance.naver.com/sise/sise_market_sum.naver'
   target_res = requests.get(target_url)
   target_soup = bs(target_res.text, 'html.parser')
   data_rows = target_soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")


   data = []
   for row in data_rows:
      # 각 row마다 td를 가지고옴
      columns = row.find_all("td")
      # td가 1개인 것(데이터 없는 것)은 skip
      if len(columns)<=1:
         continue
      # data = []
      top_stock = []
      for column in columns:
         origin = column.get_text().strip()
         top_stock.append(origin)
         
      del top_stock[5:]
      data.append(top_stock)
      ##print(top_stock)
      
   number = 0
   for i in data: # % 삭제
      data[number][4] = (i[4][:-1])
      number = number +1
   print(data)
          
   return render_template('toplist.html', top_stock=data)