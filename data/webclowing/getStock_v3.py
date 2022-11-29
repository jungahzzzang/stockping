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
# stream_path = "S.txt"
at = load_token(token_path)

# s = websockk()
# s = load_token(stream_path)

# 주식현재가 시세
def nowJ():
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"
    Jcode = "005930"
    headers = {"Content-Type":"application/json", 
            "authorization": f"Bearer {at}",
            "appkey": appKey,
            "appsecret":appSecret,
            "tr_id":"FHKST01010100"}

    params = {
        "fid_cond_mrkt_div_code":"J",##FID 조건 시장 분류 코드 # J : 주식,  ETF ...등등
        "fid_input_iscd":Jcode}   #주식 코드(6자리)

    res = requests.get(URL, headers=headers, params=params)

    # print(res.json()['msg1'] )#msg1 / msg_cd / output
    print(res.json()['rt_cd'])#성공 여부
    print(res.json()['output']['rprs_mrkt_kor_name'] )#대표 시장 한글 명
    print(res.json()['output']['bstp_kor_isnm'] )#해당 주식 업종
    print(res.json()['output']['stck_oprc'] )#주식 시가 (그날 최초로 체결된 가격)
    # print(res.json()['output']['stck_oprc']) # 주식 고가
    # print(res.json()['output']['stck_oprc']) # 주식 저가
    # print(res.json()['output']['stck_clpr']) # 주식 종가
    # print(res.json()['output']['stck_prpr'] )#주식 현재가
    # print(res.json()['output']['INVT_CAFUL_YN'] )#투자유의여부
    if res.json()['rt_cd'] != "0":
        print("에러발생")
        return 0
    return res.json()['output']['rprs_mrkt_kor_name'], res.json()['output']['stck_prpr']




# nowJ()

#국내주식기간별 시세 #date와 주식code에 대한 정보.
def getStock(dataF, dataS, Jcode):

    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json",
            "authorization": f"Bearer {at}",
            "appkey" : appKey,
            "appsecret":appSecret,
            "tr_id":"FHKST01010100",
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
    print(res.json()["msg1"])
    isnm = res.json()['output']['bstp_kor_isnm']# 업종 ex) 전기.전자, 화학
    mrkt = res.json()['output']['rprs_mrkt_kor_name']# 시장 ex)KOSPI200, 코스닥
    vol = res.json()['output']['acml_vol']# 누적 거래량
    # print(res.json()['output']['acml_tr_pbmn']) #누적 거래 대금
    # print(res.json()['output']['prdy_vrss'])#전일 대비
    # print(res.json())
    return isnm, mrkt, vol

#일정 기간 데이터를 끌어올 방법을 모색중
#DB에 저장되어있는 주식코드(jcode)를 가져와서 일일단위로 for문을 돌려 거래량, 종가, 시장정보를 가져올 코드 작성할것
# 1회에는 3년치 데이터를, n회차 이후부터는 업데이트 되지 않은 정보를 insert하는 코드 작성할것
from datetime import datetime, timedelta

# 시작일,종료일 설정
start = "2021-08-01"
last = "2022-11-27"
jcode = "005930"

# 시작일, 종료일 datetime 으로 변환
start_date = datetime.strptime(start, "%Y-%m-%d")
end_date = datetime.strptime(last, "%Y-%m-%d")

# 종료일 까지 반복
while start_date <= end_date:
    dates = str(start_date.strftime("%Y%m%d"))
    print(dates)
    
    print(getStock(dates, dates, jcode))

    # 하루 더하기
    start_date += timedelta(days=1)


getStock(start_date, end_date, jcode)

#이후 nowJ같은 실시간으로 데이터를 종목별 실시간으로 데이터를 가져오는 코드 작성
# 현재 초당 get 요청횟수가 많아 오류가 발생하는것으로 보임
# server time을 이용해 메모리에 유의하여 요청횟수를 제한할것

#마지막으로, 해외 주식 정보 또한 가져올것
# 일일이 가져와 DB에 넣기보다, 그냥 가져와서 사용하면 안되나? 