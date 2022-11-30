import requests
import json
import csv


with open('../../settings/config.json', 'r') as f: #Instant Client 접속을 위한 전자지갑속 오라클 클라우드DB 정보(tnsnames.ora 파일)
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


token_path = "T.txt"
at = load_token(token_path)


#국내주식기간별 시세 #date와 주식code에 대한 정보.
def getStock(dataF, dataS, Jcode):

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
        "FID_INPUT_DATE_1" : dataF,
        "FID_INPUT_DATE_2" : dataS,
        "FID_PERIOD_DIV_CODE" : "D", #D:일봉 W:주봉, M:월봉, Y:년봉
        "FID_ORG_ADJ_PRC" : "1"
        }

    res = requests.get(URL, headers=headers, params=params)
    # isnm = res.json()['output']['bstp_kor_isnm']# 업종 ex) 전기.전자, 화학
    # mrkt = res.json()['output']['rprs_mrkt_kor_name']# 시장 ex)KOSPI200, 코스닥
    # vol = res.json()['output']['acml_vol']# 누적 거래량
    # print(res.json()['output']['acml_tr_pbmn']) #누적 거래 대금
    # print(res.json()['output']['prdy_vrss'])#전일 대비
    # print(res.json())
    return res.json()["output2"]
     

#일정 기간 데이터를 끌어올 방법을 모색중
#DB에 저장되어있는 주식코드(jcode)를 가져와서 일일단위로 for문을 돌려 거래량, 종가, 시장정보를 가져올 코드 작성할것
# 1회에는 3년치 데이터를, n회차 이후부터는 업데이트 되지 않은 정보를 insert하는 코드 작성할것

#주식 코드
jcode = "005930"

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# 시작일,종료일 설정
start = "2021-08-01"
last = "2022-11-27"


# 시작일, 종료일 datetime 으로 변환
startDate = datetime.strptime(start, "%Y-%m-%d")
lastDate = datetime.strptime(last, "%Y-%m-%d")


# 종료일 까지 반복
while startDate <= lastDate:
    fDate = startDate = startDate.strftime("%Y%m%d")
    startDate = datetime.strptime(startDate, "%Y%m%d")

    startDate = startDate + relativedelta(months=1)
    nextDate = startDate + relativedelta(days=-1)
    
    nextDate = nextDate.strftime("%Y%m%d")

    # print(fDate)
    # print(nextDate)
    a = getStock(fDate,nextDate,jcode)
    for i in a:
        print("거래일 : ", i['stck_bsop_date'])
        print("거래량 : ", i['acml_vol'])
        print(" 시가  : ", i['stck_oprc'])
        print(" 종가  : ", i['stck_clpr'],"\n")


# import cx_Oracle
# with open('../../settings/config.json', 'r') as f:
#     config = json.load(f)
# db_info = config['DB']
# cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_19_16") 
# # 본인이 Instant Client 넣어놓은 경로를 입력해준다
# connection = cx_Oracle.connect(user=db_info['username'], password=db_info['password'], dsn=db_info['dsn'])
# cursor = connection.cursor()
# sql ="SELECT * FROM ADMIN.TB_NEWS"
# cursor.execute(sql)
# daataa = cursor.fetchall()
