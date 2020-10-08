# time_change_proxy

### 30s change proxy ip

拉取代理池中的IP 测试其有效性 之后在本地监听(default) 127.0.0.1:3336 端口
通过该端口的流量将被转发到代理
注意该脚本core/connect_proxy.py 文件 建立一个TCP连接 
module/getproxy_ip.py 由代理池URL中 拉取一个IP并测试有效性 :

[代理池地址](https://github.com/Python3WebSpider/ProxyPool)


### auto_proxy.py

该文件作为一个组织module 与core 之间的配合
可以自行修改 没有友好的命令行help信息 
很多内容需要到该文件中修改 

以及connect_proxy.py 文件中设置缓冲区大小以及 更改时间
时间的更改时间是不确定的最小的更改为30秒 因为要在请求到达后解除阻塞才会判断是否修改

```
    #套接字缓冲区大小
    PKT_BUFF_SIZR = 1024 
    # IP更换时间 默认为30秒 更换实际根据请求频率
    CHANGE_TIME = 30

```


...

### USAGE 

**拉取到本地**

```
    git clone git@github.com:problemsname/time-change-proxy.git
```

**配置信息修改**

```
    #代理池地址
    proxy_pool_url = "http://localhost:5555/random"
    #测试IP是否可用URL 
    test_target = "http://myip.ipip.net/"
    #本地监听地址
    lhost = "127.0.0.1"
    lport = 3336
    
    #返回一个代理池对象 连接部分写的不好需要将对象加入到 core 中 考虑重新设计一个模块协调两者
    def get_proxypool(proxy_pool_url, test_target) return proxy_pool_obj:
    #初始化连接对象并开始建立连接
    def set_proxy(lhost, lport, proxyHost, proxyPort, poolOBJ):
```

**依赖**


- pip3 install -r requirements.txt

- or pip3 install requests 

```
#运行
    python3 auto_proxy.py
```
 
**脚本中有很多注释详细可以查看注释**


enjoy:)
