import string
import random
import douban.database as db
import re
import json
from scrapy import Spider
from douban.items import UserMovie
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule

cursor = db.connection.cursor()
# 获取评论区用户的url
class UserMovieSpider(CrawlSpider):
    name = 'user_movie'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    allowed_domains = ["movie.douban.com","m.douban.com"]
    sql = 'SELECT url FROM hq_movie_url'
    print("select movies url from db: ", sql)
    cursor.execute(sql)
    movies = cursor.fetchall()
    if len(movies) > 0:
        movie_list = [ i['url'] for i in movies]
        urls = tuple(movie_list)
    rules = (Rule(LinkExtractor(allow=('movie.douban.com/subject/(\d)*/')), callback='parse_movie', process_request='cookie', follow=False), )

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
    
    def parse_movie(self, response):
        meta = UserMovie()
        regx = '//div[@id="hot-comments"]/div[@class="comment-item"]//span[@class="comment-info"]/a/@href'
        data = response.xpath(regx).extract()
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
        if len(data) > 0:
            for url in data:
                temp = re.sub(r'h.*people/', "", url)
                user_id = re.sub(r'\/.*', "", temp)
                user_movie_url = "https://movie.douban.com/people/" + user_id + "/collect?sort=rating&start=0&mode=grid&tags_sort=count"
                #self.start_urls.append(url)
                print("User URL:", user_movie_url)
                meta['url'] = user_movie_url
        regx = '//div[@class="review-list  "]/div/div/header/a/@href'
        data = response.xpath(regx).extract()
        if len(data) > 0:
            for url in data:
                temp = re.sub(r'h.*people/', "", url)
                user_id = re.sub(r'\/.*', "", temp)
                user_movie_url = "https://movie.douban.com/people/" + user_id + "/collect?sort=rating&start=0&mode=grid&tags_sort=count"
                #self.start_urls.append(url)
                print("User URL:", user_movie_url)
                meta['url'] = user_movie_url
        return meta

   