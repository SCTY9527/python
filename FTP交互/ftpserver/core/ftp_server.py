#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = '单人行'

import socketserver
import json,os,sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

class MyTCPHandler(socketserver.BaseRequestHandler):
    def put(self,*args):
        """
        客户端上传文件到服务端
        获取指令、文件名、文件大小
        接收文件
        """
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        filesize = cmd_dic["size"]
        print("filesize:",filesize)
        if os.path.isfile(filename):
            f = open(filename + ".new","wb")
        else:
            f = open(filename,"wb")
        self.request.send(b"ready accept...")  # 5、发送准备好接受文件，防止粘包
        receive_size = 0
        while receive_size < filesize:
            data = self.request.recv(1024)  # 6、接收文件
            f.write(data)
            receive_size += len(data)
        else:
            print("file [%s] has uploaded..." % filename)

    def get(self,*args):
        """
        客户端从服务端下载文件，
        获取客户端的指令：命令和文件
        判断文件是否存在并发送文件大小
        发送文件给客户端
        """
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        if os.path.isfile(filename):
            self.request.send(b'yes')  # 5、发送文件是否存在
            filesize = os.stat(filename).st_size
            print(filesize)
            self.request.send(str(filesize).encode())  # 6、发送文件大小
            f = open(filename,"rb")
            for line in f:
                self.request.send(line)  ## 7、发送文件
            else:
                print("file send success...")
                f.close()
        else:
            print("file in not exist...")
            self.request.send(b'no')

    def func_call(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()  # 4、接受用户指令
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                cmd_dic = json.loads(self.data.decode())
                action = cmd_dic["action"]
                if hasattr(self,action):   # 利用反射根据客户端的命令调用相应功能
                    func = getattr(self,action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print("error:",e)
                break


    def handle(self):
        # 用户验证
        user_name = self.request.recv(1024).decode()  #1、接受用户名
        if os.path.isfile(BASE_DIR + '/accounts/' + user_name +'.json'):
            with open(BASE_DIR + '/accounts/' + user_name +'.json') as f:
                user_info = json.loads(f.read())
                user_pass = self.request.recv(1024).decode()  # 2、接受用户密码
                if user_pass == user_info["password"]:
                    print("用户%s登录成功..."%user_name)
                    self.request.send(b"yes")  # 3、发送用户是否登陆成功
                    self.func_call()
                else:
                    print("密码错误，用户登录失败...")
                    self.request.send(b"no")  # 3、。。。
        else:
            print("用户不存在...")
            self.request.send(b"no")

def server_start():
    if __name__ == "__main__":
        HOST,PORT = "localhost", 9999
        server = socketserver.ThreadingTCPServer((HOST,PORT), MyTCPHandler)
        server.serve_forever()