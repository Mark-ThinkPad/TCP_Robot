import sys
import time
from server import Server
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QMessageBox,
                             QPushButton, QLineEdit, QTextBrowser, QColorDialog,
                             QFontDialog)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor

class Robot(QWidget):
    def __init__(self):
        # 建立服务端对象
        self.server = Server(server='127.0.0.1', port=8000)
        # 父级初始化
        super().__init__()
        # 初始化自定义UI
        self.initUI()

    def initUI(self):
        # 聊天输入框
        self.chatInput = QLineEdit(self)
        self.chatInput.setGeometry(QRect(10, 522, 281, 41))
        # 设置左上对齐
        self.chatInput.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # 设置回车键事件, 按下回车键直接发送消息
        self.chatInput.returnPressed.connect(self.SendMsg)

        # 发送按钮
        self.send = QPushButton('发送消息', self)
        self.send.setGeometry(QRect(210, 570, 80, 23))
        self.send.setToolTip('向客户端发送消息')
        self.send.clicked.connect(self.SendMsg)

        # 强制下线按钮
        self.exit = QPushButton('强制下线', self)
        self.exit.setGeometry(QRect(10, 570, 80, 23))
        self.exit.setToolTip('强制下线服务器')
        self.exit.clicked.connect(self.Disconnect)

        # 重启服务按钮
        self.reconnect = QPushButton('重启服务', self)
        self.reconnect.setGeometry(QRect(100, 570, 80, 23))
        self.reconnect.setToolTip('重新启动服务器')
        self.reconnect.clicked.connect(self.Reconnect)

        # 聊天内容显示区域
        self.display = QTextBrowser(self)
        self.display.setGeometry(QRect(10, 10, 281, 441))

        # 设置聊天背景颜色的按钮
        self.color = QPushButton('更换背景颜色', self)
        self.color.setGeometry(QRect(10, 460, 80, 23))
        self.color.setToolTip('更换当前聊天区域的背景颜色')
        self.color.clicked.connect(self.SetColor)

        # 更改聊天字体的按钮
        self.font = QPushButton('更换字体', self)
        self.font.setGeometry(QRect(10, 490, 80, 23))
        self.font.setToolTip('更改当前聊天字体')
        self.font.clicked.connect(self.SetFont)

        # 夜间模式按钮
        self.night = QPushButton('夜间模式', self)
        self.night.setGeometry(QRect(210, 460, 80, 23))
        self.night.setToolTip('开启夜间模式')
        self.night.clicked.connect(self.Night)

        # 日间模式按钮
        self.day = QPushButton('日间模式', self)
        self.day.setGeometry(QRect(210, 490, 80, 23))
        self.day.setToolTip('开启日间模式')
        self.day.clicked.connect(self.Day)

        # 启动服务按钮
        self.start = QPushButton('启动服务', self)
        self.start.setGeometry(QRect(110, 490, 80, 23))
        self.start.setToolTip('启动聊天服务器')
        self.start.clicked.connect(self.Start)

        # 设置固定的窗口尺寸
        self.setFixedSize(300, 600)
        # 自定义的窗口显示在屏幕中心的方法
        self.center()
        # 设置窗口标题
        self.setWindowTitle('Robot')
        # 显示在屏幕上
        self.show()

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 重写 closeEvent() 事件处理程序, 在关闭窗口的时候添加确认框
    # 如果关闭QWidget，就会产生一个QCloseEvent。改变控件的默认行为，就是替换掉默认的事件处理
    def closeEvent(self, event):
        # 我们创建了一个消息框，上面有两个按钮：Yes和No
        # 第一个字符串显示在消息框的标题栏，第二个字符串显示在对话框
        # 第三个参数是消息框的俩按钮，最后一个参数是默认按钮，这个按钮是默认选中的。返回值在变量reply里
        reply = QMessageBox.question(self, '消息', "你确定是否关闭此程序?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 强制关闭服务端的Socket
            self.server.s.close()
            self.display.append('退出服务端(后台)')
            event.accept()
        else:
            event.ignore()

    # 重写事件处理器函数keyPressEvent()
    # 自定义Esc键为退出程序
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def Disconnect(self):
        # 强制关闭服务端socket
        self.server.s.close()
        print('服务端已下线')
        self.display.append('服务端已下线')

    def Reconnect(self):
        # 先强制关闭服务端socket
        self.server.s.close()
        # 再重新建立一个服务端对象
        self.server = Server(server='127.0.0.1', port=8000)
        self.display.append('重启服务端成功\n')
        print('重启服务端成功')

    def SetColor(self):
        # 弹出一个 QColorDialog 对话框, 选择颜色
        color = QColorDialog.getColor()
        # 我们可以预览颜色，如果点击取消按钮，没有颜色值返回，如果颜色是我们想要的，就从取色框里选择这个颜色
        if color.isValid():
            self.display.setStyleSheet("QWidget { background-color: %s }" % color.name())
            self.display.append('设置颜色为' + str(color.name()))

    def Night(self):
        color = QColor(51, 51, 51)
        if color.isValid():
            self.setStyleSheet("QWidget { background-color: %s }" % color.name())
            self.display.append('已切换为夜间模式')

    def Day(self):
        self.setStyleSheet("QWidget { background-color: window }")
        self.display.append('已切换为日间模式')

    def SetFont(self):
        # 创建了一个有一个按钮和一个标签的QFontDialog的对话框, 我们可以使用这个功能修改字体样式
        # 弹出一个字体选择对话框, getFont()方法返回一个字体名称和状态信息。状态信息有OK和其他两种
        font, ok = QFontDialog.getFont()
        # 如果点击OK, 标签的字体就会随之更改
        if ok:
            self.chatInput.setFont(font)
            self.display.setFont(font)

    def Start(self):
        self.server.run()

    def SendMsg(self):
        message = self.chatInput.text()
        # if message:
        #     self.display.append("【我】" + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n' + message + '\n')
        #     self.client.send_msg_gui(message)
        #     # 发送后清空输入栏
        #     self.chatInput.setText('')
        #     # 刷新消息
        #     self.ReceiveMsg()
        # else:
        #     QMessageBox.warning(self, '警告', '未输入任何消息')

    def ReceiveMsg(self):
        # res = self.client.rec_msg_gui()
        # if res == 'exit':
        #     self.display.append('与服务器断开连接')
        #     return
        # if res == '与服务器意外断开连接':
        #     self.display.append('与服务器意外断开连接')
        #     return
        # if res:
        #     self.display.append("【人工智障聊天机器人】" + " " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n' + res + '\n')
        pass

if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    robot = Robot()
    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())