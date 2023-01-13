#run.py 기준 경로
from app import *
from flask import Blueprint
from app.stock import getTopTen as gt


app = Flask(__name__)
blueprint = Blueprint("home", __name__, url_prefix="/")
abs_path = os.getcwd()

with open(abs_path+'/app/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']
    api_info = config['NAVERAPI']

    mongo_connect = db_info['MONGO_URI']
    client = MongoClient(mongo_connect)
    
    db = client.db_info['db_name']
    collection = db.db_info['collection_name']

@blueprint.route('/main', methods=['GET', 'POST'])
def index():
    
    # 지수 데이터 크롤링
    index_url = "https://finance.naver.com/sise/"
    index_taget = urllib.request.urlopen(index_url)
    source = index_taget.read()
    index_taget.close()
    
    soup = bs(source, 'html.parser', from_encoding='euc-kr')
    kospi_value = soup.find("span", id="KOSPI_now")
    kosdaq_value = soup.find("span", id="KOSDAQ_now")
    kospi_change = soup.find("span", id='KOSPI_change').text
    kosdaq_change = soup.find("span", id='KOSDAQ_change').text
    real_time = soup.find("span", id="time1").text

    # 거래 순위 데이터 크롤링
    target_url = 'https://finance.naver.com/sise/sise_market_sum.naver'
    target_res = requests.get(target_url)
    target_soup = bs(target_res.text, 'html.parser')
    data_rows = target_soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    data_index = target_soup.find("table", attrs={"class":"type_2"}).find("tbody").select("tr>td>a")
   


   
    # Q1: stock_code 50개가 각각 2개씩 총 100개 출력됩니다. 혹시 이유를 아실까요?
    stock_code_list = []
    for index in data_index:
        href = index.attrs['href']
        stockcode = href[-6:]
        # print(stockcode)
        stock_code_list.append(stockcode) 

    data = []
    for row in data_rows:
        # 각 row마다 td를 가지고옴
        columns = row.find_all("td")
        # td가 1개인 것(데이터 없는 것)은 skip
        if len(columns)<=1:
            continue
        top_stock = []
        for column in columns:
            origin = column.get_text().strip()
            top_stock.append(origin)
            

        del top_stock[5:]
        data.append(top_stock)
    

    # Q1에 대해 일단 추가해두었습니다.
    print(len(top_stock))
    for i in range(len(data)):
        data[i].append(stock_code_list[i*2])
    
    topten = gt.get_topten(data)

         
    return render_template('index.html', real_time=real_time, kospi_value=kospi_value.text, kosdaq_value = kosdaq_value.text, kospi_change=kospi_change, kosdaq_change=kosdaq_change, top_stock=topten)




# @app.route('/')
# def gotomain():
#    return render_template('/main')