import random
import pymysql
import threading
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import time
from utils.testIpPool import test_proxy_list
from 下载图片 import parsing_picture

# 限制多线程的并发数量
sem = threading.Semaphore(5)

def checkProxies(proxies):
    url = 'https://movie.douban.com/'
    valid_proxies = []
    for proxy in proxies:
        response = requests.get(url=url,proxies={proxy},timeout=5)

        if response.status_code == 200:
            valid_proxies.append(proxy)
        else:
            pass
    return valid_proxies

# 获取地理池
def get_89ip_IP():
    # 获取89免费代理网站前三页IP及其端口
    urls = ['https://www.89ip.cn/index_{}.html'.format(str(i)) for i in range(1,4)]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    info = []
    for url in urls:
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        
        soup = BeautifulSoup(content, 'lxml')
        
        tableList = soup.select('table[class=layui-table] > tbody > tr')
        for tr in tableList:
            ip = tr.select('td')[0].text.split()[0]
            port = tr.select('td')[1].text.split()[0]
            item = {"http": f"http://{ip}:{port}","https": f"https://{ip}:{port}"}
            info.append(item)
    return info
 
# 格式化得到的ip的port
def proxiesPool(info):
    proxies = []
    for item in info:
        proxies.append('http": f"http://{}:{}'.format(item[0],item[1]))
    return proxies

# 获取需要爬取电影的id
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
    for (i,) in cursor.fetchall():
        arr.append(i)
    db.close()
    return arr

# 测试使用代理池
def parseHtml_inpool(url):
    # 拿到ip代理地址池
    proxies = get_89ip_IP()

    try:
        # 随机选择一个代理
        proxy = random.choice(proxies)
        # 创建代理处理器
        proxy_hander = urllib.request.ProxyHandler(proxy)
        # 创建url打开器
        opener = urllib.request.build_opener(proxy_hander)
        # 安装url打开器
        urllib.request.install_opener(opener=opener)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        # 构建请求对象
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
    except :
        print(f'Request to {proxy} failed. Retrying with a different IP address...')
        parseHtml(url)
    else:
        content = response.read().decode('utf-8')
    
        soup = BeautifulSoup(content, 'lxml')
        return soup   

# 返回解析得到的html
def parseHtml(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        # 构建请求对象
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)

        content = response.read().decode('utf-8')
    
        soup = BeautifulSoup(content, 'lxml')
        return soup   


# 返回对应html爬取的信息
def parseData(soup, i):
    item = []
     # 电影名字
    movie_name = soup.select('span[property="v:itemreviewed"]')[0].text
    # print(movie_name)

    # 电影年份
    movie_year = soup.select('span[class="year"]')[0].text
    # print(movie_year)

    # 电影海报
    poster_url = soup.select('a[class="nbgnbg"] > img')[0]['src']
    # print(movie_poster)

    # 电影海报
    movie_poster = parsing_picture(poster_url,'allMovie_image/')

    # 豆瓣评分
    movie_score = soup.select('strong[property="v:average"]')[0].string
    # print(movie_score)        
    
    # 评价人数
    movie_comment = soup.find(property="v:votes").text
    # print(movie_comment)

    # 电影的所有属性值
    movie_attributes = soup.select('div[id="info"]')[0].text.split('<br>')[0]
    # print(movie_attributes)

    # 电影简介
    movie_plot = soup.select('span[property="v:summary"]')[0].text.strip().replace(' ','')
    # print(movie_plot)

    # 电影编号
    # movie_id = get_number_zero(url)
    movie_id = i
    

    item.append(movie_name)
    item.append(movie_year)
    item.append(poster_url)
    item.append(movie_score)
    item.append(movie_comment)
    item.append(movie_attributes)
    item.append(movie_plot)
    item.append(movie_id)
    item.append(movie_poster)
    return item

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
    cursor.execute("DROP TABLE IF EXISTS movie_details")

    sql = """CREATE TABLE movie_details (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        movie_name VARCHAR(255),
        movie_year VARCHAR(255),
        poster_url VARCHAR(255),
        movie_score VARCHAR(255),
        movie_comment VARCHAR(255),
        movie_attributes VARCHAR(1000),
        movie_plot VARCHAR(1000),
        movie_id varchar(255),
        movie_poster longblob
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
    sql = 'INSERT INTO movie_details(movie_name,movie_year,poster_url,movie_score,movie_comment,movie_attributes,movie_plot,movie_id,movie_poster) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'   
    try:
        cursor.executemany(sql,values)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print('插入数据失败')
    db.close()

#多线程解析网页
def startParseHtml(i):
    with sem:
            print("线程执行对应的编号：{}".format(i))
            info = []
            url = 'https://movie.douban.com/subject/{}'.format(str(i))
            soup = parseHtml(url)
            item = parseData(soup, i)
            info.append(item)
            insert(info)
    time.sleep(1)

# 主函数
def main():
    array = getMovieId()
    print(array)
    for i in array:
        th = threading.Thread(target=startParseHtml, args=(i,))
        th.start()


if __name__ == '__main__':
    create()
    main()

    