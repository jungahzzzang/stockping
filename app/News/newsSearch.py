import os
import datetime
import urllib.request
import urllib.parse
import json
import cx_Oracle
import re
# from News.config import *

# CODE_1
def get_request_url(url):
    client_id="CD_wYAn2Fncz2V0cVhh0"
    client_secret="W_TLk3pV43"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    try:
        response = urllib.request.urlopen(request) # 정보 추출
        if response.getcode() == 200:              # OK(성공)
            print("[%s] Url Response Success" % datetime.datetime.now())
            response_body = response.read()
            news_list = response_body.decode('utf-8')   # 추출한 정보가 담겨져 있음
            print(news_list)
            return news_list
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None
    
# CODE_2 [뉴스 수집]
def getNaverSearchResult(sNode, search_text, page_start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % sNode

    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(search_text), page_start, display)

    url = base + node + parameters

    retData = get_request_url(url)

    if(retData == None):
        return None
    else:
        # print(retData)
        return json.loads(str(retData)) # JSON 형식으로 리턴

# CODE_3 [데이터 담기]
def getNewsData(item, jsonResult):
    title = item['title']
    originallink = item['originallink']
    link = item['link']
    description = item['description']
    pubDate = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pubDate = pubDate.strftime('%Y-%m-%d %H:%M:%S')
    title = title.replace("'", "")
    description = description.replace("'", "")
    
    jsonResult.append({'title': title, 'description': description,
                       'originallink': originallink, 'link': link,
                       'pubDate': pubDate})

# CODE_4 [오라클 연동]
def save_oracle(jsonResult):
    # Instant Client 경로 입력
    LOCATION = r"C:\\oracle\\instantclient_21_7"
    # 환경변수 등록
    os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]
    # 오라클 클라우드 DB 사용자 이름, 비밀번호, dsn 입력
    connection = cx_Oracle.connect(user='admin', password='Tmxhrvld1234!', dsn='stockping_high')
    # 커서 생성
    cursor = connection.cursor()
    # DB 저장
    sql = "insert into tb_news values (news_seq.nextval, :title, :originallink, :link, :description, :pubDate)"
    for rec in jsonResult:
        try:
            cursor.execute(sql, rec)
        except: # 데이터 중 encoding 오류 데이터는 제외하고 DB 저장
            print(rec)
            for reckey in rec:
                rec[reckey] = re.sub('[^가-힝0-9a-zA-Z<>&.?:/#\[\]\\s]', ' ', rec[reckey]) # []에 없는 문자를 제거, ^~ :~를 제외한 나머지
            cursor.execute(sql, rec)    # 수정된 데이터 DB 저장
            print(rec)
    connection.commit()

def main():
    jsonResult = []

    sNode = 'news'
    search_text = '주식'
    display_count = 100

    jsonSearch = getNaverSearchResult(sNode, search_text, 1, display_count)
    print("jsonSearch = ", jsonSearch)

    while((jsonSearch != None) and (jsonSearch['display'] != 0)):   # 추출한 데이터가 있을 때
        for item in jsonSearch['items']:
            print(item)
            getNewsData(item, jsonResult)

        nStart = jsonSearch['start'] + jsonSearch['display']
        jsonSearch = getNaverSearchResult(sNode, search_text, nStart, display_count)

    with open('%s naver_%s_DB.json' % (search_text, sNode), 'w', encoding='utf-8') as outfile:
        retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(retJson)

    print('%s_naver_%s.json SAVED' % (search_text, sNode))

    save_oracle(jsonResult)

# if __name__ == "__main__":
#     main()