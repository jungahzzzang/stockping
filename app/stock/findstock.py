import getStock
import insert_stock_code_
import pandas as pd


# 홈페이지 입력값 or DB값 or 일정기간
start = "20210801"
last = "20221127"
kospi, kosdaq = insert_stock_code_.getStockCode() #DB로 변환.

# Jcode = kospi
kospi.loc()

Jcode = kospi.iloc[0,1]
stockData = getStock.call_stock(start,last,Jcode)

for i in range(0,len(stockData)):
    print(stockData[i])