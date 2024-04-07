# -*- coding: UTF-8 -*-
import urllib
import csv
from bs4 import BeautifulSoup
import re
import urllib2
import xlwt
import requests
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

findLink_class_0 = re.compile(r'<a class="mw-selflink selflink">(.*?)</a>')  # 创建正则表达式对象
findLink_class_1 = re.compile(
    r'<tr><th class="navbox-group" scope="row">(.*?)</th>.*?<tbody><tr><th class="navbox-group" scope="row">(.*?)</th>(.*?)</tr>')
findLink_drama_url = re.compile(r'<a href="(.*?)" title="(.*?)">(.*?)</a>')  # 创建正则表达式对象
findLink_drama_content = re.compile(r'<ul class="log_style" id="playback_all_result">(.*?)</ul>')  # 创建正则表达式对象
findLink_drama_delong = re.compile(
    r'<div class="common_style playback_common hidden" id="sys_playback_all">(.*?)</div>')
findLink_drama_content_name = re.compile(r'.*?=.*?"(.*?)"')  # 创建正则表达式对象
findLink_drama_content_focus = re.compile(r'.*?=(.*?)\)]')  # 创建正则表达式对象
findLink_drama_content_img = re.compile(r'image="(.*?)"')  # 创建正则表达式对象
findLink_drama_content_ref = re.compile(r'.*?="(.*?)"')  # 创建正则表达式对象

findName_board = re.compile(r'<div class="brandtitle">(.*?)')  # 创建正则表达式对象
findLogo_board = re.compile(r'<div class="brand-content-logo">(.*?)')  # 创建正则表达式对象
findText_board = re.compile(r'<div class="brand-content-text">(.*?)</div>')  # 创建正则表达式对象
findTitle = re.compile(r'<img alt="(.*?)" *')
findImg = re.compile(r'<img height="100%" src="(.*?)"')
findImg0 = re.compile(r'<img src="(.*?)"')
findName_cloth = re.compile(r'<th colspan="5" style="position:relative;">(.*?)<')
findName_else0_cloth = re.compile(r'Animated</span></span> </span>(.*?)</th></tr>')
findName_else1_cloth = re.compile(r'</span></span></span>(.*?)<span class="mc-tooltips">')
findIntroduce0_cloth = re.compile(r'<p style="margin:5px; margin-bottom:10px;">(.*?)</p>')
findIntroduce1_cloth = re.compile(r'<p style="margin:5px;"><i>(.*?)</i></p>')
findArtiest_cloth = re.compile(r'<td width="105px">(.*?)</td>')
findget_cloth = re.compile(r'<td width="105px"><a href=".*" title="(.*?)">(.*?)')
findcost_cloth = re.compile(
    r'<div style="display:inline-block;line-height:24px;vertical-align:top;font-weight:bold;font-size:15px;color:white;padding-left:28px;">(.*?)</div>')
findbelong_cloth = re.compile(r'<td colspan="3">(.*?)')
findtime_cloth = re.compile(r'</th><td colspan="3">(.*?) ~ <br/>')
findtext_cloth = re.compile(r'<td colspan="4" style="text-align:left; height:(.*);"><p>(.*?)</p>')
findimg_cloth = re.compile(r'<img alt="(.*?)"')

def replace_str(original, replacements):
    for old, new in replacements.items():
        original = original.replace(old, new)
    return original

def main():
    baseurl = "https://prts.wiki/w/%E5%89%A7%E6%83%85%E4%B8%80%E8%A7%88"  # 要爬取的网页链接
    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = "drama.csv"  # 当前目录新建XLS，存储进去
    # dbpath = "movie.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(datalist, savepath)  # 2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)


