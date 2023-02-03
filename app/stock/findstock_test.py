import getStock
import insert_stock_code_
import pandas as pd
import datetime

def findStock(Jcode):
    start = "20230113"
    last = "20230113"
    stockData = getStock.call_stock(start,last,Jcode)

    return stockData

if __name__ =="__main__":
    # 홈페이지 입력값 or DB값 or 일정기간
    start = "20210801"
    last = "20221127"
    
    kospi, kosdaq = insert_stock_code_.getStockCode()
    kospi.loc()

    Jcode = kospi.iloc[0,1]
    stockData = getStock.call_stock(start,last,Jcode)

    for i in range(0,len(stockData)):
        print(stockData[i])