## Melon Music crawling 

import math
import time
import datetime
start = time.time()
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
## for processing
from konlpy.tag import Hannanum
import re
import pandas as pd
import numpy as np
import csv
import sys
## visualization
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
from PIL import Image

## interactiveshell
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
#ignore warnings
import warnings
warnings.filterwarnings(action="ignore")

url = "https://www.melon.com/"
print("가수 이름을 입력하세요")
singer = str(input())


#수집할 정보 리스트 
titles =[]
infos =[]
lyricses=[]

def melon_crawling(url, singer):
    
    ##크롬 드라이버 호출
    driver = webdriver.Chrome()
    driver.get(url) 
    
    ##페이지 이동
    #검색창
    driver.find_element(By.XPATH,'//*[@id="top_search"]').click()
    #가수명 입력
    driver.find_element(By.XPATH,'//*[@id="top_search"]').send_keys(singer)
    #검색창 클릭
    driver.find_element(By.XPATH,'//*[@id="gnb"]/fieldset/button[2]').click() 
    #곡 선택
    driver.find_element(By.XPATH,'//*[@id="divCollection"]/ul/li[3]/a').click() 
    #아티스트명에서
    driver.find_element(By.XPATH,'//*[@id="conts"]/div[3]/div[1]/a[2]').click()
    driver.execute_script("window.scrollTo(0, 500)") 
    time.sleep(3) 
    
    # 곡정보 크롤링
    try:
        for page in range(1,6):
            for i in range(1, 51): #50개씩 있음
                #곡정보 칸으로 이동
                sing_css= f'#frm_defaultList > div > table > tbody > tr:nth-child({i}) > td:nth-child(3) > div > div > a.btn.btn_icon_detail'
                driver.find_element(By.CSS_SELECTOR,sing_css).click() 
                driver.execute_script("window.scrollTo(0, 500)") 
                time.sleep(3) 
                ##페이지 파싱 및 정보 수집
                html_source = driver.page_source 
                soup = BeautifulSoup(html_source, 'lxml')
                try:                     
                    title =driver.find_element(By.CSS_SELECTOR, "#downloadfrm > div > div > div.entry > div.info > div.song_name").text 
                    titles.append(title)
                    #세부 정보 
                    info  = driver.find_element(By.CSS_SELECTOR, "#downloadfrm > div > div > div.entry > div.meta").text
                    infos.append(info)
                    
                    #가사
                    lyrics =driver.find_element(By.CSS_SELECTOR, "#d_video_summary").text
                    lyricses.append(lyrics)
                    print(f'{i}번째 곡 크롤링 완료, 곡 제목:', title)
                except:
                    print("가사 정보가 없습니다.")
                    lyricses.append("unknown")
                    print(f'{i}번째 곡 크롤링 완료, 곡 제목:', title, "* 특이사항: 가사 없음")
                driver.back()
            print(f"{page}번째 페이지 크롤링 완료")
            print("====================")
            n= page+1
            print(f'{n}번째 페이지 크롤링 시작 ')
            last_page_height = driver.execute_script("return document.documentElement.scrollHeight") 
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") 
            driver.find_element(By.XPATH,  f'//*[@id="pageObjNavgation"]/div/span/a[{page}]').click()
            time.sleep(3)
    except:
        print("더 이상 수집할 수 있는 정보가 없습니다. ")
        pass
    
    driver.close()
    return titles, lyricses, infos


titles, lyricses, infos = melon_crawling(url, singer)

import pickle
print(len(titles), len(lyricses), len(infos))
with open("titles.pkl", 'wb') as f:
    pickle.dump(titles, f)
    
with open("lyricses.pkl", 'wb') as f:
    pickle.dump(lyricses, f)

with open("infos.pkl", 'wb') as f:
    pickle.dump(infos, f)

print("저장 완료")

#전처리
df= pd.DataFrame({"title": titles, 
              "lyrics":lyricses, 
              "information":infos})
album = []
date= []
genre =[]

for i in range(len(df)):
    album.append(df.information[i].split('\n')[1])
    date.append(df.information[i].split('\n')[3])
    genre.append(df.information[i].split('\n')[5])
df['album'] = album
df['date'] = date
df['genre'] = genre

df.drop(["information"], axis =1, inplace=True )

df.to_csv("Melon_Crawling.csv", index=False)

end = time.time()
sec = (end - start)
result = datetime.timedelta(seconds=sec)
result_list = str(datetime.timedelta(seconds=sec)).split(".")
print("총 수행시간 :", result_list[0])



