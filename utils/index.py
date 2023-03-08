import re
import requests



# 得到链接中的数字编号
def get_number_first(value):
    number = re.compile(r'\d+').findall(value)[1]
    return number

# 得到链接中的第一个数字编号
def get_number_zero(value):
    number = re.compile(r'\d+').findall(value)[0]
    return number


def parse(html):
    # 利用正则表达式 解析并获取页面中所有IP地址
    ip_list = re.findall(
        r'(?<![\.\d])(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?![\.\d])',
        html)
    return ip_list

def test(ip, port):
    # 如果代理成功 则页面解析获取的IP应当与输入IP相同
    # True 代理成功 False代理失败
    print('开始测试' + str(ip) + '...')
    url = 'http://httpbin.org/ip'
    proxies = {"http": f"http://{ip}:{port}", "https": f"http://{ip}:{port}"}
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33'
    }
    html = requests.get(url=url, headers=headers, data=None, proxies=proxies)
    if html == "GET异常":
        return False
    return parse(html)[0] == ip

def test_list(ip_dic):
    ip_list = list(ip_dic.keys())
    for num in range(len(ip_list)):
        if test(ip_list[num], ip_dic[ip_list[num]]):
            print(str(ip_list[num]) + '有效')
        else:
            print(str(ip_list[num]) + '无效')
            ip_dic.pop(ip_list[num])
    return ip_dic
