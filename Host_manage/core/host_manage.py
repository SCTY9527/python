#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = '单人行'

import os
import paramiko
import threading
import sys,time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from conf import settings

class REMOTE_HOST(object):
    def __init__(self,host,port,username,password,cmd):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.cmd = cmd

    def run(self):
        cmd_str = self.cmd.split()[0]
        if hasattr(self,cmd_str):
            getattr(self,cmd_str)()
        else:
            setattr(self,cmd_str,self.command)
            getattr(self,cmd_str)()

    def command(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
        stdin, stdout, stderr = ssh.exec_command(self.cmd)
        res,err = stdout.read(),stderr.read()
        result = res if res else err
        print("%s".center(40, "-") % self.host)
        print(result.decode())
        ssh.close()

    def put(self):
        file_name = self.cmd.split()[1]
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(file_name, file_name)
        print("send success...")
        transport.close()

def show_iplist():
    for key in settings.msg_dic:
        print(key)
    while True:
        choose_group = input(">>>:(eg:group1)")
        while True:
            host_dic = settings.msg_dic[choose_group]
            cmd = input("请输入指令(enter b break):").strip()
            if cmd == "break":
                break
            else:
                thread_list = []
                for key in host_dic:
                    print(host_dic[key]["IP"])
                    host,port = host_dic[key]["IP"],host_dic[key]["port"]
                    username,password = host_dic[key]["username"],host_dic[key]["password"]
                    func = REMOTE_HOST(host,port,username,password,cmd)
                    t = threading.Thread(target=func.run)
                    t.start()
                    thread_list.append(t)
                for i in thread_list:
                    i.join()