import pandas as pd
import cx_Oracle
import json


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
    
    with open('config.json', 'r') as f: #Instant Client 접속을 위한 전자지갑속 오라클 클라우드DB 정보(tnsnames.ora 파일)
        config = json.load(f)
    db_info = config['DB']

    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_19_16") # 설치한 Instant Client 경로
    connection = cx_Oracle.connect(user=db_info['username'], password=db_info['password'], dsn=db_info['dsn'])
    cursor = connection.cursor()

    kospi, kosdaq = getStockCode()
    # print(len(kospi))
    # cursor.execute(sql)
    # connection.commit()

    # sql = "ALTER SEQUENCE ADMIN.STOCK_SEQ INCREMENT BY 1 MINVALUE 1 MAXVALUE 9999 NOCYCLE NOCACHE NOORDER"
    # cursor.execute(sql)
    # connection.commit()



    for i in range(0,len(kospi),1):
        try:
            sql = f"INSERT INTO ADMIN.TB_STOCK_INFO (STOCK_CODE, STOCK_NAME, STOCK_IDX) VALUES('{kospi['종목코드'][i]}', '{kospi['회사명'][i]}', STOCK_SEQ.NEXTVAL)"
            cursor.execute(sql)
            connection.commit()

        except:
            print(i," 번째 오류, 다시시도")
            i = i-1

    for j in range(0,len(kosdaq),1):
        try:
            sql = f"INSERT INTO ADMIN.TB_STOCK_INFO (STOCK_CODE, STOCK_NAME, STOCK_IDX) VALUES('{kosdaq['종목코드'][j]}', '{kosdaq['회사명'][j]}', STOCK_SEQ.NEXTVAL)"
            cursor.execute(sql)
            connection.commit()

        except:
            print(j," 번째 오류, 다시시도")
            j = j-1


    # sql = "SELECT STOCK_CODE, STOCK_NAME, STOCK_IDX FROM ADMIN.TB_STOCK_INFO"
    # cursor.execute(sql)
    # connection.commit()
    # daataa = cursor.fetchall()
    

cursorLoad()
print("done")



# kospi, kosdaq = getStockCode()
# print(kospi['종목코드'][0])
# print(len(kospi))

# for i in kospi['종목코드']:
#     print(i)
# for j in kospi['종목코드']:
#     print(i)
