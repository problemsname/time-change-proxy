#!/usr/bin/env python
# coding=utf-8
from module import getproxy_ip

proxy_pool_url = "http://localhost:5555/random"
test_target = "http://www.baidu.com"
# 代理池URL 代理测试可用性URL
proxy_filename = "proxylist.txt"
# proxy save to the file name 
proxyNumber = 20
# proxy 数量 默认为 20 

poolOBJ = getproxy_ip.get_proxypool_ip(proxy_pool_url, test_target)

file_c = open(proxy_filename,'w')

for i in range(proxyNumber):
    ip, port = poolOBJ.Loadips()
    file_c.writelines(ip+":"+str(port)+"\n")

file_c.close()