import os
import requests
from utils.index import get_number
import base64


# 创建图片文件夹
def create_folder():
    folder = 'image'
    if not os.path.exists(folder):
        print('文件不存在，已创建！')
        os.mkdir(folder)
    else:
        print('开始下载图片')

def parsing_picture(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    picture_down = requests.get(url=url,headers=headers)
    with open('image/' + get_number(url) + '.jpg', mode='wb') as f:
        f.write(picture_down.content)
    with open('image/' + get_number(url) + '.jpg', mode='rb') as f:
        # 转化为二进制,并使用base64进行加密
        # base64_data = base64.b64encode(f.read())
    # return base64_data
        return f.read()


if __name__ == '__main__':
    create_folder()
    # parsing_picture('https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg')