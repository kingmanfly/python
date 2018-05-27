from urllib import request

def use_proxy(proxy_addr, url):
    proxy = request.ProxyHandler({'http': proxy_addr})
    opener = request.build_opener(proxy, request.HTTPHandler)
    request.install_opener(opener)  #系统都会被修改掉
    data = request.urlopen(url).read().decode('utf-8')
    return data

proxy_addr = '218.20.55.34:9797'
data = use_proxy(proxy_addr, "http://www.baidu.com")
print(len(data))