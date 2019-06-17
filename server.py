import socket
import threading
import time

# 沙雕回复语料库
keywords = {'你是谁': '我是人工智障聊天机器人',
            '今天天气如何': '荆州的天气可说不准呢',
            '现在几点': '不要逗我了, 你电脑的任务栏上一眼就可以看到时间',
            '吃饭了吗': '吃吃吃就知道吃',
            '你昨天几点睡的': '真正的强者不需要睡觉',
            '阿米娅是兔子还是驴': '是驴',
            '我想睡觉': 'Doctor, 您现在还不能休息呢',
            '奥尔加团长': '不要停下来啊',
            'PHP': 'PHP是世界上最好的语言',
            'Python': 'Python可能是世界上最好......学的语言',
            'CSS': '天下苦CSS久矣',
            '关机': '本人工智障暂时没有执行 shutdown now 的权限',
            }

class Server:
    def __init__(self, server, port):
        # 创建socket
        # 指定IPv4协议（AF_INET），IPv6协议请使用AF_INET6
        # 指定使用TCP协议（SOCK_STREAM），UDP协议请使用SOCK_DGRAM
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定ip和port
        # 绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。
        self.s.bind((server, port))
        # 监听端口
        # 指定等待连接的最大数量
        self.s.listen(5)
        # 输出
        print('正在监听 ' + server + ':' + str(port))

    def chat(self, c, addr):
        c.sendall('你好, 人工智障聊天机器人为您服务, 输入 exit 即可退出聊天'.encode('utf-8'))
        while True:
            try:
                data = c.recv(1024).decode('utf-8')
            except ConnectionResetError:
                c.close()
                print(addr, '意外断开\n')
                break
            if data == 'exit':
                c.sendall('exit'.encode('utf-8'))
                c.close()
                print('与', addr, '结束对话\n')
                break
            if data == 'force_exit':
                c.close()
                print('与', addr, '结束对话\n')
                break
            if data:
                print('来自', addr, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '的消息:', data)
                if data in keywords:
                    c.sendall(keywords[data].encode('utf-8'))
                else:
                    # 复读机模式
                    # res = data
                    # 人工回复模式
                    print('请输入回复:', end='')
                    res = input()
                    c.sendall(res.encode('utf-8'))

    def run(self):
        # 接收数据
        while True:
            # 接受一个新连接，阻塞的，只有接收到新连接才会往下走
            # s.accept(), 接受TCP链接并返回（conn, address），其中conn是新的套接字对象，可以用来接收和发送数据，address是链接客户端的地址
            c, addr = self.s.accept()
            print('连接地址:', addr)
            # 每一次连接，都要创建新线程，否则一次只能处理一个连接
            t = threading.Thread(target=self.chat(c, addr))
            t.start()

if __name__ == '__main__':
    server = Server(server='127.0.0.1', port=8000)
    server.run()