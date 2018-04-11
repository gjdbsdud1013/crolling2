import json
import os
import urllib.request
import requests
from bs4 import BeautifulSoup
from newspaper import Article


def article_parsing(a): # 뉴스 본문 읽어오기
    a.download()
    a.parse()
    print(a.text)
    return a.text

url= requests.get('http://news.naver.com/main/ranking/popularDay.nhn?mid=etc')
html = url.text

soup = BeautifulSoup(html, "lxml")
link_list = soup.find_all('li', class_='num1')
count = 1

for list in link_list[:6]:
    link="http://news.naver.com/"+list.find('a').get('href') #
    title=list.find('a').get('title')
    print(link)
    print(title)

    a = Article(link, language='ko')
    article_text = article_parsing(a)
    f = open("text{0}.txt".format(count), 'w', encoding='utf-8')
    f.write(article_text)
    f.close()
    count=count+1

