import requests
import database as db
import json
import time
import random

cursor = db.connection.cursor()
def get_data(url, count, proxy):
    params = {"sort":"U", "range":"9,10", "tags":"%E7%94%B5%E5%BD%B1", "start":str(count)}
    #headers = {'User-Agent': 'ua.chrome'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.115'}
    url = url + str(count)
    print(url)
    r = requests.get(url=url, proxies=proxy, headers=headers)
    #print(json.loads(r.text))
    return json.loads(r.text)

#print(raw_json['data'])
def save_data(raw_json):
    print(len(raw_json['data']))
    for i in range(len(raw_json['data'])):
        url = str(raw_json['data'][i]['url'])
        #name = str(raw_json['data'][i]['title'])
        print(url)
        values = (url)
        sql = "INSERT INTO hq_movie_url (url) VALUES ('%s')"
        cursor.execute(sql % values)
    db.connection.commit()

tunnel = "tps139.kdlapi.com:15818"

username = "t19513891049081"
password = "y9le01hg"

proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}

#该url对应榜单最大数目是855
url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=9,10&tags=%E7%94%B5%E5%BD%B1&start="
for i in range(43):
    start_num = i*20
    raw_json = get_data(url=url, proxy=proxies, count=start_num)
    save_data(raw_json)
    time.sleep(1)


