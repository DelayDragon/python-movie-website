import json
import requests
from lxml import etree
import pymysql

# 获取信息
def getTags():
    url = 'https://movie.douban.com/j/search_tags?type=movie&source=index'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers).text
    return json.loads(res)['tags']

# 插入数据
def insertTags(values,db):
    print(values)
    cursor = db.cursor()
    sql = "INSERT INTO resentlyhot(tag_name) value(%s)"
    try:
        cursor.executemany(sql,values)
        db.commit()
        print('更新数据成功')
    except:
        db.rollback()
        print('更新数据失败')

# 更新数据
def updateTags(tags):
    db = pymysql.connect(host='localhost',
                        port=3306,
                        database='movie-website',
                        user='root',
                        password='admin123',
                        charset='utf8'
                        )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS resentlyhot")

    sql = """
        CREATE TABLE resentlyhot (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            tag_name char(40)
        )
    """
    cursor.execute(sql)
    insertTags(tags, db)
    db.close()

# 查询resentlyhot的数据
def checkDb():
    db = pymysql.connect(host='localhost',
                         port=3306,
                         database='movie-website',
                         user='root',
                         password='admin123',
                         charset='utf8'
                         )
    cursor = db.cursor()
    checkSql = 'select tag_name from resentlyhot'
    cursor.execute(checkSql)
    tags = cursor.fetchall()
    for tag in tags:
        print(tag[0])
    db.close()

# 入口函数
if __name__ == '__main__':
    tags = getTags()
    updateTags(tags)


