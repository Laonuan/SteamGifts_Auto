import re
import requests
import ConstVar


class SteamGiftsCrawler:

    def __init__(self):
        self.cookie = ConstVar.COOKIE
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,de;q=0.4,ja;q=0.2,zh-TW;q=0.2,pt;q=0.2",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            "Cookie": self.cookie
        }

    def getHTMLText(self, url):
        try:
            r = requests.get(url, timeout=90, headers=self.headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            return r.text
        except Exception, e:
            print e.message
            return ""

    def regex_content(self, content):
        codes = []
        expression = 'href="/giveaway/(.*?)/(.*?)"'
        pattern = re.compile(expression, re.S)
        items = re.findall(pattern, content)

        for item in items:
            if item not in codes:
                code = item[0]
                game = item[1]
                game = game.replace('/entries', '')
                game = game.replace('/comments', '')
                codes.append([code, game])

        expression = 'name="xsrf_token" value="(.*?)"'
        pattern = re.compile(expression, re.S)
        token = re.findall(pattern, content)
        try:
            token = token[0]
        except Exception:
            token = ""

        return token, codes

    def get_information(self, url):
        content = self.getHTMLText(url)
        return self.regex_content(content)


if __name__ == "__main__":
    crawler = SteamGiftsCrawler()
    print crawler.get_information("https://www.steamgifts.com/giveaways/search?page=2")
