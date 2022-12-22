import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv
from functools import reduce
import json
import requests
import pandas as pd
import datetime
import pytz # 없는 사람은 pip install pytz # 서울시간
import time
import random
import json

# 리눅스 환경에서 한국 시간 설정
def get_seoul_date():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    kst_now = utc_now.astimezone(pytz.timezone("Asia/Seoul"))
    da = kst_now.strftime("%m/%d/%Y")
    ti = kst_now.strftime("%H:%M:%S")
    return da, ti

melonList=[]
rank=[]
up_down=[]
title=[]
singer=[]
album=[]
code=[]
like=[]
query=[]

# 실시간 top 100 가져오기 반복
while True:
    # def generate_payment_date(start,end):
    URL='https://www.melon.com/chart/index.htm'
    headers={
    "User-Agent": UserAgent().chrome
    }
    res=requests.get(URL,headers=headers)
    soup = BeautifulSoup(res.content,'html.parser')

    lst50=soup.select('.lst50,.lst100')



    for i in lst50:
        data=[]
        code_number=[]
        # 1. 순위
        rank.append(i.select_one('.rank').text)

        num =i.select_one('span.rank_wrap').text.strip().split('\n')
        stage =i.select_one('span.rank_wrap').text.strip().split('\n')

        if '순위 동일' in stage:
            stage=''
        elif '단계 상승' in stage:
            stage='+'
        elif '단계 하락' in stage:
            stage="-"
        elif '순위 진입' in stage:
            stage=''

        if len(num)==1:
            num.append('0')

        rank_up= str(stage)+str(num[1])
        #2. 순위 오르락 내리락
        up_down.append(rank_up)
        #3. 노래제목
        title.append(i.select_one('.ellipsis.rank01').a.text)
        #4. 가수
        singer.append(i.select_one('.ellipsis.rank02').a.text)
        #5. 앨범
        album.append(i.select_one('.ellipsis.rank03').a.text)
        # code=i.select_one('div.wrap > a')['href']

        #6. 노래 제목코드
        code_number.append(i.select_one('.wrap.t_right > input')["value"]) 
        query.append(code_number)
        query_sum=sum(query,[])
        code.append(i.select_one('.wrap.t_right > input')["value"])
      

    # query_keys = sorted(list(melonList.keys()))
    API_URL = f"https://www.melon.com/commonlike/getSongLike.json?contsIds={','.join(query_sum)}"
    #print(API_URL)
    headers = {
    "content-type": "application/json;charset=UTF-8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    response = requests.get(
    API_URL,
    headers=headers
    )
    likes = response.json()['contsLike']

    for k in likes:
        cnt=(k["SUMMCNT"])
        like.append(cnt)

        
    pairs=list(zip(rank,up_down,title,singer,album,code,like))
    # print(pairs)
    def table_result():
        for i in range(0,100):
            conn=[]
            da,ti=get_seoul_date()
            for j in pairs:
                new_data = {
                    "DATE":da,
                    "TIME":ti,
                    "RANK" : rank[i],
                    "UP_DOWN" : up_down[i],
                    'TITLE' : title[i],
                    'SINGER':singer[i],
                    'ALBUM':album[i],
                    "LIKE":like[i]
                }
                conn.append(new_data)
        return conn

    print(table_result())


# 한세트씩 인덱스에 따라 나왔지만 dict 형태 전환 실패

# while True:
   
#     rank[0:100],up_down[0:100],title[0:100],singer[0:100],album[0:100],like[0:100] = generate_payment_date(1,100)

#     # 프로듀서가 스트리밍할 데이터 조립(json으로)
#     new_data = {
#         "RANK" : rank[0:100],
#         "UP_DOWN" : up_down[0:100],
#         'TITLE' : title[0:100],
#         'SINGER':singer[0:100],
#         'ALBUM':album[0:100],
#         "like":like[0:100]
#     }


