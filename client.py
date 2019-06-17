import socket
import time

class Client:
    def __init__(self, server, port):
        # 创建socket
        # 指定IPv4协议（AF_INET），IPv6协议请使用AF_INET6
        # 指定使用TCP协议（SOCK_STREAM），UDP协议请使用SOCK_DGRAM
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务器
        self.s.connect((server, port))

    # 以下是在终端中使用的方法
    def receive_msg(self):
        data = self.s.recv(1024).decode('utf-8')  # 每次接收1KB
        if data == 'exit':
            return 'exit'
        if data:
            print("\n【人工智障聊天机器人】" + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            print(data)
            return True
        return False

    def send_msg(self):
        print('\n请输入对话: ', end='')
        message = input()
        self.s.sendall(message.encode('utf-8'))

    def chat(self):
        data = self.s.recv(1024).decode('utf-8')  # 每次接收1KB
        print(data)
        self.send_msg()
        while True:
            rec = self.receive_msg()
            if rec == 'exit':
                self.s.close()
                print('聊天服务器断开连接')
                break
            if rec:
                self.send_msg()

    # 以下是为 Qt5 图形界面新增的方法
    # 判断socket连接是否关闭
    def isClose(self):
        try:
            test = self.s.recv(1024).decode('utf-8')
            if not test:
                return True
        except OSError:
            return True
        return False

    # 关闭与服务器的连接
    def closeSocket(self):
        self.s.sendall('exit'.encode('utf-8'))
        while True:
            rec = self.receive_msg()
            if rec == 'exit':
                self.s.close()
                print('与聊天服务器断开连接')
                break

    # 强制关闭Socket
    def force_close(self):
        try:
            self.s.sendall('force_exit'.encode('utf-8'))
            print('断开连接')
        except OSError:
            print('当前没有连接服务器')
        self.s.close()

    # 在Qt5界面中发送消息
    def send_msg_gui(self, message):
        try:
            self.s.sendall(message.encode('utf-8'))
            print('消息', '\"' + message + '\"', '已发送')
        except OSError:
            print('与服务器意外断开连接')

    # 在Qt5界面中接收服务器发来的回复
    # 异步接收消息方法, 默认不启用
    # def rec_msg_gui(self):
    #     while True:
    #         try:
    #             res = self.s.recv(1024).decode('utf-8')
    #             if res == 'exit':
    #                 self.s.close()
    #                 return 'exit'
    #             if not res:
    #                 return '与服务器意外断开连接'
    #             else:
    #                 return res
    #         except OSError:
    #             return '与服务器意外断开连接'

    # 在Qt5界面中接收服务器发来的回复
    # 配合QThread多线程对象使用的同步方法
    def rec_msg_thread(self) -> str:
        try:
            res = self.s.recv(1024).decode('utf-8')
            if res == 'exit':
                self.s.close()
                return '与服务器断开连接'
            if not res:
                return '与服务器意外断开连接'
            elif res:
                return res
        except OSError:
            return '与服务器意外断开连接'

if __name__ == '__main__':
    client = Client(server='127.0.0.1', port=8000)
    client.chat()