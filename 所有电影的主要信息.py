from 下载图片 import parsing_picture
import pymysql


def connectDb():
    array = []
    db = pymysql.connect(host='localhost',
                    port=3306,
                    database='movie-website',
                    user='root',
                    password='admin123',
                    charset='utf8'
                    )
    cursor = db.cursor()
    sql = 'select cover,id from all_movie'
    cursor.execute(sql)
    for (i,) in cursor.fetchall():
        array.append(i)
    return array

array = connectDb()
print(array)

