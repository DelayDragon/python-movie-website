import json
import requests
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import urllib.request
import re
from pybloom_live import BloomFilter

# 得到字符串中的id
def get_number(value):
    number = re.compile(r'\d+').findall(value)[0]
    return number

def getMovieId():
    arr = []
    db = pymysql.connect(host='localhost',
                    port=3306,
                    database='movie-website',
                    user='root',
                    password='admin123',
                    charset='utf8'
                    )
    cursor = db.cursor()
    cursor.execute("SELECT ID FROM all_movie")
    for (i,) in cursor.fetchmany(2):
        arr.append(i)
    db.close()
    return arr

array = getMovieId()
urls = ['https://movie.douban.com/subject/{}/celebrities'.format(str(i)) for i in array]

# 连接列表中的数据成字符串
def link_values(arr):
    str = ''
    for i in arr:
        str +=  '/' + i
    return str

# 所有职员的主要信息
def get_actor():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    info = []
    for url in urls:
        print(url)
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        
        soup = BeautifulSoup(content, 'lxml')

        # 所有职员
        actor_brief_list = soup.select('div[id="celebrities"] > div[class="list-wrapper"] > ul > li')

        # 储存职员信息

        for actor_brief in actor_brief_list:
            item = []
            # 职员链接编号
            actor_id = get_number(actor_brief.select('a')[0]['href'])

            # 职员名称
            actor_name = actor_brief.select('a')[0]['title']

            # 职员头像
            actor_pictrue = re.compile(r'[(](.*?)[)]',re.S).findall(actor_brief.select('a > div')[0]['style'])
            if len(actor_pictrue) == 2:
                actor_pictrue = actor_pictrue[1]
            else:
                actor_pictrue = actor_pictrue[0]
            actor_avatar = actor_pictrue
            # print(actor_link, actor_name, actor_avatar)

            # 职员角色
            actor_role = actor_brief.select('div[class="info"] > span[class="role"]')
            if len(actor_role) == 0:
                actor_role = ''
            else:
                actor_role = actor_role[0]['title']
            # print(actor_name, actor_role)

            # 职员代表作
            actor_works = []
            actor_representative_list = actor_brief.select('div[class="info"] > span[class="works"] > a')
            for actor_representative in actor_representative_list:
                actor_works.append(actor_representative['title'])
                # print(actor_representative['title'])
            
            # 储存信息
            item.append(actor_id)
            item.append(actor_name)
            item.append(actor_avatar)
            item.append(actor_role)
            item.append(link_values(actor_works))
            info.append(item)

    return info

# 连接数据库，建表
def create():
    db = pymysql.connect(host='localhost',
                         port=3306,
                         database='movie-website',
                         user='root',
                         password='admin123',
                         charset='utf8'
                         )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS actor_brief")

    sql = """CREATE TABLE actor_brief (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        actor_id INT NOT NULL,
        name VARCHAR(255) ,
        avatar VARCHAR(255) ,
        role VARCHAR(255) ,
        works VARCHAR(255)
    )"""
    cursor.execute(sql)
    db.close()

# 插入数据
def insert(values):
    db = pymysql.connect(host='localhost',
                    port=3306,
                    database='movie-website',
                    user='root',
                    password='admin123',
                    charset='utf8'
                    )
    cursor = db.cursor()
    sql = "INSERT INTO actor_brief(actor_id,name,avatar,role,works) VALUES(%s,%s,%s,%s,%s)"
    try:
        cursor.executemany(sql,values)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print('插入数据失败')
    db.close()

# 去重
def remove_repetition(values):
    info = []
    f = BloomFilter(capacity=5000,error_rate=0.01)
    [f.add(i[0]) for i in values]
    return f

if __name__ == '__main__':
    create()
    info = get_actor()
    # print(info)
    remove_repetition(info)
    insert(info)