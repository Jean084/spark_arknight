import requests
import os
import time
import re
import random
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
json_url = "https://api.bilibili.com/x/v2/medialist/resource/list?mobi_app=web&type=1&biz_id=3461583078427355&oid=&otype=2&ps=20&direction=false&desc=true&sort_field=1&tid=0&with_current=false"
           #https://api.bilibili.com/x/v2/medialist/resource/list?mobi_app=web&type=1&biz_id=3461583078427355&oid=         &otype=2&ps=20&direction=false&desc=false&sort_field=1&tid=0&with_current=false
           #https://api.bilibili.com/x/v2/medialist/resource/list?mobi_app=web&type=1&biz_id=3461583078427355&oid=1750719624&otype=2&ps=20&direction=false&desc=true&sort_field=1&tid=0&with_current=false
           #https://api.bilibili.com/x/v2/medialist/resource/list?mobi_app=web&type=1&biz_id=3461583078427355&oid=1151928360&otype=2&ps=20&direction=false&desc=true&sort_field=1&tid=0&with_current=false

class MySpider(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit"
                          "/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}

    def get_json(self, url):
        response = requests.get(url, headers=self.headers)
        print(response)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                print("error",e )
        else:
            print("get su")

    def download_video(self, url, video_name):
        response = requests.get(url, headers=self.headers, stream=True)
        if not os.path.exists("video"):
            os.mkdir("video")
        if response.status_code == 200:
            with open("video/" + video_name + ".mp4", "wb") as file:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    file.flush()
                print("finish")
        else:
            print("false")


if __name__ == '__main__':
    spider = MySpider()
    for i in range(10):
        json_data = spider.get_json(json_url.format(i))
        # print(json_data.get('data', "123").encode('latin1').decode('utf-8'))
        media_list = json_data.get('data', "123").get("media_list","123")
        vid=0
        for media in media_list:
            print(json.dumps(media,ensure_ascii=False))
            vid = media.get("id","0")
            title = media.get("title","0")
            print(vid,title.encode("UTF-8"))
        json_str = json.dumps(json_data.get('data', "123"),ensure_ascii=False)
        print(json_str)
        video_infos = json["data"]["items"]
        for video_info in video_infos:
            title = video_info["item"]["description"]
            comp = re.compile("[^A-Z^a-z^0-9^\u4e00-\u9fa5]")
            title = comp.sub("", title)
            video_url = video_info["item"]["video_playurl"]
            print(title, video_url)
            spider.download_video(video_url, title)
        time.sleep(random.randint(3, 6))