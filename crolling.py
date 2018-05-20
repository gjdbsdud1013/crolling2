import json
import os
import urllib.request
import requests
from bs4 import BeautifulSoup

url= requests.get('http://news.naver.com/main/ranking/popularDay.nhn?mid=etc')
html = url.text

soup = BeautifulSoup(html, "lxml")
link_list1 = soup.find_all('li', class_='num1')
link_list2 = soup.find_all('li', class_='num2')
link_list3 = soup.find_all('li', class_='num3')
link_list4 = soup.find_all('li', class_='num4')
link_list5 = soup.find_all('li', class_='num5')
count = 1

for list in link_list1[:6]: # lank1
    link="http://news.naver.com/"+list.find('a').get('href') #
    title=list.find('a').get('title')
    # print(link)
    # print(title)

    response = urllib.request.urlopen(link)

    soup = BeautifulSoup(response, "lxml")
    content = soup.select_one('#articleBodyContents')

    output = ""
    for item in content.contents:
        stripped = str(item).strip()
        if stripped == "":
            continue
        if stripped[0] not in ["<", "/"]:
            output += str(item).strip()
    output.replace("&apos;", "")
    article_text = output.replace("본문 내용TV플레이어", "")
    #
    # a = Article(link, language='ko')
    # article_text = article_parsing(a)
    f = open("C:\\Users\\Honeyoon\\PycharmProjects\\crolling2\\textfile\\lank1-{0}.txt".format(count), 'w', encoding='utf-8')
    f.write(article_text)
    f.close()

    if count == 1:
        politic_link1 = link
    elif count == 2:
        economy_link1 = link
    elif count == 3:
        social_link1 = link
    elif count == 4:
        culture_link1 = link
    elif count == 5:
        world_link1 = link
    elif count == 6:
        IT_link1 = link
    count=count+1
    response = urllib.request.urlopen(link)

count = 1

for list in link_list2[:6]: # lank2
    link="http://news.naver.com/"+list.find('a').get('href') #
    title=list.find('a').get('title')
    # print(link)
    # print(title)

    response = urllib.request.urlopen(link)

    soup = BeautifulSoup(response, "lxml")
    content = soup.select_one('#articleBodyContents')

    output = ""
    for item in content.contents:
        stripped = str(item).strip()
        if stripped == "":
            continue
        if stripped[0] not in ["<", "/"]:
            output += str(item).strip()
    output.replace("&apos;", "")
    article_text = output.replace("본문 내용TV플레이어", "")
    #
    # a = Article(link, language='ko')
    # article_text = article_parsing(a)
    f = open("C:\\Users\\Honeyoon\\PycharmProjects\\crolling2\\textfile\\lank2-{0}.txt".format(count), 'w', encoding='utf-8')
    f.write(article_text)
    f.close()

    if count == 1:
        politic_link2 = link
    elif count == 2:
        economy_link2 = link
    elif count == 3:
        social_link2 = link
    elif count == 4:
        culture_link2 = link
    elif count == 5:
        world_link2 = link
    elif count == 6:
        IT_link2 = link
    count=count+1
    response = urllib.request.urlopen(link)

count = 1

for list in link_list3[:6]:  # lank3
    link="http://news.naver.com/"+list.find('a').get('href') #
    title=list.find('a').get('title')
    # print(link)
    # print(title)

    response = urllib.request.urlopen(link)

    soup = BeautifulSoup(response, "lxml")
    content = soup.select_one('#articleBodyContents')

    output = ""
    for item in content.contents:
        stripped = str(item).strip()
        if stripped == "":
            continue
        if stripped[0] not in ["<", "/"]:
            output += str(item).strip()
    output.replace("&apos;", "")
    article_text = output.replace("본문 내용TV플레이어", "")
    #
    # a = Article(link, language='ko')
    # article_text = article_parsing(a)
    f = open("C:\\Users\\Honeyoon\\PycharmProjects\\crolling2\\textfile\\lank3-{0}.txt".format(count), 'w', encoding='utf-8')
    f.write(article_text)
    f.close()

    if count == 1:
        politic_link3 = link
    elif count == 2:
        economy_link3 = link
    elif count == 3:
        social_link3 = link
    elif count == 4:
        culture_link3 = link
    elif count == 5:
        world_link3 = link
    elif count == 6:
        IT_link3 = link
    count=count+1
    response = urllib.request.urlopen(link)

count = 1

for list in link_list4[:6]:  # lank4
    link="http://news.naver.com/"+list.find('a').get('href') #
    title=list.find('a').get('title')
    # print(link)
    # print(title)

    response = urllib.request.urlopen(link)

    soup = BeautifulSoup(response, "lxml")
    content = soup.select_one('#articleBodyContents')

    output = ""
    for item in content.contents:
        stripped = str(item).strip()
        if stripped == "":
            continue
        if stripped[0] not in ["<", "/"]:
            output += str(item).strip()
    output.replace("&apos;", "")
    article_text = output.replace("본문 내용TV플레이어", "")
    #
    # a = Article(link, language='ko')
    # article_text = article_parsing(a)
    f = open("C:\\Users\\Honeyoon\\PycharmProjects\\crolling2\\textfile\\lank4-{0}.txt".format(count), 'w', encoding='utf-8')
    f.write(article_text)
    f.close()

    if count == 1:
        politic_link4 = link
    elif count == 2:
        economy_link4 = link
    elif count == 3:
        social_link4 = link
    elif count == 4:
        culture_link4 = link
    elif count == 5:
        world_link4 = link
    elif count == 6:
        IT_link4 = link
    count=count+1
    response = urllib.request.urlopen(link)

count = 1

for list in link_list5[:6]:  # lank5
    link="http://news.naver.com/"+list.find('a').get('href') #
    title=list.find('a').get('title')
    # print(link)
    # print(title)

    response = urllib.request.urlopen(link)

    soup = BeautifulSoup(response, "lxml")
    content = soup.select_one('#articleBodyContents')

    output = ""
    for item in content.contents:
        stripped = str(item).strip()
        if stripped == "":
            continue
        if stripped[0] not in ["<", "/"]:
            output += str(item).strip()
    output.replace("&apos;", "")
    article_text = output.replace("본문 내용TV플레이어", "")
    #
    # a = Article(link, language='ko')
    # article_text = article_parsing(a)
    f = open("C:\\Users\\Honeyoon\\PycharmProjects\\crolling2\\textfile\\lank5-{0}.txt".format(count), 'w', encoding='utf-8')
    f.write(article_text)
    f.close()

    if count == 1:
        politic_link5 = link
    elif count == 2:
        economy_link5 = link
    elif count == 3:
        social_link5 = link
    elif count == 4:
        culture_link5 = link
    elif count == 5:
        world_link5 = link
    elif count == 6:
        IT_link5 = link
    count=count+1
    response = urllib.request.urlopen(link)
