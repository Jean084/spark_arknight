# -*- coding: UTF-8 -*-
import urllib

from bs4 import BeautifulSoup
import re
import urllib2
import xlwt
import requests
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



findItem_active = re.compile(r'<tr>(.*?)</tr>')  # 创建正则表达式对象
findItem_active_unit = re.compile(r'<td.*?>(.*?)</td>')  # 创建正则表达式对象
findItem_active_title = re.compile(r'<a href=".*?" title="(.*?)">(.*?)</a>')  # 创建正则表达式对象
findItem_active_img = re.compile(r'<img alt="(.*?)" class="lazyload" data-src="(.*?)"')  # 创建正则表达式对象


def main():
    baseurl = "https://prts.wiki/w/%E6%B4%BB%E5%8A%A8%E4%B8%80%E8%A7%88"  #要爬取的网页链接
    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = "actives.xls"    #当前目录新建XLS，存储进去
    # 3.保存数据
    saveData(datalist,savepath)      #2种存储方式可以只选择一种


# 爬取网页
def getData(baseurl):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    datalist = []  #用来存储爬取的网页信息
    active_list=[]
    html = askURL(baseurl)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('table', class_="wikitable"):
        item = str(item).replace("\n", "")
        print item
        active_link = re.findall(findItem_active, item)
        count=0
        for item_act in active_link:
            item=str(item)
            if count==0:
                count+=1
                continue
            print(item_act)
            active_unit = re.findall(findItem_active_unit, item_act)
            print(active_unit[1])
            active_time = active_unit[0]
            print(active_time)
            active_title = re.findall(findItem_active_title, active_unit[1])[0]
            print(active_title[0])
            print(active_title[1])
            active_class = re.findall(findItem_active_title, active_unit[2])
            active_again=0
            active_class_str=""
            for one in range(len(active_class)):
                if active_class[one][0]=="分类:复刻活动":
                    active_again=1
                if one==0:
                    active_class_str+=active_class[one][0]
                    continue
                active_class_str+="_"+active_class[one][0]
            print(active_class_str)
            active_img = re.findall(findItem_active_img, item_act)[0]
            active_img_title=u"C:/Users/97227/Desktop/pip/wiki_ark/public/img/activities/" +active_title[1]+".jpg"
            active_img_url="https://prts.wiki/"+active_img[1]
            img_save = requests.get(active_img_url, headers=head).content
            with open(active_img_title, 'wb') as f:  # 把图片数据写入本地，wb表示二进制储存
                for chunk in img_save:
                    f.write(chunk)
            datalist.append([active_title[1], active_time, active_class_str,active_again, active_title[1]+".jpg"])
        conut=0
    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib2.Request(url, headers=head)
    html = ""
    try:
        response = urllib2.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib2.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据到表格
def saveData(datalist,savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('active', cell_overwrite_ok=True) #创建工作表
    col = ("name","time","class","again","img")
    for i in range(0,5):
        sheet.write(0,i,col[i])  #列名
    for i in range(len(datalist)):
        data = datalist[i]
        for j in range(0,5):
            sheet.write(i+1,j,data[j])  #数据
    book.save(savepath) #保存

# 保存数据到数据库

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()
    # init_db("movietest.db")
     print("爬取完毕！")