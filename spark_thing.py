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



findItem_thing_class = re.compile(r'<div class="smwdata" data-category="(.*?)" data-description=.*? data-file="(.*?)" data-id=".*?" data-name="(.*?)" data-obtain_approach="(.*?)" data-rarity=".*?" data-usage=.*?>')  # 创建正则表达式对象
findItem_thing_next_url = re.compile(r'<div style="display:block;position:absolute;right:12px;.*?><a href="(.*?)"')  # 创建正则表达式对象
findItem_thing_getitem = re.compile(r'<td.*?>(.*?)</td>')
findItem_thing_getimg = re.compile(r'<img alt=".*?" class="lazyload" data-src="(.*?)"/>')
def main():
    baseurl = "https://prts.wiki/w/%E5%BD%BC%E5%BE%97%E6%B5%B7%E5%A7%86%E7%83%AD%E9%94%80%E9%A5%BC%E5%B9%B2"  #要爬取的网页链接
    # 1.爬取网页
    #baseurl = "https://prts.wiki//w/%E8%87%B3%E7%BA%AF%E6%BA%90%E7%9F%B3"
    datalist = getData(baseurl)
    savepath = "thing.xls"    #当前目录新建XLS，存储进去
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
    url_first="https://prts.wiki/index.php?title=%E9%81%93%E5%85%B7%E4%B8%80%E8%A7%88&filter=A%2C%2C%2CwBA"
    html_first = askURL(url_first)
    soup_first = BeautifulSoup(html_first, "html.parser")
    for item in soup_first.find_all('div', class_="smwdata"):
        item=str(item)
        thing_item_fist = re.findall(findItem_thing_class, item)[0]
        url_thing="https://prts.wiki/w/"+str(thing_item_fist[1]).split("_")[-1][:-4]
        html = askURL(url_thing)
        soup = BeautifulSoup(html, "html.parser")
        #for item in soup.find_all('div', class_="tl-idnav"):
        #    item = str(item)
        #    baseurl = "https://prts.wiki/"+re.findall(findItem_thing_next_url, item)[0]
        #    print (baseurl)
        for item in soup.find_all('table', class_="itemInfo"):
            item = str(item).replace("\n", "")
            print(item)
            thing_item = re.findall(findItem_thing_getitem, item)
            #for item0 in thing_item:
            #    print(item0)
            thing_name=thing_item_fist[2]
            thing_url=str(re.findall(findItem_thing_getimg, thing_item[2])[0]).split('"')[0]
            if thing_url[0:7]=="/images":
                thing_url="https://prts.wiki"+thing_url
            else:
                thing_url="https:"+thing_url
            thing_class = str(thing_item_fist[0]).replace("分类:","").replace(", ",'_')
            thing_use = thing_item[3]
            thing_introduce=str(thing_item[4]).replace('<p>','\n')
            thing_introduce = thing_introduce.replace('</p>', '')
            thing_get=thing_item_fist[3]
            print("thing_name:"+thing_name)
            print("thing_url:"+thing_url)
            print("thing_class:"+thing_class)
            print("thing_use:"+thing_use)
            print("thing_introduce:"+thing_introduce)
            print("thing_get:"+thing_get)
            img_title = thing_url.split("/")[-1]
            print("thing_title:"+img_title)
            thing_title = u"C:/Users/97227/Desktop/pip/wiki_ark/public/img/thing/" + img_title
            thing_save = requests.get(thing_url, headers=head).content
            with open(thing_title, 'wb') as f:  # 把图片数据写入本地，wb表示二进制储存
                for chunk in thing_save:
                    f.write(chunk)
            datalist.append([thing_name,thing_class,thing_use,thing_introduce,thing_get,img_title])
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
    col = ("name","class","use","introduce","get","img")
    for i in range(0,6):
        sheet.write(0,i,col[i])  #列名
    for i in range(len(datalist)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0,6):
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