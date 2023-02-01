from app import * # main에 선언된 모든 값을 가져온다.
from flask import Blueprint

app = Flask(__name__)

blueprint = Blueprint("topfifty", __name__, template_folder="templates", static_folder="static", url_prefix="/")

@blueprint.route('/topfifty/list', methods=['GET'])
def index():
       

      

   
# 상승 순위 데이터 크롤링
   target_url3 = 'https://finance.naver.com/sise/sise_rise.naver'
   target_res3 = requests.get(target_url3)
   target_soup3 = bs(target_res3.text, 'html.parser')
   data_rows3 = target_soup3.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")


   rise = []
   for row in data_rows3:
      # 각 row마다 td를 가지고옴
      columns3 = row.find_all("td")
      # td가 1개인 것(데이터 없는 것)은 skip
      if len(columns3)<=1:
         continue
      # data = []
      _rise = []
      for column3 in columns3:
         origin = column3.get_text().strip()
         _rise.append(origin)
         
      del _rise[5:]
      rise.append(_rise)
      ##print(top_stock)
      
   number = 0
   for i in rise: # % 삭제
      rise[number][4] = (i[4][:-1])
      number = number +1
   
# 하락 순위 데이터 크롤링
   target_url4 = 'https://finance.naver.com/sise/sise_fall.naver'
   target_res4 = requests.get(target_url4)
   target_soup4 = bs(target_res4.text, 'html.parser')
   data_rows4 = target_soup4.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")


   fall = []
   for row in data_rows4:
      # 각 row마다 td를 가지고옴
      columns4 = row.find_all("td")
      # td가 1개인 것(데이터 없는 것)은 skip
      if len(columns4)<=1:
         continue
      # data = []
      _fall = []
      for column4 in columns4:
         origin = column4.get_text().strip()
         _fall.append(origin)
         
      del _fall[5:]
      fall.append(_fall)
      ##print(top_stock)
      
   number = 0
   for i in fall: # % 삭제
      fall[number][4] = (i[4][:-1])
      number = number +1
      
   return render_template('topList.html', market_sum=market_sum)
   #return render_template('topList.html', market_sum=market_sum, quant=quant, rise=rise, fall=fall)