#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author '单人行'

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from atm import atm
from shopping import shop

while True:
    choice = input("请选择购物系统(按'1'),ATM系统(按'2'):")
    if choice == "1":
        shop.main_shop()
    elif choice == "2":
        atm.main_atm()
    else:
        sys.exit()