import requests
from bs4 import BeautifulSoup as bs
import urllib.parse

def crowl():
    index_url = "https://finance.naver.com/sise/"
    index_taget = urllib.request.urlopen(index_url)
    source = index_taget.read()
    index_taget.close()
    
    # 거래 순위 데이터 크롤링
    target_url = 'https://finance.naver.com/sise/sise_market_sum.naver'
    target_res = requests.get(target_url)
    target_soup = bs(target_res.text, 'html.parser')
    data_rows = target_soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    

    #데이터 전처리
    data = [] 
    for row in data_rows:
        # 각 row마다 td를 가지고옴
        columns = row.find_all("td")
        # td가 1개인 것(데이터 없는 것)은 skip
        if len(columns)<=1:
            continue
        # data = []
        top_stock = []
        for column in columns:
            origin = column.get_text().strip()
            top_stock.append(origin)
            
            
        del top_stock[5:]
        data.append(top_stock)


    return data




def selectionSort(x):
    length = len(x)
    for i in range(length-1):
        indexMin = i
        for j in range(i+1, length):
            if float(x[indexMin][-1]) > float(x[j][-1]):#정렬 기준
                indexMin = j
        x[i], x[indexMin] = x[indexMin], x[i]
            
    return x

# %기준 선택 정렬
def getPosentsort(x):
    length = len(x)
    for i in range(length-1):
        indexMin = i
        for j in range(i+1, length):
            if float(x[indexMin][-1]) > float(x[j][-1]):
                indexMin = j
        x[i], x[indexMin] = x[indexMin], x[i] 
    # data = selectionSort(data)
    x.reverse()
    return x


def get_topten(data):
    # 지수 데이터 크롤링
    
    ## 데이터 가공
    number = 0
    for i in data: # % 삭제
        data[number][4] = (i[4][:-1])
        number = number +1
    # print(data)
    
    ## 등락률
    # data = getPosentsort(data)

    topten = [] #10위까지 저장
    for i in range(0,10):
        data[i][4] = data[i][4]+'%' 
        if i < 10:
            topten.append(data[i])
            topten[i][0] = str(i+1)
    return topten

if __name__ == "__main__":
    data = crowl() # 크롤링 한 데이터
    top = get_topten(data)
    for i in top:
        print("top ten : ",i)