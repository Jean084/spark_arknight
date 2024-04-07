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

findItem_directory0 = re.compile(r'<li class="toclevel-1.*?"><a href=".*?"><span class="tocnumber">(.*?)</span> <span class="toctext">(.*?)</span></a>')
findItem_directory1 = re.compile(r'<li class="toclevel-2.*?"><a href=".*?"><span class="tocnumber">(.*?)</span> <span class="toctext">(.*?)</span></a>')
findItem_directory2 = re.compile(r'<li class="toclevel-3.*?"><a href=".*?"><span class="tocnumber">(.*?)</span> <span class="toctext"><b>(.*?)</b></span></a>')
findItem_history_large0 = re.compile(r'<table class="wikitable" style="width:.*?px">(.*?)</table>')
findItem_history_large1 = re.compile(r'<tr><th(.*?)>(.*?)</th>')
findItem_history_item_num = re.compile(r'rowspan="(.*?)"')
findItem_history_item_thing = re.compile(r'<td>(.*?)</td>')
findItem_history_large2 = re.compile(r'<h3><span id=".*?"></span><span class="mw-headline" id="(.*?)">(.*?)</span></h4>(.*?)<table class="wikitable" style=".*?">(.*?)</table>')
findItem_history_h4 = re.compile(r'<h4><span id=".*?"></span><span class="mw-headline" id="(.*?)">(.*?)</span></h4>(.*?</table>)')

findItem_thing_next_url = re.compile(r'<div style="display:block;position:absolute;right:12px;.*?><a href="(.*?)"')  # 创建正则表达式对象
findItem_thing_getitem = re.compile(r'<td.*?>(.*?)</td>')
findItem_thing_getimg = re.compile(r'<img alt=".*?" class="lazyload" data-src="(.*?)"/>')
findItem_thing_gettitle_large = re.compile(r'<span class="mw-headline" id=".">')
def main():
    baseurl = "https://prts.wiki/w/%E6%B3%B0%E6%8B%89%E5%B9%B4%E8%A1%A8"  #要爬取的网页链接
    # 1.爬取网页
    #baseurl = "https://prts.wiki//w/%E8%87%B3%E7%BA%AF%E6%BA%90%E7%9F%B3"
    datalist = getData(baseurl)
    savepath = "history.xls"    #当前目录新建XLS，存储进去
    # dbpath = "movie.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(datalist,savepath)      #2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)



# 爬取网页
def getData(baseurl):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    datalist0 = []  #用来存储爬取的网页信息
    datalist = []
    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    directory_list=[]
    conut=0
    time_list=[]
    for item in soup.find_all('li',class_="toclevel-1"):
        thing_item = re.findall(findItem_directory0, str(item))
        item_list1 = []
        for item1 in item.find_all('li', class_="toclevel-2"):
            thing_item_fist = re.findall(findItem_directory1, str(item1))
            item_list2=[]
            for item2 in item1.find_all('li', class_="toclevel-3"):
                thing_item_second = re.findall(findItem_directory2, str(item2))
                for time_data0 in thing_item_second:
                    item_list2.append(time_data0[1].replace(" ",""))
            for time_data1 in thing_item_fist:
                directory_list[conut].values().append({time_data1[1]:[]})
                item_list1.append({time_data1[1]:item_list2})
        for time_data in thing_item:
            directory_list.append({time_data[1]:item_list1})

    for directory0 in directory_list:
        time_str=directory0.keys()[0]
        if len(directory0.values()[0])==0:
            time_list.append(time_str)
        for directory1 in directory0.values()[0]:
            if len(directory1.values()[0])==0:
                time_list.append(time_str + "_"+directory1.keys()[0])
            for directory2 in directory1.values()[0]:
                time_list.append(time_str + "_"+directory1.keys()[0] + "_" + directory2)
    time_list=time_list[:-1]
    #for time in time_list:
    #    print(time)

    for item in soup.find_all('div', class_="mw-parser-output"):
        item=str(item)
        thing_item_fist = re.findall(findItem_history_large0, str(item).replace("\n", ""))
        conut=0
        for time_data in thing_item_fist:
            print(time_data)
            thing_item_title = re.findall(findItem_history_large1,time_data)
            now_time=time_list[conut]
            thing_list=[]
            conut+=1
            print(now_time)
            thing_item_thing = re.findall(findItem_history_item_thing, time_data)
            for time_data0 in thing_item_thing:
                thing=str(time_data0).split("<p>")[-1].split("</p>")
                thing[0] = thing[0].replace("<br/>","\n")
                if len(thing)==1:
                    thing.append("")
                else:
                    thing[1]=thing[1].split("<li>")[-1].split("</li>")[0]
                thing[1]=re.sub("<a.*?>|</a>", "",thing[1])
                print(thing[0])
                print(thing[1])
                thing_list.append(thing)
            time_num = 0
            for time_data0 in thing_item_title:
                thing_item_num = re.findall(findItem_history_item_num, time_data0[0])
                thing_item_num = 1 if(len(thing_item_num)==0) else int(thing_item_num[0])
                thing_item_time = re.sub(" |<p>|</p>|<br/>","",time_data0[1])
                for i in range(thing_item_num):
                    print(thing_item_time)
                    print(thing_item_num)
                    print(thing_list[i+time_num][0])
                    print(thing_list[i+time_num][1])
                    datalist.append([now_time,thing_item_time,thing_list[i+time_num][0],thing_list[i+time_num][1]])
                time_num+=thing_item_num
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
    col = ("largetime","time","thing","from")
    for i in range(0,len(col)):
        sheet.write(0,i,col[i])  #列名
    for i in range(len(datalist)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0,len(col)):
            sheet.write(i+1,j,data[j])  #数据
    book.save(savepath) #保存

# 保存数据到数据库

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()
    # init_db("movietest.db")
     print("爬取完毕！")