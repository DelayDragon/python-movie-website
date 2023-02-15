import requests
from lxml import etree

def get_first_text(list):
    try:
        return list[0].strip()
    except:
        return ''
i = 1292052
urls = ['https://movie.douban.com/subject/{}'.format(str(i)) for i in range(1292052, 1292054)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
count = 1
for url in urls:
    res = requests.get(url=url, headers=headers)
    html = etree.HTML(res.text)
    title = get_first_text(html.xpath('//*[@id="content"]/h1/span[1]/text()'))
    # years = get_first_text(html.xpath('//*[@id="content"]/h1/span[2]/text()'))
    if title != '' :
        print(count, title)
        count = count + 1
    else:
        print(count)
        count = count + 1

# array = ['{}'.format(str(i * 25)) for i in range(10)]

# for arr in array:
#     print(arr)
# urls = [
# 'https://movie.douban.com/top250?start={}&filter='.format(str(i * 25)) for i in range(10)]
# for url in urls:
#     print(url)