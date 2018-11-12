#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = '单人行'

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from core import ftp_server

while True:
    choice = input("是否开始服务端工作('Y'or'N'):")
    if choice == "Y":
        ftp_server.server_start()
    else:
        print("退出启动程...")
        break