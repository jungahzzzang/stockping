import requests
import json
import csv


with open('../settings/config.json', 'r') as f: 
    config = json.load(f)
db_info = config['DB']
HAPI_info = config['HANTOAPI']

appKey = HAPI_info['APP_KEY']
appSecret = HAPI_info['APP_SECRET']
#실전도메인
URL_BASE = "https://openapi.koreainvestment.com:9443"

#토큰 가져오기
def load_token(path):
    f = open(path, 'r')
    line = f.readline()
    # print(line)
    f.close()
    return line


token_path = "../settings/token.txt"
at = load_token(token_path)


#받은 데이터를 이름, 날짜, 종가, 체결량을 dict형태로 만들어준다.
def setDateFrame(data):
    df = []
    
    name = data['output1']['hts_kor_isnm']
    for i in range(0,len(data['output2'])):
        date = data['output2'][i]['stck_bsop_date']
        price = data['output2'][i]['stck_clpr']
        deal = data['output2'][i]['acml_vol']

        dict_data = {
            'name' : f"{name}",     # 이름
            'date' : f"{date}",     # 날짜
            'price' : f"{price}",   # 당일 종료 가격
            'deal' : f"{deal}"      # 체결량
        }
    
        df.append(dict_data)

    return df


#국내주식기간별 시세 #date와 주식code에 대한 정보.
def getStock(startDate, endDate, Jcode):

    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json",
            "authorization": f"Bearer {at}",
            "appkey" : appKey,
            "appsecret":appSecret,
            "tr_id":"FHKST03010100",
            "custtype" : "P"}

    params = {
        "fid_cond_mrkt_div_code":"J",##FID 조건 시장 분류 코드 # J : 주식,  ETF ...등등
        "fid_input_iscd":Jcode,   #주식 코드(6자리)
        "FID_INPUT_DATE_1" : startDate,
        "FID_INPUT_DATE_2" : endDate,
        "FID_PERIOD_DIV_CODE" : "D", #D:일봉 W:주봉, M:월봉, Y:년봉
        "FID_ORG_ADJ_PRC" : "1"
        }
    res =  requests.get(URL, headers=headers, params=params)
    # print(res.json())



    print(startDate)
    # print(check_date)
    print(endDate)

    #판다스로 바꾼다면? 억지?
    df = setDateFrame(res.json())
    print(len(df))
    


    check_date = res.json()['output2'][-1]['stck_bsop_date']
    if startDate<check_date:
        startDate = check_date


        getStock(startDate,endDate,Jcode)
        # print("appenddf: ",df)


    # for i in df:
    #     print(i)
    return df







#일정 기간 데이터를 끌어올 방법을 모색중
#추후 DB에 저장되어있는 주식코드(jcode)를 가져와서 일일단위로 for문을 돌려 거래량, 종가, 시장정보를 가져올 코드 작성할것

#모두 스캔하여 가져오는 주식 코드
# import insert_stock_code_
# stockCode = insert_stock_code_.getStockCode()


jcode = "005930"

# 시작일,종료일 설정
start = "20190101"
last = "20220207"

# 0. 'stck_bsop_date': '20221209',  영업일자 
# 1. 'stck_clpr': '46300',          주식 종가
# 2. 'stck_oprc': '45400',          주식 시가
# 3.  'stck_hgpr': '46450',         주식 최고가
# 4.  'stck_lwpr': '44950',         주식 최저가
# 5.  'acml_vol': '25740',          주식 누적 거래량
# 6.  'acml_tr_pbmn': '1183410750', 주식 거래 대금
# 7.  'flng_cls_code': '00',        락 구분 코드
# 8.  'prtt_rate': '0.00',          분할 비율
# 9.  'mod_yn': 'N',                분할변경여부
# 10. 'prdy_vrss_sign': '2',        전일 대비 부호
# 11. 'prdy_vrss': '1250',          전일 대비 수치
total = getStock(start,last,jcode) # 한번 요청할 때 100개.
# print(len(token_path))
## name = 주식이름, date = 날짜, price = 당일 종료 가격, deal = 거래량

