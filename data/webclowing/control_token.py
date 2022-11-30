import requests
import json

# with open('config.json', 'r') as f: #Instant Client 접속을 위한 전자지갑속 오라클 클라우드DB 정보(tnsnames.ora 파일)
with open('../../settings/config.json', 'r') as f: #Instant Client 접속을 위한 전자지갑속 오라클 클라우드DB 정보(tnsnames.ora 파일)
    config = json.load(f)
db_info = config['DB']
HAPI_info = config['HANTOAPI']

appKey = HAPI_info['APP_KEY']
appSecret = HAPI_info['APP_SECRET']

def create_token(token_path):# 토큰발급 #기한 : 1일
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
            "appkey":appKey, 
            "appsecret":appSecret}
    PATH = "oauth2/tokenP"
    URL_BASE = "https://openapi.koreainvestment.com:9443"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))

    ACCESS_TOKEN = res.json()["access_token"]
    save_token(ACCESS_TOKEN, token_path)

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


def save_token(token_data, token_path):
    f = open(token_path, 'w')
    f.write(token_data)
    f.close()

#토큰 가져오기
def load_token(token_path):
    f = open(token_path, 'r')
    line = f.readline()
    f.close()
    return line



token_path = "T.txt"
create_token(token_path)
token = load_token(token_path)
# delet_token(token)