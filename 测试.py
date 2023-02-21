import requests
from lxml import etree

from bs4 import BeautifulSoup
import urllib.request


url = 'https://movie.douban.com/subject/10047547/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

soup = BeautifulSoup(content, 'lxml')
print(soup)

res = requests.get(url=url, headers=headers) 
html = etree.HTML(res.text)
print(html)
