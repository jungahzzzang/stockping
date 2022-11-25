import requests
import json
import csv


with open('config.json', 'r') as f: #Instant Client 접속을 위한 전자지갑속 오라클 클라우드DB 정보(tnsnames.ora 파일)
    config = json.load(f)
db_info = config['DB']
HAPI_info = config['HAPI']

#실전도메인
URL_BASE = "https://openapi.koreainvestment.com:9443"


#토큰 가져오기
def load_token(path):
    f = open(path, 'r')
    line = f.readline()
    # print(line)
    f.close()
    return line

def save_csv():
    f = open('write.csv','a', newline='')#r 읽기 w 쓰기  a 추가
    wr = csv.writer(f)
    wr.writerow(nowJ())
    f.close()


def load_csv():# csv 파일 가져오기
    f = open('write.csv','r')
    rdr = csv.reader(f)
    
    for line in rdr:
        print(line)
    f.close()



token_path = "T.txt"
stream_path = "S.txt"
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
            "appkey":HAPI_info['appKey'],
            "appsecret":HAPI_info['appSecret'],
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
    print(res.json()['output']['stck_prpr'] )#주식 현재가
    # print(res.json()['output']['INVT_CAFUL_YN'] )#투자유의여부
    if res.json()['rt_cd'] != "0":
        print("에러발생")
        return 0   
    return res.json()['output']['rprs_mrkt_kor_name'], res.json()['output']['stck_prpr']





# nowJ()
# st = load_token(stream_path)

#국내주식기간별 시세 #date와 주식code에 대한.
def getStock(dataF, dataS, Jcode):

    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json",
            "authorization": f"Bearer {at}",
            "appkey":HAPI_info['appKey'],
            "appsecret":HAPI_info['appSecret'],
            "tr_id":"FHKST01010100",
            "custtype" : "P"}

    params = {
        "fid_cond_mrkt_div_code":"J",##FID 조건 시장 분류 코드 # J : 주식,  ETF ...등등
        "fid_input_iscd":Jcode,   #주식 코드(6자리)
        "FID_INPUT_DATE_1" : dataF,
        "FID_INPUT_DATE_2" : dataS,
        "FID_PERIOD_DIV_CODE" : "D",
        "FID_ORG_ADJ_PRC" : "1"
        }

    res = requests.get(URL, headers=headers, params=params)
    print(res.json())
    # print(res.json()['output']['bstp_kor_isnm'])# 업종
    # print(res.json()['output']['rprs_mrkt_kor_name'])# 시장 정보
    # print(res.json()['output']['acml_vol'])# 누적 거래량
    # print(res.json()['output']['acml_tr_pbmn']) #누적 거래 대금
    # print(res.json()['output']['prdy_vrss'])#전일 대비
    # print(res.json()['output']['prdy_vrss_sign'])# 전일 대비 부호


    # print(res.json())


fdate = "20211101"
sdate = "20221101"
jcode = "096770"
getStock(fdate, sdate, jcode)