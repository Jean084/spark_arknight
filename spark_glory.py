# -*- coding: UTF-8 -*-
import urllib

from bs4 import BeautifulSoup
import re
import urllib2
import xlwt
import requests
import sqlite3
import time
import sys
import json
reload(sys)
import execjs
sys.setdefaultencoding('utf-8')


def main():
    baseurl0 = "https://prts.wiki/index.php?title=%E5%85%89%E8%8D%A3%E4%B9%8B%E8%B7%AF%2Fdata&action=raw"
    baseurl1 = ""
    #baseurl = "https://prts.wiki/index.php?title=%E5%85%89%E8%8D%A3%E4%B9%8B%E8%B7%AF&amp;action=history"  #要爬取的网页链接
    # 1.爬取网页
    time.sleep(1)
    #baseurl = "https://prts.wiki//w/%E8%87%B3%E7%BA%AF%E6%BA%90%E7%9F%B3"
    datalist,datalist0,datalist1 = getData(baseurl0)
    savepath = "glory.xls"    #当前目录新建XLS，存储进去
    # dbpath = "movie.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(datalist,datalist0,datalist1,savepath)      #2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)



# 爬取网页
def getData(baseurl):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Cookie":"Hm_lvt_e1369c7d981281aa581e68b669c5a75c=1709775888,1709856585,1710115571,1710208507; _gid=GA1.2.1238155790.1710208507; _gat_gtag_UA_158174062_1=1; _ga_DEE6E93G5M=GS1.1.1710211398.49.1.1710213552.56.0.0; Hm_lpvt_e1369c7d981281aa581e68b669c5a75c=1710213553; _ga=GA1.2.1376524672.1706168074"
    }
    datalist = []
    node = execjs.get()
    response = requests.get("https://prts.wiki/index.php?title=%E5%85%89%E8%8D%A3%E4%B9%8B%E8%B7%AF%2Fdata&action=raw", headers=head)
    str_json = response.text
    #print(str_json)
    datalist0=[]
    datalist1 = []
    json_obj = json.loads(str_json.decode('utf-8'))
    print(json_obj["category"].keys())
    category_list = json_obj["category"]
    medal_list = json_obj["medal"]
    medal_Group_list = json_obj["medalGroup"]
    for medal_Group_one in medal_Group_list.values():
        datalist1.append([medal_Group_one["name"],medal_Group_one["desc"],medal_Group_one["id"]])
        ulr = "https://torappu.prts.wiki/assets/medal_diy/" + medal_Group_one["id"]+".png"
        img_save = requests.get(ulr, headers=head).content
        with open("C:/Users/97227/Desktop/pip/wiki_ark/public/img/glory/"+medal_Group_one["id"]+".png", 'wb') as f:  # 把图片数据写入本地，wb表示二进制储存
            for chunk in img_save:
                f.write(chunk)
    for category_one in category_list.values():
        datalist0.append([category_one["name"],category_one["desc"]])
        for medal_id in category_one["medal"]:
            medal_one = medal_list[medal_id]
            ulr = "https://torappu.prts.wiki/assets/medal_icon/"+medal_id+".png"
            img_save = requests.get(ulr, headers=head).content
            with open("C:/Users/97227/Desktop/pip/wiki_ark/public/img/glory/"+medal_id + ".png", 'wb') as f:  # 把图片数据写入本地，wb表示二进制储存
                for chunk in img_save:
                    f.write(chunk)
            datalist.append([medal_one["name"],category_one["name"],medal_one["desc"],medal_one["method"],medal_one["isHidden"],medal_one["isTrim"],medal_id,False,"-"])
        for medal_Group_id in category_one["medalGroup"]:
            medal_Group = medal_Group_list[medal_Group_id]
            for medal_id in medal_Group["medal"]:
                medal_one = medal_list[medal_id]
                ulr = "https://torappu.prts.wiki/assets/medal_icon/" + medal_id + ".png"
                img_save = requests.get(ulr, headers=head).content
                with open("C:/Users/97227/Desktop/pip/wiki_ark/public/img/glory/"+medal_id + ".png", 'wb') as f:  # 把图片数据写入本地，wb表示二进制储存
                    for chunk in img_save:
                        f.write(chunk)
                datalist.append([medal_one["name"],category_one["name"],medal_one["desc"],medal_one["method"],medal_one["isHidden"],medal_one["isTrim"],medal_id,True,medal_Group["name"]])
    return datalist,datalist0,datalist1


# 得到指定一个URL的网页内容
def askURL(url):
    head = {
        # 模拟浏览器头部信息，向豆瓣服务器发送消息"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46",
        "Cookie": "Hm_lvt_e1369c7d981281aa581e68b669c5a75c=1710125566; _gid=GA1.2.1388073617.1710125567; _ga_DEE6E93G5M=GS1.1.1710143170.27.1.1710146957.60.0.0; Hm_lpvt_e1369c7d981281aa581e68b669c5a75c=1710146958; _ga=GA1.2.1762207248.1704176507"
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
def saveData(datalist,datalist0,datalist1,savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet_group = book.add_sheet('group', cell_overwrite_ok=True) #创建工作表
    sheet_one = book.add_sheet('one', cell_overwrite_ok=True) #创建工作表
    sheet_class = book.add_sheet('class', cell_overwrite_ok=True) #创建工作表
    col_one = ("name","class","desc","method","isHidden","isTrim","medal_id","Group","group_name")
    col_class = ("name","desc")
    col_group = ("name","desc","img")
    for i in range(0,len(col_group)):
        sheet_group.write(0,i,col_group[i])  #列名
    for i in range(len(datalist1)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist1[i]
        for j in range(0,len(col_group)):
            sheet_group.write(i+1,j,data[j])  #数据
    for i in range(0,len(col_class)):
        sheet_class.write(0,i,col_class[i])  #列名
    for i in range(len(datalist0)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist0[i]
        for j in range(0,len(col_class)):
            sheet_class.write(i+1,j,data[j])  #数据
    for i in range(0,len(col_one)):
        sheet_one.write(0,i,col_one[i])  #列名
    for i in range(len(datalist)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0,len(col_one)):
            sheet_one.write(i+1,j,data[j])  #数据
    book.save(savepath) #保存

# 保存数据到数据库

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()
    # init_db("movietest.db")
     print("爬取完毕！")