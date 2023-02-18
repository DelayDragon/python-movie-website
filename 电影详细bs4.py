import json
import requests
from lxml import etree
import pymysql
from bs4 import BeautifulSoup
import urllib.request
import re



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
urls = ['https://movie.douban.com/subject/{}'.format(str(i)) for i in array]
print(urls)

# 功能函数，获取列表的第一个元素，去除空格，遇空返空
def get_first_text(list):
    try:
        return list[0].strip()
    except:
        return ''

# 得到链接中的数字编号
def get_number(value):
    number = re.compile(r'\d+').findall(value)[0]
    return number

# 提取数据
def get_html_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    info = []
    for url in urls:
        # res = requests.get(url=url, headers=headers)
        # html = etree.HTML(res.text)
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        
        soup = BeautifulSoup(content, 'lxml')

        # 导演 # 导演编号
        # director = soup.select('#info > span')[0].select('span[class="attrs"] > a')[0].string
        # director_number = get_number(soup.select('#info > span')[0].select('span[class="attrs"] > a')[0]['href'])
        # print(director,director_number)

        # 编剧 # 编剧编号
        # screenwriter_list = soup.select('#info > span')[1].select('span[class="attrs"] > a')
        # for screenwriter in screenwriter_list:
        #     screenwriter_number = re.compile(r'\d+').findall(screenwriter['href'])[0]
        #     print(screenwriter.string,screenwriter_number)

        # 主演 # 主演演员编号
        # actor_list = soup.select('#info > span[class="actor"] > span[class="attrs"] > a')
        # for actor in actor_list:

        #     actor_number = re.compile(r'\d+').findall(actor['href'])[0]
        #     print(actor.string,actor_number)


        # 电影类型
        # movie_type = soup.select('span[property="v:genre"]')
        # for type in movie_type:
        #     print(type.string)

        # 制片国家/地区
        movie_country = soup.select('div[id="info"]')[0].string
        # movie_country = soup.select('div[id="info"]')[0]
        print(movie_country)

        # 语言
        # language = soup.select('#info')[0]
        # print(language)
        
        # 上映时间
        # showtime_list = soup.select('span[property="v:initialReleaseDate"]')
        # for name in showtime_list:
        #     print(name.string)

        # 片长
        # movie_time = soup.select('span[property="v:runtime"]')[0].string
        # print(movie_time)

        # 官方网站
        # offical_website = soup.select('#info > a[rel="nofollow"]')
        # if len(offical_website) == 0:
        #     return offical_website
        # else:
        #     offical_website = offical_website[0].string
        # print(offical_website)

        # 剧情简介
        # plot = soup.select('span[property="v:summary"]')
        # print(plot)
get_html_data()