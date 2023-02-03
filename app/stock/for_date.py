from datetime import datetime
from dateutil.relativedelta import relativedelta

# 받은 시작달과 종료달기간을
# 월당 초일, 말일을 모두 리턴
# Stoct 데이터를 저장할 때 사용

# 시작일,종료일 설정
start = "20210801"
last = "20221127"


# 시작일, 종료일 datetime 으로 변환
startDate = datetime.strptime(start, "%Y%m%d")
lastDate = datetime.strptime(last, "%Y%m%d")

def getdate(startDate, lastDate):
    # 종료일 까지 반복
    while startDate <= lastDate:
        fDate = startDate = startDate.strftime("%Y%m%d")
        startDate = datetime.strptime(startDate, "%Y%m%d")

        startDate = startDate + relativedelta(months=1)
        nextDate = startDate + relativedelta(days=-1)
        
        nextDate = nextDate.strftime("%Y%m%d")

        print(fDate)
        print(nextDate)

if __name__ =="__main__":
    getdate(startDate, lastDate)