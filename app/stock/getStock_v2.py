import requests


headers = {
    'accept': 'application/json',
}

params = {
    'serviceKey': '9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA%3D%3D',
    # 'serviceKey': '9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA==',
    'numOfRows': '20',
    'pageNo': '1',
    'resultType': 'json',
    'basDt': '20221205',
    'itmsNm': '삼성전자',
}

# URL = 'http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo'
response = requests.get(
    # url= URL,
    'http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo',
    params=params,
    headers=headers,
)
print(response.json)


# a = requests.get("http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey=9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA%253D%253D&numOfRows=20&pageNo=1&resultType=json&basDt=20221205&itmsNm=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90")
# print(a)