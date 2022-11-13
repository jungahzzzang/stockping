import requests
import json

def create_token():# 토큰발급 #기한 : 1일
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
            "appkey":appKey, 
            "appsecret":appSecret}
    PATH = "oauth2/tokenP"
    URL_BASE = "https://openapi.koreainvestment.com:9443"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    # res.text

    ACCESS_TOKEN = res.json()["access_token"]
    
    save_token(ACCESS_TOKEN)

    print("create token")
    return(ACCESS_TOKEN)

def delet_token(token):# 토큰제거

    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
            "appkey":appKey, 
            "appsecret":appSecret,
            "token": token
            }
    PATH = "oauth2/revokeP" # 토큰 삭제
    URL_BASE = "https://openapi.koreainvestment.com:9443"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    print(res.text)

    return res.text  
  

#해쉬 키 발급
def hash_key(datas):
    URL_BASE = "https://openapivts.koreainvestment.com:29443"
    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
      'content-Type' : 'application/json',
      'appKey' : appKey,
      'appSecret' : appSecret
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]
    print(res.text)
    return hashkey


token_path = "C:/workplace/python/stockping/data/webclowing/T.txt"
def save_token(token_data):
    f = open(token_path, 'w')
    f.write(token_data)
    f.close()

#토큰 가져오기
def load_token():
    f = open(token_path, 'r')
    line = f.readline()
    # print(line)
    f.close()
    return line



# at = create_token()
# delet_token(at)


# 주식현재가 시세
def nowJ():
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"
    Jcode = "005930"
    headers = {"Content-Type":"application/json", 
            "authorization": f"Bearer {at}",
            "appKey":appKey,
            "appSecret":appSecret,
            "tr_id":"FHKST01010100"}

    params = {
        "fid_cond_mrkt_div_code":"J",##FID 조건 시장 분류 코드 # J : 주식,  ETF ...등등
        "fid_input_iscd":Jcode}   #주식 코드(6자리)

    res = requests.get(URL, headers=headers, params=params)
    # print(res.text)
    # print(res.json()['msg1'] )#msg1 / msg_cd / output
    print(res.json()['rt_cd'] )#성공 여부
    print(res.json()['output']['rprs_mrkt_kor_name'] )#대표 시장 한글 명
    print(res.json()['output']['bstp_kor_isnm'] )#해당 주식 업종
    # print(res.json()['output']['stck_oprc'] )#주식 시가 (그날 최초로 체결된 가격)
    # print(res.json()['output']['stck_oprc']) # 주식 고가
    # print(res.json()['output']['stck_oprc']) # 주식 저가
    # print(res.json()['output']['stck_clpr']) # 주식 종가
    print(res.json()['output']['stck_prpr'] )#주식 현재가
    # print(res.json()['output']['INVT_CAFUL_YN'] )#투자유의여부
    if res.json()['rt_cd'] !=0:
        print("에러발생")
        return 0   
    return res.json()['output']['stck_prpr']








PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-price"
URL = f"{URL_BASE}/{PATH}"
at = load_token()
Jcode = "005930"
headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {at}",
        "appKey":appKey,
        "appSecret":appSecret,
        "tr_id":"FHKST01010100"}

params = {
    "fid_cond_mrkt_div_code":"J",##FID 조건 시장 분류 코드 # J : 주식,  ETF ...등등
    "fid_input_iscd":Jcode,   #주식 코드(6자리)
    "FID_PERIOD_DIV_CODE" : "D" #FID 기간 분류 코드 # D : (일)최근 30거래일
}

res = requests.get(URL, headers=headers, params=params)
# print(res.json()['msg1'] )#msg1 / msg_cd / output
# print(res.json()['output']['stck_prpr'] )#msg1 / msg_cd / output
# print(res.json()['rt_cd'] )#성공 여부
# print(res.json()['output']['rprs_mrkt_kor_name'] )#대표 시장 한글 명
# print(res.json()['output']['stck_oprc']) # 주식 시가
# print(res.json()['output']['stck_hgpr']) # 주식 고가
# print(res.json()['output']['stck_lwpr']) # 주식 저가
# print(res.json()['output']['stck_clpr']) # 주식 종가
# print(res.json()['stck_clpr'])


# # 현재 시세 가져오기
# PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
# URL = f"{URL_BASE}/{PATH}"
# Jcode = "005930"# 주식 종복 번호 (6자리)

# headers = {"Content-Type":"application/json", 
#            "authorization": load_token(),
#            "appKey":appKey,
#            "appSecret":appSecret,
#            "tr_id":"FHKST01010100"}

# params = {
#     "fid_cond_mrkt_div_code":"J", #FID 조건 시장 분류 코드 #J : 주식,  ETF, ETN
#     "fid_input_iscd":Jcode}  #종목번호 (6자리)

# res = requests.get(URL, headers=headers, params=params)
# print(res.text)
# # int(res.json()['output']['stck_prpr'])#msg1 / msg_cd / output


# """현재가 조회"""

# PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
# URL = f"{URL_BASE}/{PATH}"
# headers = {"Content-Type":"application/json", 
#            "authorization": "Bearer"+load_token(),
#         "appKey":appKey,
#         "appSecret":appSecret,
#         "tr_id":"FHKST01010100"}
# params = {
#     "fid_cond_mrkt_div_code":"J",
#     "fid_input_iscd":Jcode,
# }
# print()
# print("현재가 조회")
# res = requests.get(URL, headers=headers, params=params)
# int(res.json()['output']['stck_prpr'])
# # return int(res.json()['output']['stck_prpr'])

