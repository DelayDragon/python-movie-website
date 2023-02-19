# 导入米快
import pandas as pd
import pymysql
import requests  # 网络请求模块
from lxml import etree  # 数据解析模块
import time
from multiprocessing.dummy import Pool
from requests.exceptions import RequestException

# 插入数据到数据库
def insert(value):
    db = pymysql.connect(host='localhost',
                    port=3306,
                    database='movie-website',
                    user='root',
                    password='admin123',
                    charset='utf8'
                    )
    cursor = db.cursor()
    sql = "INSERT INTO DoubanTop(title,poster,src,dictor,score,comment,summary) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    try:
        cursor.executemany(sql,value)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print('插入数据失败')
    db.close()

# 功能函数，获取列表的第一个元素，去除空格，遇空返空
def get_first_text(list):
    try:
        return list[0].strip()
    except:
        return ''

# 提取数据
def get_html_data():
    # df = pd.DataFrame(columns=['序号', '海报', '标题', '链接', '导演', '评分', '评价人数', '简介'])
    # 解析数据
    urls = [
    'https://movie.douban.com/top250?start={}&filter='.format(str(i * 25)) for i in range(10)]
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    info = []
    for url in urls:
        res = requests.get(url=url, headers=headers)  # 发起请求
        html = etree.HTML(res.text)  # 将返回的文本加工为可以解析的html
        lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')  # 获取每个电影的li元素
        try:
            for li in lis:
                item = []
                title = get_first_text(
                    li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))  # 电影标题
                poster = get_first_text(li.xpath('./div/div[1]/a/img/@src'))  # 海报链接
                src = get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))  # 电影链接
                dictor = get_first_text(
                    li.xpath('./div/div[2]/div[2]/p[1]/text()'))  # 导演
                score = get_first_text(
                    li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))  # 评分
                comment = get_first_text(
                    li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))  # 评价人数
                summary = get_first_text(
                    li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))  # 电影简介
                # print(count,poster, title, src, dictor, score, comment, summary)  # 输出
                # df.loc[len(df.index)] = [count, poster, title,
                #         src, dictor, score, comment, summary]
                item.append(poster)
                item.append(title)
                item.append(src)
                item.append(dictor)
                item.append(score)
                item.append(comment)
                item.append(summary)
                # insert(item)
                info.append(item)
        except:
            pass
    return info



    # 处理数据
    # df.to_excel('豆瓣电影top250.xlsx', sheet_name='豆瓣电影top250数据', na_rep="")

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
    cursor.execute("DROP TABLE IF EXISTS DoubanTop")

    sql = """CREATE TABLE DoubanTop (
        ID INT PRIMARY KEY AUTO_INCREMENT,
        title CHAR(255),
        poster CHAR(255),
        src CHAR(255),
        dictor CHAR(255),
        score CHAR(255),
        comment CHAR(255),
        summary CHAR(255)
    )"""
    cursor.execute(sql)
    db.close()

# 主函数
# def main(offset):
    # urls = [
    #     'https://movie.douban.com/top250?start={}&filter='.format(str(i * 25)) for i in range(10)]
    # get_html_data()


# 入口函数
if __name__ == '__main__':
    # 发起网络请求
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    # }
    # print('多线程爬取开始')
    # start_time = time.time()
    # p = Pool(10)
    # p.map(main,[i * 10 for i in range(10)])
    # end_time = time.time()
    # print('多线程爬取结束')
    # p.close()
    # p.join()
    create()
    movie_data = get_html_data()
    print(movie_data)
    insert(movie_data)
