import socket 
import threading 
import time

#套接字缓冲区大小
PKT_BUFF_SIZR = 1024 
# IP更换时间 默认为30秒 更换实际根据请求频率
CHANGE_TIME = 30


class create_proxy_connect:
    """
        2020年 10月 07日 星期三 14:39:17 CST
        模块tcp connect 链接到http 代理
        建立与本地监听模块的信息交换
        多线程获得本地连接
        多线程数据交换 
        
        暂时使用Thread 类的构造方法创建线程 后续扩展可以考虑继承Thread 类
        以获得对线程的操作
        这里简化实现不对sqlmap假设为并发请求
        
        2020年 10月 07日 星期三 22:23:35 CST
            基本能够实现但是速度太慢 
            对抛出异常位置重写使其能够 重新设置代理IP
            抛出异常位置其中send2target 方法为正常抛出异常 之后中断该TCP
            建立的TCP 不是面向连接 
            


    """
    
    def __init__(self, lhost, lport,proxyHost, proxyPort):
        self.lhost = lhost
        self.lport = lport
        self.proxyHost = proxyHost
        self.proxyPort = proxyPort

        
        
    def __create_socket(self, conn_host, conn_port,conn_type=1):
        """
            方法功能接收一个类型参数 0 为远程连接 1为本地连接 (default 1)
            连接的端口与地址
            返回建立连接的对象
        """
        conn_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #创建一个socket 对象
        if conn_type:
            try :
                conn_socket.bind((conn_host,conn_port))
                #开启监听 注意是一个元组
                conn_socket.listen(5)
                #不是的最大链接数量 可以链接的数量为 线程数+5 
            except Exception as exception:
                print( "binf local addr error: code=0x005 ",end="")
                #绑定本地地址失败
                print(exception)
                exit(-1) 
        else:
            try:
                conn_socket.connect((conn_host,conn_port))
            except Exception as exception :
                print(exception)
                print("create connect remote error: code=0x006")
                return False
        return conn_socket

    def create_local2remote(self,poolOBJ):
        """
            在本地监听一个地址返回监听对象 
        """
        flag_change = int(time.time())
        #时间戳初始化
        local_socket = self.__create_socket(self.lhost, self.lport, conn_type=1)
        if local_socket is False:
            exit(-1)
        print("start bind >>> " + self.lhost + ":"+str(self.lport))
        proxyHost = self.proxyHost
        proxyPort = self.proxyPort
        while True:
            # 建立本地链接
            if int(time.time()) - flag_change >= CHANGE_TIME:
                #设置更改IP时间 
                flag_change = int(time.time())
                proxyHost, proxyPort = poolOBJ.Loadips()

            local_conn, local_addr = local_socket.accept()

            #将每一个本地建立的链接 都与代理建立双向通信首先需要一个远程的连接对象
            threading.Thread(target=create_proxy_connect.create_remote_connect, args=(self,local_conn,proxyHost,proxyPort)).start()


    def create_remote_connect(self, local_conn, proxyHost, proxyPort):
        """
            在本地连接到达后 建立一个remote_proxy 连接并在另一个线程中实现交互
            考虑将本地连接与一个远程连接相当于一个远程端口转发 
            可以考虑将这个模块单独实现端口转发功能 
        """
        remote_conn = self.__create_socket(proxyHost, proxyPort, conn_type=0)
        if remote_conn is False:
            #proxy 建立连接失败  是否考虑重新建立还是重新获取一个IP 这里直接中断程序
            # 因为网络环境无法建立还是其他原因未可知以及重新获取IP 速度太慢
            exit(-3)
        #创建多个套接字
        # 拥有两者地址 多线程实现双向通信 
        threading.Thread(target=create_proxy_connect.send2target, args=(self,local_conn, remote_conn)).start()
        print( " >> "+proxyHost+":"+str(proxyPort))
        threading.Thread(target=create_proxy_connect.send2target, args=(self,remote_conn, local_conn)).start()
        print( " << "+proxyHost+":"+str(proxyPort))
        # 这里并不结束TCP连接 而是在线程中
        
        
    def send2target(self, sender_conn, receive_conn):
        """
            方法建立一个单项数据流 
            sender_conn连接将数据发送到receive_conn
            先接收数据将之后转发 
            recv()接收指定缓冲区大小的数据
        """
        while True:
            try :
                data = sender_conn.recv(PKT_BUFF_SIZR)
            except Exception as exception:
                print( "send2target: coode = 0x001")
                print(exception)
                break 
            #data为空或者exit 表示数据接收完毕可以关闭套接字
            if not data or data=="exit":
                print( "send2target: coode = 0x000 send all")
                break
            
            try :
                receive_conn.sendall(data)
    
            except Exception as exception:
                print( "send2target: coode = 0x003")
                print(exception)
                break 
            #关闭套接字连接
        sender_conn.close()
        receive_conn.close()    

    
    
