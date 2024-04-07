import requests
import json
import re
import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


findImg = re.compile(r'<a href="//(.*?)".*?title="(.*?)" class="title">(.*?)</a>')

driver=webdriver.Chrome(executable_path='C:/Program Files/Google/Chrome/Application/chromedriver')
# driver.maximize_window()
# driver.minimize_window()
driver.implicitly_wait(5)
data_list=[]
for i in range(7):
    url="https://space.bilibili.com/696719724/video?tid=0&pn="+str(i+2)+"&keyword=&order=pubdate"
    driver.get(url)
    driver.implicitly_wait(5)
    element=driver.find_elements(By.XPATH,'//li[@class="small-item fakeDanmu-item"]/a[@class="title"]')
    driver.set_window_size(100,100)
    title_list=[]
    href_list=[]
    for elem in element:
        title = elem.get_attribute('title')
        title_list.append(title)
        href = elem.get_attribute('href')
        href_list.append(href)
    for i in range(len(title_list)):
        data_list_one=[]
        title = title_list[i]
        href = href_list[i]
        data_list_one.append(title)
        print(title)
        print(href)
        driver.get(href)
        driver.implicitly_wait(15)
        elements = driver.find_elements(By.XPATH, '//ul[@class="list-box"]/li/a/div/div/span[@class="part"]')
        # print(driver.page_source)
        for elems in elements:
            # elems.get_attribute("title")
            # list0 = elems.find_element(By.XPATH,"a")
            name = elems.get_attribute('outerHTML')
            song_name=name.split("</")[0].split(">")[-1]
            song_name = str(song_name).replace("-","|").replace("&amp;","")
            print(song_name)
            data_list_one.append(song_name)
        data_list.append(data_list_one)
    driver.quit()
with open("savepath.csv", 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data_list)