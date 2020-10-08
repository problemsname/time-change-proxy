#!/bin/python3 
from module import getproxy_ip
from core import connect_proxy


proxy_pool_url = "http://localhost:5555/random"
test_target = "https://www.baidu.com"
lhost = "127.0.0.1"
lport = 3336
#本地监听  的端口与IP
#代理池地址与需要测试代理的可用性使用的连接 

def get_proxypool(proxy_pool_url, test_target):
    poolOBJ = getproxy_ip.get_proxypool_ip(proxy_pool_url, test_target)
    return poolOBJ

def set_proxy(lhost, lport, proxyHost, proxyPort, poolOBJ):
    """
        暂时这样写 之后扩展时在优化
    """
    sock_obj = connect_proxy.create_proxy_connect(lhost, lport, proxyHost, proxyPort)
    #创建一个对象连接对象
    sock_obj.create_local2remote(poolOBJ)

if __name__ == "__main__":
    poolOBJ = get_proxypool(proxy_pool_url,test_target)
    proxyHost, proxyPort = poolOBJ.Loadips()
    set_proxy(lhost, lport, proxyHost, proxyPort, poolOBJ)
    
