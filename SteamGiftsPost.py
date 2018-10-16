# -*- coding:utf-8 -*-

import urllib
import json
import requests
import ConstVar

class SteamGiftsPost:

    def __init__(self):
        self.request_url = 'https://www.steamgifts.com/ajax.php'
        self.cookie = ConstVar.COOKIE
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,de;q=0.4,ja;q=0.2,zh-TW;q=0.2,pt;q=0.2",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            "Connection": "keep-alive",
            "Content-Length": "70",
            "Content-Type": "application/x-www-form-urlencoded; charse =UTF-8",
            "Cookie": self.cookie
        }

    def bulid_param(self, code, token, do="entry_insert"):
        param = dict()
        param['code'] = code
        param['do'] = do
        param['xsrf_token'] = token

        return param

    def send_post(self, param):
        post_data = urllib.urlencode(param).encode('utf-8')
        self.headers["Content-Length"] = str(len(post_data))

        try:
            r = requests.post(url=self.request_url, data=post_data, timeout=90, headers=self.headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
        except Exception, e:
            print e.message
            return ""

        return json.loads(r.text, encoding='utf-8')

    def unpack_json(self, data):
        result = data.get("type", "error").encode("utf-8")
        point = data.get("points", "0").encode("utf-8")
        msg = data.get("msg","None").encode('utf-8')

        try:
            point = int(point)
        except ValueError:
            point = 0
        return [result, point, msg]

    def join_gift(self, code, token, do="entry_insert"):
        param = self.bulid_param(code, token, do)
        data = self.send_post(param)

        if data is None:
            return None
        else:
            return self.unpack_json(data)

if __name__ == "__main__":

    gift_post = SteamGiftsPost()
    print gift_post.join_gift("XnHUW", "8a6c469adb8bab15e9e03d22fe12b182")
