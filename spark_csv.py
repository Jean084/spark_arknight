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



findLink_board = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象
findName_board = re.compile(r'<div class="brandtitle">(.*?)')  # 创建正则表达式对象
findLogo_board = re.compile(r'<div class="brand-content-logo">(.*?)')  # 创建正则表达式对象
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
findcost_cloth = re.compile(r'<div style="display:inline-block;line-height:24px;vertical-align:top;font-weight:bold;font-size:15px;color:white;padding-left:28px;">(.*?)</div>')
findbelong_cloth = re.compile(r'<td colspan="3">(.*?)')
findtime_cloth = re.compile(r'</th><td colspan="3">(.*?) ~ <br/>')
findtext_cloth = re.compile(r'<td colspan="4" style="text-align:left; height:(.*);"><p>(.*?)</p>')
findimg_cloth = re.compile(r'<img alt="(.*?)"')

def main():
    baseurl = "https://prts.wiki/w/%E6%97%B6%E8%A3%85%E5%9B%9E%E5%BB%8A"  #要爬取的网页链接
    # 1.爬取网页
    datalist,board_list = getData(baseurl)
    savepath = "skin.xls"    #当前目录新建XLS，存储进去
    # dbpath = "movie.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(datalist,board_list,savepath)      #2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)



# 爬取网页
def getData(baseurl):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    datalist = []  #用来存储爬取的网页信息
    board_list=[]
    html = askURL(baseurl)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="brandbtn"):
        item=str(item)
        board_link = re.findall(findLink_board, item)[0]
        board_name = board_link.split("/")[-1]
        board_html = askURL("https://prts.wiki"+urllib.quote(board_link))
        board_soup = BeautifulSoup(board_html, "html.parser")
        board_img = board_soup.find_all('div', class_="swiper-slide")
        conut=0
        for img in board_img:
            img=str(img)
            img_data = re.findall(findImg, img)[0]
            if img_data=='':
                continue
            title = u"C:/Users/97227/Desktop/pip/wiki_ark/public/img/board/"+str(board_name)+'_'+str(conut)+".png"
            img_save = requests.get("https:" +img_data, headers=head).content
            with open(title, 'wb') as f:  # 把图片数据写入本地，wb表示二进制储存
                for chunk in img_save:
                    f.write(chunk)
            conut+=1
        board_cont = board_soup.find_all('div', class_="brand-container")[0]
        logo ="https:" + str(re.findall(findImg0,str(board_cont))[0])
        logo_title = u"C:/Users/97227/Desktop/pip/wiki_ark/public/img/board/" + str(board_name)+".png"
        logo_save = requests.get(logo, headers=head).content
        with open(logo_title, 'wb') as f:  # 把图片数据写入本地，wb表示二进制储存
            for chunk in logo_save:
                f.write(chunk)
        board_text = str(re.findall(findText_board, str(board_cont))[0]).replace("<br/>",'\n')
        board_text = str(re.findall(findText_board, str(board_cont))[0]).replace("<br/>",'\n')
        board_list.append([board_name,english,board_text,conut])
        clothes_meg = board_soup.find_all('table', class_="wikitable logo nomobile")
        for clothe_meg in clothes_meg:
            #print(clothe_meg)
            clothe_meg=str(clothe_meg).replace("\n","")
            #print(clothe_meg)
            name=re.findall(findName_cloth, clothe_meg)
            if(len(name)<1):
                name=re.findall(findName_else0_cloth, clothe_meg)
                if(len(name)<1):
                    name = re.findall(findName_else1_cloth, clothe_meg)
            cloth_name = str(name[0])
            colth_introduce0 = str(re.findall(findIntroduce0_cloth, clothe_meg)[0])
            colth_introduce1 = str(re.findall(findIntroduce1_cloth, clothe_meg)[0])
            art_get = re.findall(findArtiest_cloth, clothe_meg)
            colth_Artiest = str(art_get[0])
            art_get[1]=[x for x in str(art_get[1]).split('<') if x][0]
            art_get[1]=[x for x in str(art_get[1]).split('>') if x][-1]
            if art_get[1]=="采购中心":
                colth_get = art_get[1]
                cost=re.findall(findcost_cloth, clothe_meg)
                time0=re.findall(findtime_cloth, clothe_meg)
                if len(cost)<1:
                    colth_cost=0
                else:
                    colth_cost=str(re.findall(findcost_cloth, clothe_meg)[0])
                if len(time0)<1:
                    colth_time="-"
                else:
                    colth_time = str(re.findall(findtime_cloth, clothe_meg)[0]).split(">")[-1]
            elif art_get[1]=="活动获得":
                colth_get = art_get[1]
                cost=re.findall(findget_cloth, clothe_meg)
                time0 = re.findall(findtime_cloth, clothe_meg)
                if len(cost)<1:
                    colth_cost="-"
                else:
                    colth_cost = str(re.findall(findget_cloth, clothe_meg)[0][0])
                if len(time0)<1:
                    colth_time="-"
                else:
                    colth_time = str(re.findall(findtime_cloth, clothe_meg)[0]).split(">")[-1]
                print(colth_cost)
            else:
                colth_get = art_get[1]
                colth_cost = 0
                colth_time="-"
            belong_img=re.findall(findimg_cloth, clothe_meg)
            colth_belong = str(belong_img[0]).split(" ")[-1].split(".")[0]
            colth_text = str(re.findall(findtext_cloth, clothe_meg)[0][1])
            colth_img = str(belong_img[1]).replace(" ","_")
            colth_staff = colth_img.split("_")[1]
            print(board_name)
            print(cloth_name)
            print(colth_img)
            print(colth_introduce0)
            print(colth_introduce1)
            print(colth_Artiest)
            print(colth_get)
            print(colth_cost)
            print(colth_time)
            print(colth_belong)
            print(colth_text)
            print(colth_staff)
            datalist.append([board_name,cloth_name,colth_img,colth_introduce0,colth_introduce1,colth_Artiest,colth_get,colth_cost,colth_time,colth_belong,colth_text,colth_staff])
    return datalist,board_list


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
def saveData(datalist,broad_list,savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet_clothes = book.add_sheet('clothes', cell_overwrite_ok=True) #创建工作表
    sheet_broad = book.add_sheet('broad', cell_overwrite_ok=True) #创建工作表
    col_clothes = ("board","name","img","intro0","intro1","artist","get","cost","time","belong","text","staff")
    broad_clothes = ("name","english","intro","num")
    for i in range(0,11):
        sheet_clothes.write(0,i,col_clothes[i])  #列名
    for i in range(len(datalist)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0,11):
            sheet_clothes.write(i+1,j,data[j])  #数据
    for i in range(0,3):
        sheet_broad.write(0,i,broad_clothes[i])  #列名
    for i in range(len(broad_list)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = broad_list[i]
        for j in range(0,3):
            sheet_broad.write(i+1,j,data[j])  #数据
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