import requests
import urllib.request
import random
from 多线程 import get_89ip_IP

# 定义IP地址池
ipPool = get_89ip_IP()
print(ipPool)

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
        print(
            f'Request to {ip} failed with error: {e}. Retrying with a different IP address...')
        send_request(url)
    else:
        # 请求成功，返回响应内容
        return response_text


test = [
    {
        'http': 'http://220.179.210.151:8089',
        'https': 'https://220.179.210.151:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://220.179.210.151:8089',
        'https': 'https://220.179.210.151:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://175.10.204.189:7890',
        'https': 'https://175.10.204.189:7890',
        'ftp': 'http://127.0.0.1:7890'},
    {
        'http': 'http://59.59.162.167:8089',
        'https': 'https://59.59.162.167:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://59.59.162.207:8089',
        'https': 'https://59.59.162.207:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://59.59.162.207:8089',
        'https': 'https://59.59.162.207:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://222.190.208.32:8089',
        'https': 'https://222.190.208.32:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://222.190.215.170:8089',
        'https': 'https://222.190.215.170:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://59.59.158.101:8089',
        'https': 'https://59.59.158.101:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://183.150.68.224:9128',
        'https': 'https://183.150.68.224:9128',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://59.59.158.101:8089',
        'https': 'https://59.59.158.101:8089',
        'ftp': 'http://127.0.0.1:7890'
    },
    {
        'http': 'http://183.150.68.224:9128',
        'https': 'https://183.150.68.224:9128',
        'ftp': 'http://127.0.0.1:7890'
    }
]


def testIpPool(url):
    info = []
    for proxy in ipPool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(
                url, headers=headers, proxies=proxy, timeout=5)
            print(response.status_code)
        except Exception as e:
            print(f"请求失败，代理IP无效！{e}")
        else:
            print("请求成功，代理IP有效！")
            info.append(proxy)
    return info


# 调用请求函数并打印响应内容
# response_text = send_request('https://movie.douban.com/')
# print(response_text)
info = testIpPool('https://movie.douban.com/')
print(info)
