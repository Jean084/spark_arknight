# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import re
import urllib2
import xlwt
import requests
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



findLink = re.compile(r'<a class="image" href="(.*?)">')  # 创建正则表达式对象
findTitle = re.compile(r'<img alt="(.*?)" *')
findImg = re.compile(r'<a href="(.*?)">')

def main():
    baseurl = "https://prts.wiki/index.php?title=%E7%89%B9%E6%AE%8A:%E6%90%9C%E7%B4%A2&limit=20&offset="  #要爬取的网页链接
    # 1.爬取网页
    datalist = getData(baseurl)
    #savepath = "豆瓣电影Top250.xls"    #当前目录新建XLS，存储进去
    # dbpath = "movie.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    #saveData(datalist,savepath)      #2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)



# 爬取网页
def getData(baseurl):
    datalist = []  #用来存储爬取的网页信息
    for i in range(43, 101):  # 调用获取页面信息的函数，10次
        url = baseurl+str(i*20)+"&ns0=1&ns6=1&ns3000=1&search=%E7%AB%8B%E7%BB%98"
        html = askURL(url)  # 保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        print i
        for item in soup.find_all('table', class_="searchResultImage"):  # 查找符合要求的字符串
            data = []  # 保存一部电影所有信息
            item = str(item)
            img_link = "https://prts.wiki"+re.findall(findLink, item)[0]  # 通过正则表达式查找
            print img_link
            img_html = askURL(img_link)  # 保存获取到的网页源码
            # 2.逐一解析数据
            img_soup = BeautifulSoup(img_html, "html.parser")
            img = img_soup.find_all('div', class_="fullImageLink")[0]
            img = str(img)
            title = str(re.findall(findTitle, img)[0]).split("文件:")[-1].split("立绘 ")[-1]
            title_ = u"C:/Users/97227/Desktop/pip/wiki_ark/public/img/chara_all/"+title.replace(" ","_")
            print title_
            img_data = "https://prts.wiki"+re.findall(findImg, img)[0]
            head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
            }
            img_save = requests.get(img_data,headers=head).content
            with open(title_, 'wb') as f:  # 把图片数据写入本地，wb表示二进制储存
                for chunk in img_save:
                    f.write(chunk)
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
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True) #创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])  #列名
    for i in range(0,250):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])  #数据
    book.save(savepath) #保存

# def saveData2DB(datalist,dbpath):
#     init_db(dbpath)
#     conn = sqlite3.connect(dbpath)
#     cur = conn.cursor()
#     for data in datalist:
#             for index in range(len(data)):
#                 if index == 4 or index == 5:
#                     continue
#                 data[index] = '"'+data[index]+'"'
#             sql = '''
#                     insert into movie250(
#                     info_link,pic_link,cname,ename,score,rated,instroduction,info)
#                     values (%s)'''%",".join(data)
#             # print(sql)     #输出查询语句，用来测试
#             cur.execute(sql)
#             conn.commit()
#     cur.close
#     conn.close()


# def init_db(dbpath):
#     sql = '''
#         create table movie250(
#         id integer  primary  key autoincrement,
#         info_link text,
#         pic_link text,
#         cname varchar,
#         ename varchar ,
#         score numeric,
#         rated numeric,
#         instroduction text,
#         info text
#         )
#
#
#     '''  #创建数据表
#     conn = sqlite3.connect(dbpath)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     conn.close()

# 保存数据到数据库

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
     main()
    # init_db("movietest.db")
     print("爬取完毕！")