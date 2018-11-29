#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = '单人行'

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from core import host_manage

while True:
    host_manage.show_iplist()