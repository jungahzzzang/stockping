# #json
# import requests

# headers = {
#     'accept': 'application/json',
# }

# params = {
#     # 'serviceKey': '9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA%3D%3D',
#     'serviceKey': '9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA==',
#     'numOfRows': '10',
#     'pageNo': '10000',
#     # 'resultType': 'json',
#     'basDt': '20211201',
# }

# # params = {
# #     'serviceKey': '9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA%3D%3D',
# #     'numOfRows': '10',
# #     'pageNo': '10000',
# #     'resultType': 'json',
# # }

# response = requests.get('https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo', params=params, headers=headers, verify=False) 
# # response = requests.get('https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey=9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA%253D%253D&numOfRows=10&pageNo=1000&resultType=json', verify=False) 
# print(response.text)



#xml
import requests
response = requests.get('https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey=9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA%3D%3D&numOfRows=10&pageNo=1000&resultType=json')

import requests

headers = {
    'accept': 'application/xml',
}

params = {
    # 'serviceKey': '9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA==',
    'serviceKey': '9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA%3D%3D',
    'numOfRows': '10',
    'pageNo': '1000',
    'resultType': 'xml',
}

response = requests.get('https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo', params=params, headers=headers, verify=False)





# import urllib.request
# import xml.dom.minidom

# encodingKey = "9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA%3D%3D"
# decodingKey = "9DgV2rhVrUef40rwgpaDjWxHQdFR0HU5xYS9TEK2bv20x92pptTdPhaSs43BnOFYEqcPi1rQw2oThMzVZt1ObA=="

# print("[START]")

# # request url정의
# url = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey="+ decodingKey+"&numOfRows=10&pageNo=10000&basDt=20211201"
# request = urllib.request.Request(url)

# # request보내기
# response = urllib.request.urlopen(request)

# # 결과 코드 정의
# rescode = response.getcode()

# if(rescode==200):
#     response_body = response.read()
#     dom = xml.dom.minidom.parseString(response_body.decode('utf-8'))
#     pretty_xml_as_string = dom.toprettyxml()
#     print(pretty_xml_as_string)
# else:
#     print("Error Code:" + rescode)

# print("[END]")




# #http response test
# import requests

# response = requests.get("https://www.naver.com")
# data = response.text
# print(data)
#정상작동. 