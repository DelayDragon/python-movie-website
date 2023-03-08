import urllib.request
import random
from 多线程 import get_89ip_IP

# 定义IP地址池
ipPool = get_89ip_IP()

# 定义请求函数
def send_request(url):
    # 随机选择一个IP地址
    ip = random.choice(ipPool)
    print(f'Sending request to {ip}...')
    try:
        # 构建请求对象
        req = urllib.request.Request(url)
        # 添加代理
        proxy = urllib.request.ProxyHandler(ip)
        opener = urllib.request.build_opener(proxy)
        # 发起请求
        response = opener.open(url, timeout=5)
        response_text = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        # 请求失败，重新选择一个IP地址并发起请求
        print(f'Request to {ip} failed with error: {e}. Retrying with a different IP address...')
        send_request(url)
    else:
        # 请求成功，返回响应内容
        return response_text

# 调用请求函数并打印响应内容
response_text = send_request('https://movie.douban.com/')
print(response_text)