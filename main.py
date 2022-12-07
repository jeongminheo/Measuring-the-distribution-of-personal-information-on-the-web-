import requests
import re
import selenium
from konlpy.tag import Okt
from konlpy.corpus import kolaw
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
#수집및 동의 항목 추출
url = 'https://nid.naver.com/user2/V2Join?m=agree&lang=ko_KR&cpno='

req= requests.get(url)
data=list()
html= req.text
soup=BeautifulSoup(html, 'html.parser')
result01=soup.find('div', id='divPrivacy')
result01_01=result01.find_all('div', class_='article')
for result in result01_01:
    data.append(result.get_text())
 

value=data[0].replace('.','\n').split('\n')+data[1].replace('.','\n').split('\n')+data[2].replace('.','\n').split('\n')+data[3].replace('.','\n').split('\n')

li=[]
for word in value:
    if '필수항목' in word:
        li.append(word)
    elif '선택항목' in word:
        li.append(word)
for i in li:
    with open('C:\\Users\\gjwjd\\Measuring-the-distribution-of-personal-information-on-the-web-\\venv\\Lib\\site-packages\\konlpy/data/corpus/kolaw/list.txt','w',encoding='UTF-8') as txtfile:
        for i in li:
            txtfile.write(i)

okt=Okt()
doc_ko=kolaw.open('list.txt').read()
token_ko=okt.nouns(doc_ko)
del token_ko[0:5]
del token_ko[8:10]
del token_ko[11:]
token_ko.remove('번호')
print(token_ko)

#실제입력항목 추출
# 드라이버 위치 경로 입력
driver = webdriver.Chrome('C:\\Users\gjwjd\Downloads\chromedriver_win32/chromedriver.exe')
# url을 이용하여 브라우저로 접속
driver.get('https://nid.naver.com/user2/V2Join?m=agree&lang=ko_KR&cpno=')
driver.implicitly_wait(3)
# stay signed in 체크박스 채우기(클릭)
driver.find_element(By.XPATH,'//*[@id="join_form"]/div[1]/p/span/label').click()
# 확인버튼을 누르기
driver.find_element(By.XPATH,'/html/body/div/div[3]/div/div/div/form/div[2]/span[2]/a').click()
data2=list()
html= driver.page_source
soup= BeautifulSoup(html,'html.parser')
result01_02=soup.find_all('h3', class_='join_title')
for result in result01_02:
    data2.append(result.get_text())
for i in data2:
    with open('C:\\Users\\gjwjd\\Measuring-the-distribution-of-personal-information-on-the-web-\\venv\\Lib\\site-packages\\konlpy/data/corpus/kolaw/page.txt','w',encoding='UTF-8') as txtfile:
        for i in data2:
            txtfile.write(i)
driver.quit()
doc_ko2=kolaw.open('page.txt').read()
token_ko2=okt.nouns(doc_ko2)
del token_ko2[2:5]
del token_ko2[11:]
token_ko2.remove('선택')
print(token_ko2)
C = list(set(token_ko) - set(token_ko2))
if len(C)==0:
    print('SAME!!')
else:
    print('DIFFERENT!!')