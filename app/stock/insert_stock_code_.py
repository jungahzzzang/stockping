import pandas as pd
import json


# 종목 코드 정렬
def getStockCode():
    url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'

    kospi_code = pd.read_html(url+"?method=download&marketType=stockMkt")[0]
    kosdaq_code = pd.read_html(url+"?method=download&marketType=kosdaqMkt")[0]

    kospi_code = kospi_code[['회사명','종목코드']]
    kosdaq_code = kosdaq_code[['회사명','종목코드']]

    def make_code_ks(x):
        x = str(x)
        return '0'*(6-len(x))+x

    def make_code_kq(x):
        x = str(x)
        return '0'*(6-len(x))+x
        
    kospi_code['종목코드'] = kospi_code['종목코드'].apply(make_code_ks)
    kosdaq_code['종목코드'] = kosdaq_code['종목코드'].apply(make_code_kq)

    return kospi_code, kosdaq_code


def cursorLoad():
    
    with open('../settings/config.json', 'r') as f: #몽고DB 정보(tnsnames.ora 파일)
        config = json.load(f)
    db_info = config['DB']


    kospi, kosdaq = getStockCode()

    ### 몽고 DB에 맞게 쿼리문을 수정해야함.
    # for i in range(0,len(kospi),1):
    #     try:
    #         sql = f"INSERT INTO ADMIN.TB_STOCK_INFO (IDX, STOCK_CODE, STOCK_NAME) VALUES(STOCK_SEQ.NEXTVAL, '{kospi['종목코드'][i]}', '{kospi['회사명'][i]}')"

    #     except:
    #         print(i," 번째 오류, 다시시도")
    #         i = i-1

    # for j in range(0,len(kosdaq),1):
    #     try:
    #         sql = f"INSERT INTO ADMIN.TB_STOCK_INFO (IDX, STOCK_CODE, STOCK_NAME) VALUES(STOCK_SEQ.NEXTVAL, '{kosdaq['종목코드'][j]}', '{kosdaq['회사명'][j]}')"

    #     except:
    #         print(j," 번째 오류, 다시시도")
    #         j = j-1


    # sql = "SELECT STOCK_CODE, STOCK_NAME, STOCK_IDX FROM ADMIN.TB_STOCK_INFO"
    # cursor.execute(sql)
    # connection.commit()
    # daataa = cursor.fetchall()
    

cursorLoad()
# print("loding done")



# kospi, kosdaq = getStockCode()
# print(kospi['종목코드'][0])
# print(len(kospi))

# for i in kospi['종목코드']:
#     print(i)
# for j in kospi['종목코드']:
#     print(i)