# 爬取网页
def getData(baseurl):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    datalist0 = []  # 用来存储爬取的网页信息
    datalist0.append(["name", "class", "filename", "desc", "category"])
    html = askURL(baseurl)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('table', class_="navbox"):
        item = str(item)
        drama_category0 = re.findall(findLink_class_0, item)[0]
        drama_class1 = re.findall(findLink_class_1, item)
        for class1 in drama_class1:
            drama_category1 = class1[0]
            drama_class = class1[1]
            print(drama_category0+" "+drama_category1+" "+drama_class)
            # if drama_category0=="主线剧情一览":
            #     continue
            drama_urls = re.findall(findLink_drama_url, str(item))
            num=0
            for drama_one in drama_urls:
                num+=1
                print(num)
                # if num<780:
                #     continue
                drama_url = "https://prts.wiki" + drama_one[0]
                title_csv = "daram/" + drama_one[1].replace("/","_").replace("?","？").replace(".","").replace(":","_") + ".csv".decode("utf-8")
                name = drama_one[2]
                datalist0.append([name, drama_class, title_csv, drama_category1, drama_category0])
                drama_html = askURL(drama_url)
                drama_soup = BeautifulSoup(drama_html, "html.parser")
                #"Predicate", "Blocker", "ImageTween","CameraShake", "CameraShake", "CameraEffect", "StartBattle", "Tutorial","Subtitle","Background", "Image",
                str_map = {
                    "delay": "Delay",
                    "stopmusic": "StopMusic",
                    "playsound": "PlaySound",
                    "character":"Character",
                    "playMusic":"PlayMusic",

                }
                for item in drama_soup.find_all('script', id='datas_txt'):
                    # print(item)
                    datalist=[]
                    datalist.append(["id", "class", "name", "content"])
                    count = 0
                    sys.stdout.write(str(count))
                    for row in str(item).split("\n"):
                        if row=="":
                            continue
                        # print(row)
                        class0 = row.split("[",1)[-1].split("(",1)
                        if len(class0[0])<1:
                            class0[0]=class0[1]
                        class0[0] = replace_str(class0[0], str_map)
                        if (class0[0] in ["HEADER"]):
                            continue
                        elif class0[0][:4] == "name":
                            drama_content_class = "Dialog"
                            class0[0] = class0[0].replace("'", '"')
                            # print(re.findall(findLink_drama_content_name, class0[0]))
                            drama_content_name = re.findall(findLink_drama_content_name, class0[0])[0]

                            drama_content_text = class0[0].split("  ")[-1].split("]")[-1]
                            # print(drama_content_class + " " + drama_content_name + " " + drama_content_text)
                        elif class0[0] in ["Predicate", "PlayMusic", "Blocker", "ImageTween", "StopMusic",
                                           "CameraShake", "CameraEffect", "StartBattle", "Tutorial",
                                           "Subtitle","Background", "Image", "Dialog","Character", "Delay", "PlaySound"]:
                            drama_content_class = class0[0]
                            drama_content_name_list = re.findall(findLink_drama_content_name, class0[1])
                            drama_content_name = drama_content_name_list[0] if len(
                                drama_content_name_list) > 0 else ""
                            drama_content_text = class0[1].split(")")[0]
                            # print(drama_content_class + " " + drama_content_name + " " + drama_content_text)
                        elif class0[0][-1]=="]" or class0[0][-1]==">":
                            drama_content_class = class0[0].split("]")[0]
                            drama_content_name_list = re.findall(findLink_drama_content_name, class0[0])
                            drama_content_name = drama_content_name_list[0] if len(
                                drama_content_name_list) == 1 else "end"
                            drama_content_text = ""
                            # print(drama_content_class + " " + drama_content_name + " " + drama_content_text)
                        elif class0[0] == "Decision":
                            dec = class0[1].split('"')
                            drama_content_class = class0[0]
                            drama_content_name = dec[1]
                            drama_content_text = dec[3]
                            # print(drama_content_class + " " + drama_content_name + " " + drama_content_text)
                        elif class0[0] in ["Characteraction","stopSound","charslot"]:
                            drama_content_class = class0[0]
                            drama_content_name = ""
                            drama_content_text = ""
                        else:
                            # for class_one in class0:
                            #     print(class_one)
                            drama_content_class = "Text"
                            drama_content_name = ""
                            drama_content_text = class0[0]
                        datalist.append([count, drama_content_class, drama_content_name, drama_content_text])
                        count += 1
                with open("C:/Users/97227/Desktop/pip/wiki_ark/public/text/"+title_csv, 'wb') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(datalist)
    return datalist0


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
def saveData(datalist, savepath):
    print("save.......")
    with open(savepath, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(datalist)


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # init_db("movietest.db")
    print("爬取完毕！")
