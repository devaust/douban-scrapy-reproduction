import string
import random
import douban.database as db
import re
import json
from scrapy import Spider
from douban.items import UserSeen
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule

cursor = db.connection.cursor()
#获取用户看过的电影
class UserSeenSpider(CrawlSpider):
    name = 'user_seen'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    allowed_domains = ["movie.douban.com"]
    sql = 'SELECT url FROM user_url'
    print("select user url from db: ", sql)
    cursor.execute(sql)
    user_url = cursor.fetchall()
    if len(user_url) > 0:
        urls = [ i['url'] for i in user_url]
        urls = tuple(urls)
    rules = (Rule(LinkExtractor(allow=('movie.douban.com/people/.*count$')), callback='parse_user', process_request='cookie', follow=False),)

    def cookie(self, request):
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for
                      x in range(11))
        request.cookies['bid'] = bid
        request = request.replace(url=request.url.replace('?', '/?'))
        return request

    def start_requests(self):
        for url in self.urls:
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            yield Request(url, cookies={'bid': bid})

    def parse_user(self, response):
        print("Parsing User")
        meta = UserSeen()
        regx = '//div[@id="wrapper"]//div[@class="info"]/ul/li/a/@href[1]'
        raw_data = response.xpath(regx).extract()
        if len(raw_data) > 0:
            data = raw_data[0]
            temp = re.sub(r'\/people\/', "", data)
            temp = re.sub(r'\/', "", temp)
            meta['user_id'] = temp
            print("User_id:", temp)
        else:
            meta['user_id'] = ""
        regx = '//div[@class="grid-view"]/div//li[@class="title"]/a/@href'
        raw_data = response.xpath(regx).extract()
        data = []
        if len(raw_data) > 0:
            for url in raw_data:
                temp = re.sub(r'h.*subject/', "", url)
                temp2 = re.sub(r'(\/)', "", temp)
                data.append(temp2)
            all_douban_id = ",".join(data)
            meta['seen_movie_id'] = all_douban_id
            print("Seen:", all_douban_id)
        else:
            meta['seen_movie_id'] = ""
        return meta
