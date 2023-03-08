import urllib.request
import concurrent.futures



# 测试代理
def test_proxy(proxy):
    try:
        proxy_handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_handler)
        response = opener.open('https://movie.douban.com/', timeout=5)
        print(proxy + 'ip地址有效！')
        return True
    except:
        print(proxy + 'ip地址无效！')
        return False

# 实现多线程测试ip地址池的有效性
def test_proxy_list(proxy_list):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(test_proxy, proxy) for proxy in proxy_list]
        for future, proxy in zip(futures, proxy_list):
            if future.result():
                results.append(proxy)
    return results