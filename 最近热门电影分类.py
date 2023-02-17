from 最近热门电影tags import getTags
import requests
import json
import pymysql
from translate import Translator
import pypinyin


tags = getTags()


def insertMovie(tag,values):
    db = pymysql.connect(host='localhost',
                         port=3306,
                         database='movie-website',
                         user='root',
                         password='admin123',
                         charset='utf8'
                         )
    cursor = db.cursor()
    print('连接成功')
    sql = """INSERT INTO {}(epiodes_info,rate,cover_x,title,url,playable,cover,id,cover_y,is_new) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """.format(tag)
    try:
        cursor.execute(sql,values)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print('插入数据失败')
    db.close()


def toNull(arr):
    array = []
    for i in arr:
        if i == '':
            array.append(None)
        else:
            array.append(i)
    return array

def getLastlyMovie():
    for tag in tags:
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&page_limit=500&page_start=0'.format(
            tag)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        create(pinyin(tag))
        res = requests.get(url=url, headers=headers).text
        for i in json.loads(res)['subjects']:
            # print(toNull(list(i.values())))
            # print(list(i.values()))
            insertMovie(pinyin(tag), list(i.values()))
        # insertMovie(tag, json.loads(res)['subjects'])
        # 请求链接数组
        # urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag={}&page_limit=2&page_start=0'.format(str(tags[i])) for i in range(len(tags))]
        # for url in urls:
        #     headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        #     }
        #     res = requests.get(url=url, headers=headers).text
        #     print(json.loads(res)['subjects'])


# 中文转化为拼音，用于建立数据库表
def pinyin(value):
    s = ''
    for i in pypinyin.pinyin(value, style=pypinyin.NORMAL):
        s += ''.join(i) + ""
    return s


def create(tag):
    db = pymysql.connect(host='localhost',
                         port=3306,
                         database='movie-website',
                         user='root',
                         password='admin123',
                         charset='utf8'
                         )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS {}".format(tag))

    sql = """CREATE TABLE {} (
        epiodes_info CHAR(255),
        rate CHAR(10),
        cover_x INT,
        title CHAR(255),
        url CHAR(255),
        playable TINYINT(1),
        cover CHAR(255),
        id CHAR(255) PRIMARY KEY,
        cover_y INT,
        is_new TINYINT(1)
    )""".format(tag)
    cursor.execute(sql)
    db.close()


getLastlyMovie()
# for tag in tags:
#     create(pinyin(tag))

# a = ['', '8.5', 1428, '你的名字。', 'https://movie.douban.com/subject/26683290/', True, 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2395733377.jpg', '26683290', 2000, False]
# print(a)
# t = 'remen'
# insertMovie(t,a)
