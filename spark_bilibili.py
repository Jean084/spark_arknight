import json
import time

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



findLink = re.compile(r'<.*?title="(.*?)".*?>')
findTitle = re.compile(r'<img alt="(.*?)" *')
findImg = re.compile(r'<a href="(.*?)">')

def main():
    # &otype=2&ps=20&direction=false&desc=false&sort_field=1&tid=0&with_current=false
    baseurl = "https://api.bilibili.com/x/v2/medialist/resource/list?mobi_app=web&type=1&biz_id=35997770&oid="
    datalist = getData(baseurl)
    saveData(datalist,"Finn.csv")
    # saveData2DB(datalist,dbpath)



def getData(baseurl):
    datalist = []
    vid=""
    for i in range(31):
        url = baseurl+str(vid)+"&otype=2&ps=20&direction=false&desc=false&sort_field=1&tid=0&with_current=false"
        html = askURL(url)
        time.sleep(0.1)
        soup = BeautifulSoup(html, "html.parser")
        print i
        json_data = json.loads(str(soup)).get("data","123")
        media_list=json_data.get("media_list","123")
        for media in media_list:
            title = media.get("title","123")
            vid = media.get("id","123")
            pages = media.get("pages", "123")
            for page in pages:
                page_title = page.get("title","123")
                datalist.append([title,page_title])
                print(page_title)
            print(vid)
            print(title)
    return datalist


def askURL(url):
    head = {
        'referer': 'https://www.bilibili.com/',

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }

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


def saveData(datalist,savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('Top250', cell_overwrite_ok=True)
    col = ("1","2")
    for i in range(0,len(col)):
        sheet.write(0,i,col[i])
    for i in range(0,len(datalist)):
        data = datalist[i]
        for j in range(0,len(col)):
            sheet.write(i+1,j,data[j])
    book.save(savepath)

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
#     conn = sqlite3.connect(dbpath)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     conn.close()


if __name__ == "__main__":
     main()
    # init_db("movietest.db")
     print("end")

