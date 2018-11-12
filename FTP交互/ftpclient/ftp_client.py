#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = '单人行'

import socket,os,json

class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()

    def help(self):
        msg ="""
        ls
        pwd
        cd
        get filename
        put filename
        """
        print(msg)

    def connect(self,ip,port):
        self.client.connect((ip,port))

    def user_login(self):
        # 用户登录
        user_name = input("请输入用户名:").strip()
        pass_word = input("请输入用户密码:").strip()
        self.client.send(str(user_name).encode()) # 1、传输账户
        self.client.send(str(pass_word).encode()) # 2、传输密码
        yes_no = self.client.recv(1024).decode()  # 3、接受用户是否登陆成功
        if yes_no == "yes":
            print("用户登录成功...")
            self.interactive()
        else:
            print("用户登录失败...")

    def interactive(self):
        # 客户端和服务带交互开始并调用相应功能
        while True:
            cmd = input(">>:").strip()
            if len(cmd) == 0:
                continue
            cmd_str = cmd.split()[0]
            if hasattr(self,"cmd_%s"%cmd_str):
                func = getattr(self,"cmd_%s"%cmd_str)
                func(cmd)
            else:
                self.help()

    def cmd_put(self,*args):
        """
        客户端上传文件
        判断文件是否存在并发送文件信息
        打开文件并发送文件到服务端
        """
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                file_size = os.stat(filename).st_size
                msg_dic = {
                    "action": "put",
                    "filename":filename,
                    "size": file_size,
                    "overridden":True
                }
                self.client.send(json.dumps(msg_dic).encode())  # 4、发送指令
                print("send",json.dumps(msg_dic).encode("utf-8"))
                f = open(filename,"rb")
                for line in f:
                    self.client.send(line)  # 5、发送文件
                else:
                    print("file upload success...")
                    f.close()
            else:
                print(filename,"is not exist")

    def cmd_get(self,*args):
        """
        客户端下载文件
        发送指令和文件名给服务端
        接受文件大小并接受文件
        """
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                f = open(filename + ".new","wb")
            else:
                msg_dic = {
                    "action":"get",
                    "filename":filename
                }
                self.client.send(json.dumps(msg_dic).encode("utf-8"))  # 4、发送指令
                print("send",json.dumps(msg_dic).encode("utf-8"))
                yes_no = self.client.recv(1024).decode()  # 5、接受服务端是否存在此文件
                if yes_no =="yes":
                    self.data = self.client.recv(1024).strip()  # 6、接受文件大小
                    filesize = int(self.data.decode())
                    print("filesize:",filesize)
                    f = open(filename,"wb")
                    receive_size = 0
                    while receive_size < filesize:
                        data = self.client.recv(1024)   # 7、接收文件
                        f.write(data)
                        receive_size += len(data)
                    else:
                            print("file [%s] has uploaded..." % filename)
                else:
                    print("服务端无此文件...")

ftp = FtpClient()
ftp.connect("localhost",9999)
ftp.user_login()