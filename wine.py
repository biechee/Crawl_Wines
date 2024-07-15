# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import csv

wines = []
c = [0, 0, 0, 0, 0, 0]


def wineurl(url, a, b):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('網頁錯誤:', url)
    # 將網頁資料交給beautifulsoup+html5lib解析
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 因為此網頁只有分業沒有下一頁按鈕，所以將處理分業按鈕
    if a > 10:
        a = 1
    try:
        paging = soup.find('div', 'page_toolbar').find('a')['href'][:-1]
    # 到最後一頁結束程式
    except TypeError:
        print('已爬取完畢')
        return

    rents = soup.find_all('div', 'recipe_list_content')
    for rent in rents:
        wine = []
        # 名稱
        name = rent.find('div', 'recipe_list_content_name').text.strip()
        wine.append(name)

        # 成分  .replace(u'\xa0',' ')去除&nbsp不間斷空格
        ingred = rent.find('div', 'recipe_list_content_ingred').text.replace('\n', '').replace(u'\xa0', ' ')
        wine.append(ingred)

        # 介紹
        intro = rent.find('div', 'recipe_list_content_intro').span.text
        if intro:
            wine.append(intro.strip())
        else:
            wine.append('無')

        # 篩選
        if b in ingred:
            wines.append(wine)
            print('酒品:' + wine[0] + '\n成分:' + wine[1] + '\n介紹:' + wine[2])
            print()

        # 判斷
        if '威士忌' in ingred:
            c[0] = c[0] + 1
        if '琴酒' in ingred:
            c[1] = c[1] + 1
        if '龍舌蘭' in ingred:
            c[2] = c[2] + 1
        if '蘭姆酒' in ingred:
            c[3] = c[3] + 1
        if '白蘭地' in ingred:
            c[4] = c[4] + 1
        if '伏特加' in ingred:
            c[5] = c[5] + 1

    # 將檔案存進CSV
    with open('wine.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 設定標題
        writer.writerow(('酒品', '成分', '介紹'))
        for item in wines:
            writer.writerow(item)

    # 爬取下一頁內容
    a = a + 1
    wineurl('https://mixology.com.tw' + paging + str(a), a, b)


print('請輸入您的調酒想要的成分來搜尋(若是全部的調酒請直接Enter):')
b = input()

wineurl('https://mixology.com.tw/Recipe.aspx', 1, b)

# 資料分析
print('\n此網站調酒分類(圓餅圖顯示)')
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Whisky', 'Gin', 'Tequila', 'Rum', 'Brandy', 'Vodka'
sizes = [c[0], c[1], c[2], c[3], c[4], c[5]]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
