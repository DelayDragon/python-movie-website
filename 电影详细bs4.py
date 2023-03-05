import pymysql
from bs4 import BeautifulSoup
import urllib.request
import re
from utils.index import get_number_zero




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
    for (i,) in cursor.fetchmany(10):
        arr.append(i)
    db.close()
    return arr

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
    array = getMovieId()
    # urls = ['https://movie.douban.com/subject/{}'.format(str(i)) for i in array]
    for i in array:
        url = 'https://movie.douban.com/subject/{}'.format(str(i))
        
    # for url in urls:
        item = []
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

        # 制片国家/地区 未获取
 

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

        # 豆瓣评分
        # score = soup.select('strong[property="v:average"]')[0].string
        # print(score)

        # 评价人数
        # comment = soup.find(property="v:votes").text
        # print(comment)

        # 剧情简介
        # plot = soup.select('span[property="v:summary"]')[0].text
        # print(plot.strip())




        # 电影名字
        movie_name = soup.select('span[property="v:itemreviewed"]')[0].text
        # print(movie_name)

        # 电影年份
        movie_year = soup.select('span[class="year"]')[0].text
        # print(movie_year)

        # 电影海报
        movie_poster = soup.select('a[class="nbgnbg"] > img')[0]['src']
        # print(movie_poster)

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
        item.append(movie_poster)
        item.append(movie_score)
        item.append(movie_comment)
        item.append(movie_attributes)
        item.append(movie_plot)
        item.append(movie_id)
        info.append(item)

    print(info)
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
    cursor.execute("DROP TABLE IF EXISTS movie_details")

    sql = """CREATE TABLE movie_details (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        movie_name VARCHAR(255),
        movie_year VARCHAR(255),
        movie_postor VARCHAR(255),
        movie_score VARCHAR(255),
        movie_comment VARCHAR(255),
        movie_attributes VARCHAR(1000),
        movie_plot VARCHAR(1000),
        movie_id varchar(255)
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
    sql = 'INSERT INTO movie_details(movie_name,movie_year,movie_postor,movie_score,movie_comment,movie_attributes,movie_plot,movie_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'   
    try:
        cursor.executemany(sql,values)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print('插入数据失败')
    db.close()


create()

info = get_html_data()
# print(info)
insert(info)
