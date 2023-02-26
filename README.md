# python-movie-website
### 爬虫douban电影信息
## 简述
这是一个python实现的爬虫，目标网址是douban电影；（编写中）
其中包含了：
（1）douban电影top250的信息（海报、片名、导演、主演、评分、评分人数、电影简述）；
（2）douban电影主页中的最近热门电影栏中的所有tag；
（3）对应的每个tag的500条电影信息（主要信息爬取：海报、片名、评分）；
（4）整合所有tag对应的电影条目，去重后大概有3000条电影信息；
（5）每部电影的详细的信息爬取（片名、海报、年份、导演、主演、评分等）；
（6）职员的信息爬取（名字、照片、基本信息、简介等）；

## 详细

## 注意
  爬取的方式上有xpath和bs4，主要是因为两种方式各有千秋，xpath在性能和速度方面的体验是非常不错的，但是在某些情况下，没有好的爬取方案，无法爬取到想要的信息；这时候我转战bs4，bs4的写法上来说很贴近css，更加通俗易懂，使得我很快就上手了，并使用起来比较顺手，对于信息爬取的方案的思考都是比较有帮助的，通过一些时间的积累，我基本上爬取到了我想要的一些信息；
