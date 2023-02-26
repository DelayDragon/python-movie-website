import json
import requests
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import urllib.request
from pybloom_live import BloomFilter

# 获取演员的所有id，未去重
def get_actor_id():
    arr = []
    db = pymysql.connect(host='localhost',
                    port=3306,
                    database='movie-website',
                    user='root',
                    password='admin123',
                    charset='utf8'
                    )
    cursor = db.cursor()
    cursor.execute("SELECT actor_id FROM actor_brief")
    for (i,) in cursor.fetchall():
        arr.append(i)
    db.close()
    return arr

# 去重,适合去重主键重复的
def remove_repetition(values):
    info = [] # 承载返回的数据集
    info_re = []
    f = BloomFilter(capacity=5000,error_rate=0.01)
    [f.add(i) for i in values]
    for i in values:
        if i in f:
            if i in info:
                info_re.append(i)
            else:
                info.append(i)
        else:
            info.append(i)
        
    return info

# 去重2 普通的去重空间复杂度更低
def remove_repetition_test(values):
    info = []
    for i in values:
        if i in info:
            pass
        else:
            info.append(i)
    return info

# 去除空格
def remove_blank(str):
    s = str.replace(' ', '')

# 将列表用/分隔转换成str
def to_str(arr):
    str = ''
    for i in arr:
        str += i + '/'
    return str

# 获取职员详细信息
def get_actor_details(array):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    urls = ['https://movie.douban.com/celebrity/{}/'.format(str(i)) for i in array]
    info = []
    for url in  urls:
        item = []
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        
        soup = BeautifulSoup(content, 'lxml')

        # 职员名称
        actor_name = soup.select('div[id="content"] > h1')[0].string

        # 职员的所有属性
        a_list = []
        attribute_list = soup.select('div[class="info"] > ul > li')
        for attribute in attribute_list:
            a_list.append(attribute.text.replace('\n', '').replace(' ', ''))
        a_list = to_str(a_list)
        
        # 职员简介
        personal_introduction = soup.select('div[id="intro"] > div[class="bd"]')
        try:
            personal_introduction = personal_introduction[0].select('span[class="all hidden"]')[0].text
        except:
            personal_introduction = personal_introduction[0].text.strip()

        item.append(actor_name)
        item.append(a_list)
        item.append(personal_introduction)
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
    cursor.execute("DROP TABLE IF EXISTS actor_details")

    sql = """CREATE TABLE actor_details (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        actor_name CHAR(255),
        attribute_list CHAR(255),
        personal_introduction VARCHAR(2000)
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
    sql = 'INSERT INTO actor_details(actor_name,attribute_list,personal_introduction) VALUES(%s,%s,%s)'   
    try:
        cursor.executemany(sql,values)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print('插入数据失败')
    db.close()

create()
info = get_actor_id()
info_redo = remove_repetition_test(info)
actor_details = get_actor_details(info_redo)
insert(actor_details)