# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
import time
from pytube import YouTube
import json

# 自動下載ChromeDriver
# s= ChromeService(r"./chromedriver.exe")

# 開啟瀏覽器
driver = webdriver.Chrome(r"C:\Users\91032\Desktop\TWsignTube\chromedriver.exe")
time.sleep(5)

# 想爬取的youtube
youtuber = ['@DeafNewsTV'
#,            '@hsiyunlin'
            ]

#準備容器
#name = []
#pageurl = []
videolink = {}
# 開始一個一個爬蟲
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
for yChannel in youtuber:

    # #--- 簡介 部分
    # driver.get('https://www.youtube.com/' + str(yChannel) + '/about')
    # time.sleep(1)

    # 基本資料
    #name.append(driver.find_element(by=By.ID, value='text-container').text) # 存youtuber頻道名
    #pageurl.append('https://www.youtube.com/' + str(yChannel)) # 存頻道網址

    #--- 影片 部分
    driver.get('https://www.youtube.com/' + str(yChannel) + '/videos')
    time.sleep(10)

    # 滾動頁面
    for scroll in range(1):#看要滑幾下
        driver.execute_script('window.scrollBy(0,1000)')#滑多少
        time.sleep(2)

    containar = [] # 結果整理成list
    for link in  driver.find_elements(by=By.ID, value='video-title-link'):
        h=link.get_attribute('href')
        n=link.get_attribute('title')
        containar.append({"name":n, "url":h,"cc":False})
    videolink[yChannel] = containar

driver.close()

outf = open(r'C:\Users\91032\Desktop\TWsignTube\test\links.json', 'w+', encoding='UTF-8')
json.dump(videolink, outf, ensure_ascii=False, indent=2)
outf.close()
