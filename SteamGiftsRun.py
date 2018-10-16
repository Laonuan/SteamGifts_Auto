# -*- coding: utf-8 -*-

import time
from SteamGiftsCrawler import *
from SteamGiftsPost import *


class Run:

    def __init__(self):
        self.post = SteamGiftsPost()
        self.crawler = SteamGiftsCrawler()
        self.code_hash = set([])
        self.game_hash = set([])

    def start(self):
        page = 1
        error_cnt = 0
        stop_join = False
        self.game_hash.clear()

        while not stop_join and page < 50:
            url = "https://www.steamgifts.com/giveaways/search?page={page}".format(page=page)
            print url

            try:
                token, info = self.crawler.get_information(url)
            except Exception, e:
                print "get information error", e
                return False

            for c in info:
                code = c[0]
                game = c[1]

                if code in self.code_hash or game in self.game_hash:
                    continue

                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print current_time, "Code:{code} Game:{game}".format(code=code, game=game)

                try:
                    data = self.post.join_gift(code, token)
                except Exception, e:
                    print "join error", e
                    error_cnt += 1
                    break

                if data is None:
                    print "Data Error"
                    break
                else:
                    result, point, msg = data
                    print "Result:{result} Point:{point} Message:{msg}".format(result=result, point=point, msg=msg)

                if point <= 5 :
                    stop_join = True
                    break
                elif result == "success":
                    self.code_hash.add(code)
                    self.game_hash.add(game)
                    error_cnt = 0
                elif result == "error":
                    error_cnt += 1
                    self.game_hash.add(game)
                    if msg != "Not Enough Points":
                        self.code_hash.add(code)
                        # self.game_hash.add(game)
                    
                if error_cnt > 50:
                    stop_join = True
                    break

                time.sleep(5)

            page += 1
            
        return True


if __name__ == "__main__":

    run = Run()
    rest_time = 2
    
    while True:
        if not run.start():
            rest_time = 0.125
        else:
            rest_time = 2

        run.game_hash = set([])
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print current_time, "Rest {rest_time} hour".format(rest_time=rest_time)
        time.sleep(60 * 60 * rest_time)




