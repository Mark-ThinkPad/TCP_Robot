# 基于TCP协议的简易聊天机器人
---
## Content

<!-- TOC -->

- [基于TCP协议的简易聊天机器人](#基于tcp协议的简易聊天机器人)
    - [Content](#content)
    - [简介](#简介)
    - [文件内容](#文件内容)
    - [技术实现](#技术实现)
    - [相关资料](#相关资料)

<!-- /TOC -->
---
## 简介

- 计算机网络课程设计中的一个题目: `基于TCP协议的简易聊天机器人`
- 开发语言: `Python 3.7.3`
- 开发平台: `Manjaro Linux 18`
- 初期版本其实就是很容易搜到的现成的轮子: [教程链接](https://www.imooc.com/article/31228), 只能在终端中使用(CLI)
- 最后的完成版为客户端编写了"简陋"的图形界面(GUI), 使用了 `Qt5(PyQT5)` 实现
- 服务端的图形界面暂时无法完整实现, 因为一时无法想出把TCP连接线程中接收到的客户端消息实时刷新的方法, 后面还有两门课设如期而至, 时间紧迫, 只能暂时弃坑, 随缘更新

---
## 文件内容

- [server.py](./server.py): 服务端端核心代码, 已经抽象成类, 可以直接在终端中运行
- [robot.py](./robot.py): 没有完整实现的服务端图形界面, emmm, 看看就好
- [client.py](./client.py): 客户端核心代码, 也抽象成类, 可以在终端中直接运行
- [user.py](./user.py): 简陋的客户端图形界面, 支持更换聊天消息框的颜色和字体, 支持夜间模式, 支持一键断开连接和一键重连, 默认回车键快捷发送消息
- [/UI/](./UI/): 使用 `Qt Designer` 设计的界面布局文件, 仅用来提供各个部件的定位
- [/background/](./background/): 客户端图形界面实现过程中使用的背景图片文件, 发现设置背景图片后实际效果并不好看, 所以没有采用背景图片的方案, 但还是决定把图片保留下来, 图片来源: `Bing必应每日壁纸`

---
## 技术实现

- 最重要的其实是实现图形客户端的实时刷新消息的功能, Qt5界面中不做处理的直接使用循环可能会导致Qt主线程阻塞, 此时需要借助QThread类使实时刷新消息不阻塞Qt主线程, 同时注意与主线程之间的信号实时传递
- 其他的直接看代码注释吧, 由于是第一次接触这些东西, 所以添加了不少注释

---
## 相关资料

- [Python Socket 编程详细介绍](https://gist.github.com/kevinkindom/108ffd675cb9253f8f71)
- [Python进阶开发之网络编程,socket实现在线聊天机器人](https://www.imooc.com/article/31228)
- [PyQt5-Chinese-tutorial](https://github.com/maicss/PyQt5-Chinese-tutorial), [教程目录](https://github.com/maicss/PyQt5-Chinese-tutorial/blob/master/SUMMARY.md?1560763794372)
- PyQt5多线程的资料很容易找到, 此处不放出(其实是忘记存浏览器书签了)
- [通俗大白话来理解TCP协议的三次握手和四次分手](https://github.com/jawil/blog/issues/14)