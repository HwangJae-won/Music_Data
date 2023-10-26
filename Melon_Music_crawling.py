## Melon Music crawling 
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
singer = str(input())

#수집할 정보 리스트 
titles =[]
infos =[]
lyricses=[]

def melon_crawling(url, singer):
    
    ##크롬 드라이버 호출
    driver = webdriver.Chrome('/Users/hwangjaewon/Desktop/chromedriver')
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
    #아티스트명 클릭: 정확도 향상
    driver.find_element(By.XPATH,'//*[@id="conts"]/div[3]/div[1]/a[2]').click()
    driver.execute_script("window.scrollTo(0, 500)") 
    time.sleep(3) 
    
    # 곡정보 크롤링
    for page in range(2,6):
        for i in range(29, 51): #50개씩 있음
            #곡정보 칸으로 이동
            sing_css= f'#frm_defaultList > div > table > tbody > tr:nth-child({i}) > td:nth-child(3) > div > div > a.btn.btn_icon_detail'
            print(sing_css)
            driver.find_element(By.CSS_SELECTOR,sing_css).click() 
            driver.execute_script("window.scrollTo(0, 500)") 
            time.sleep(3) 
            ##페이지 파싱 및 정보 수집
            html_source = driver.page_source 
            soup = BeautifulSoup(html_source, 'lxml')
            try: 
                #타이틀명 선택
                title =driver.find_element(By.CSS_SELECTOR, "#downloadfrm > div > div > div.entry > div.info > div.song_name").text 
                titles.append(title)
                #가사
                lyrics =driver.find_element(By.CSS_SELECTOR, "#d_video_summary").text
                lyricses.append(lyrics)
                #세부 정보 
                info  = driver.find_element(By.CSS_SELECTOR, "#downloadfrm > div > div > div.entry > div.meta").text
                infos.append(info)
                
                print(f'{i}번째 곡 크롤링 완료, 곡 제목:', title)
            except:
                print("가사 정보가 없습니다.")
                lyricses.append("unknown")
                print(f'{i}번째 곡 크롤링 완료, 곡 제목:', title, "* 특이사항: 가사 없음")
            
            driver.back()
            driver.execute_script("window.scrollTo(0, 200)") 
        print("====================")
        print("한 페이지 크롤링 완료")
        driver.find_element(By.XPATH, f'//*[@id="pageObjNavgation"]/div/span/a[{page}]')
    driver.close()
    
melon_crawling(url, singer)

df= pd.DataFrame({"title": titles, 
              "lyrics":lyricses, 
              "information":infos})

df.to_csv("Melon_Crawling.csv", index=False)

