import requests
import json
import re
import time
import json
import os
import importlib
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import pickle

damai_url = "https://www.damai.cn/"
login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
target_url = "https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.10d872a3Or4k5v&id=778626949623&clicktitle=2024%E3%80%8A%E6%98%8E%E6%97%A5%E6%96%B9%E8%88%9F%E3%80%8B%E9%9F%B3%E5%BE%8B%E8%81%94%E8%A7%89%E4%B8%93%E5%9C%BA%E6%BC%94%E5%87%BA-%E4%B8%8D%E8%A7%85%E6%B5%AA%E5%B0%98"
class Concert:
    def __init__(self):
        self.status = 0
        self.login_method = 1
        self.driver = webdriver.Chrome()
    def set_cookie(self):
        self.driver.get(damai_url)
        print("###请点击登录###")
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            time.sleep(1)
        print('###请扫码登录###')

        while self.driver.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            time.sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(target_url)


    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    'domain':'.damai.cn',
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)
            print('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):
                self.set_cookie()
            else:
                self.driver.get(target_url)
                self.get_cookie()

    def enter_concert(self):
        """打开浏览器"""
        print('###打开浏览器，进入大麦网###')
        # self.driver.maximize_window()           # 最大化窗口
        self.login()
        self.driver.refresh()
        self.status = 2
        print("###登录成功###")
        if self.isElementExist('/html/body/div[2]/div[2]/div/div/div[3]/div[2]'):
            self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[3]/div[2]').click()

    def isElementExist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(element)
            return flag

        except:
            flag = False
            return flag

    def choose_ticket(self):
        if self.status == 2:
            print("="*30)
            print("###开始进行日期及票价选择###")
            while self.driver.title.find('确认订单') == -1:
                try:
                    buybutton = self.driver.find_element_by_class_name('buybtn').text
                    if buybutton == "提交缺货登记":
                        self.status=2
                        self.driver.get(target_url)
                        print('###抢票未开始，刷新等待开始###')
                        continue
                    elif buybutton == "立即预定":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 3
                    elif buybutton == "立即购买":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 4
                    elif buybutton == "选座购买":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 5
                except:
                    print('###未跳转到订单结算界面###')
                title = self.driver.title
                if title == '选座购买':
                    self.choice_seats()
                elif title == '确认订单':
                    while True:
                        print('waiting ......')
                        if self.isElementExist('//*[@id="container"]/div/div[9]/button'):
                            self.check_order()
                            break

    def choice_seats(self):
        while self.driver.title == '选座购买':
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/img'):
                print('请快速的选择您的座位！！！')
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[2]/div'):
                self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/button').click()

    def check_order(self):
        if self.status in [3,4,5]:
            print('###开始确认订单###')
            try:
                self.driver.find_element_by_xpath('//*[@id="container"]/div/div[2]/div[2]/div[1]/div/label').click()
            except Exception as e:
                print("###购票人信息选中失败，自行查看元素位置###")
                print(e)
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//div[@class = "w1200"]//div[2]//div//div[9]//button[1]').click()

    def finish(self):
        self.driver.quit()

if __name__ == '__main__':
    con = Concert()
    try:
        con.enter_concert()
        con.choose_ticket()

    except Exception as e:
        print(e)
        con.finish()
