# 导入米快
import requests # 网络请求模块
from lxml import etree # 数据解析模块

# 发起网络请求
urls = ['https://movie.douban.com/top250?start={}&filter='.format(str(i * 25)) for i in range(10)]
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# 功能函数，获取列表的第一个元素，去除空格，遇空返空
def get_first_text(list):
    try:
        return list[0].strip()
    except:
        return ''

import pandas as pd 
df = pd.DataFrame(columns = ['序号','标题','链接','导演','评分','评价人数','简介'])

# 解析数据
count = 1
for url in urls:
    res = requests.get(url = url, headers = headers) # 发起请求
    html = etree.HTML(res.text) # 将返回的文本加工为可以解析的html
    lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li') # 获取每个电影的li元素
    
    for li in lis : 
        title = get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()')) # 电影标题
        src = get_first_text(li.xpath('./div/div[2]/div[1]/a/@href')) # 电影链接
        dictor = get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()')) # 导演
        score = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()')) # 评分
        comment = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()')) # 评价人数
        summary = get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()')) # 电影简介
        print(count, title,src,dictor,score,comment,summary) # 输出
        df.loc[len(df.index)] = [count, title,src,dictor,score,comment,summary]
        count = count + 1

# 处理数据

df.to_excel('豆瓣电影top250.xlsx', sheet_name='豆瓣电影top250数据', na_rep="")
