#!/bin/python3 
"""
2020年 10月 07日 星期三 13:15:27 CST
本地的一个自动代理切换工具重写
模块:自动获得一个IP保证其可用性
    模块需要的参数为代理池地址以及测试URL 
    该模块仅将内容为 <IP>:<port> 内容判断并返回
    Loadips()方法返回一个可用IP 获取格式 proxyip, port = obj.Loadips()


"""


import requests 

class get_proxypool_ip:

    """
        作用对象参数为代理池地址以及需要测试的目标测试可用性
        类支持接收单个IP并测试其可用性
        Loadips 函数返回一个可用IP 
    """

    def __init__ (self, proxypool_url, target_url):
        self.proxypool_url = proxypool_url
        self.target_url = target_url

        
    def target_test(self, target, proxyip):
        #target 为目标测试IP是否可用的连接
        #proxyip 格式ip:port 
        proxies = {"http":"http://"+proxyip,"https":"https://" + proxyip}
        try :
            r = requests.get(target,proxies=proxies,timeout=3)
        except Exception:
            return False
        if r.status_code == 200:
            print("有效:"+proxyip)
            return True
        print("IP 无效",proxyip)
        return False
    
    def __get_proxyip(self, proxypool_url):
        #获取代理ip 默认由localhost:5555/random端口获取
        r = requests.get(proxypool_url)
        if r.status_code == 200:
            ip = r.text
            return ip
        return False 
    
    
    def Loadips(self):
        """
        加载ips.txt 文件读取全部IP作为代理池
        缺点：文件读取后无法进行动态添加
        没有验证IP是否可用以及后续继续更换问题
        修改为请求URL获取IP之后 测试IP 不可用继续请求URL更换
        
            流程:
                首先请求代理池获取IP
                测试IP是否可以访问目标
                不可以继续请求 
                成功则返回该ip
        """
        ip = ""
        while True:
            ip = self.__get_proxyip(self.proxypool_url)
            if ip is None:
                continue
            if self.target_test(self.target_url,ip):
                break
        return  ip.split(":")[0], int(ip.split(":")[1])
 

