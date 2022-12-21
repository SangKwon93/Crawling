import requests
from bs4 import BeautifulSoup
from scrapy.http import TextResponse
from fake_useragent import UserAgent
import csv
from functools import reduce
import json
import requests
import pandas as pd

URL='https://www.melon.com/chart/index.htm'
headers={
"User-Agent": UserAgent().chrome
}
res=requests.get(URL,headers=headers)
soup = BeautifulSoup(res.content,'html.parser')

lst50=soup.select('.lst50,.lst100')


melonList=[]
rank=[]
up_down=[]
title=[]
singer=[]
album=[]
code=[]
like=[]
query=[]
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
    # melonList.append(data) 
    # print(query)

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


from datetime import datetime
import time
from pytz import timezone
import os

# 리눅스 시 활용
def now_time():
    # 현재 시간 구하기
    now = datetime.now(timezone('Asia/Seoul'))  # 한국시간
    now_time = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "_" + str(now.hour) + "-" + \
        str(now.minute) + "-" + str(now.second)
    now_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return now_time


# 현재시간으로 파일 저장 시도
new_frame_time = datetime.now().strftime('%Y-%m-%d %H:%M')  # 2022-12-21 23:40
#print(new_frame_time)
filename=('melon chart{}'.format(new_frame_time))
# print(filename)

melon_list = pd.DataFrame(zip(rank,up_down,title,singer,album,code,like)
            ,columns=['rank','up_down','title','singer','album','code_num','likes'])

# csv 파일 저장
melon_list.to_csv('melon chart_2320.csv', index=False)    