import json
import requests
from lxml import etree
import pymysql



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

# 提取数据
def get_html_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    info = []
    for url in urls:
        res = requests.get(url=url, headers=headers)
        html = etree.HTML(res.text)
        item = []
        title = get_first_text(html.xpath('//*[@id="content"]/h1/span[1]/text()'))
        year = get_first_text(html.xpath('//*[@id="content"]/h1/span[2]/text()'))
        poster = get_first_text(html.xpath('//*[@id="mainpic"]/a/img/@src'))
        dictor = get_first_text(html.xpath('//*[@id="info"]/span[1]/span[2]/a/text()'))
        dictor_src = get_first_text(html.xpath('//*[@id="info"]/span[1]/span[2]/a/@href'))
        screenwriter = get_first_text(html.xpath('//*[@id="info"]/span[2]/span[2]/a/text()'))
        screenwriter_src = get_first_text(html.xpath('//*[@id="info"]/span[2]/span[2]/a/@href'))

        # 以下是获取所有主演的名单
        # attrs = html.xpath('//*[@id="info"]/span[3]/span[2]/a')
        # attror_arr = []
        # for attr in attrs:
        #     attr_name = get_first_text(attr.xpath('./text()'))
        #     print(attr_name)
        #     attror_arr.append(attr_name)

        movie_type1 = get_first_text(html.xpath('//*[@id="info"]/span[5]/text()'))
        movie_type2 = get_first_text(html.xpath('//*[@id="info"]/span[6]/text()'))
        movie_type3 = get_first_text(html.xpath('//*[@id="info"]/span[7]/text()'))
        production_area = get_first_text(html.xpath('//*[@id="info"]/text()[3]'))
        language = get_first_text(html.xpath('//*[@id="info"]/text()[4]'))
        # show_time = get_first_text(html.xpath('//*[@id="info"]/span[11]/text()'))
        show_time = get_first_text(html.xpath('//*[@id="info"]/span[11]/text()'))
        movie_time = get_first_text(html.xpath('//*[@id="info"]/span[13]/text()'))
        alias = get_first_text(html.xpath('//*[@id="info"]/text()[5]/text()'))

        print(title,year,poster,dictor,dictor_src,screenwriter,screenwriter_src,movie_type1,movie_type2,movie_type3,
            production_area,language,show_time,movie_time,alias
        )

get_html_data()