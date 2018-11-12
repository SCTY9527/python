#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author '单人行'

import os,sys,json,time
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
goods_list = {
    "1":["icar",280000],
    "2":["ipad",6888],
    "3":["iphone",5888],
    "4":["mihone",1999],
    "5":["mi fan",19],
    "6":["hong mi",999],
    "7":["hat",9],
    "8":["pen",7],
    "9":["wrap",38]
}

curr_user = ""
shop_goods = []
choices = []

def acc_change():    #账户信息更改
    with open(BASE_DIR+'/accounts/'+username+'.json', "r") as f:
        user = json.loads(f.read())
        for i in choices:
            user["balance"] -= goods_list[i][1]
            with open(BASE_DIR+'/accounts/'+username+'.json', "w") as f1:
                f1.write(json.dumps(user))

def print_good_list():   # 定义登录用户后答应商品列表
    print("--------超市商品列表--------")
    print("%-7s%-10s%s"%("商品号","商品名","售价"))
    for i in goods_list:
        print("%-10s%-13s%s"%(i,goods_list[i][0],goods_list[i][1]))

def showcar():  # 定义结算时答应购物车列表
    print("****你的购物车列表****")
    global sum
    sum = 0
    for i in choices:
        print("%s:%s"%(goods_list[i][0],goods_list[i][1]))
        sum += goods_list[i][1]
    print("合计：%s"%sum)

def user_login():  # 定义用户登录
    global username
    username = input("please enter your username:")
    password = input("please enter your password:")
    if os.path.isfile(BASE_DIR + "/accounts/" + username + ".json"):
        with open(BASE_DIR + "/accounts/" + username + ".json","r") as f:
            user = json.loads(f.read())
            if username == user["username"] and password == user["password"]:
                global curr_user
                curr_user = username
            else:
                print("你的密码错误!")
    else:
        print("你输入的用户不存在!")
        sys.exit()

def write_log():   # 定义结算后将用户购物记录写入日志中
    with open(BASE_DIR + "/logs/" + curr_user + ".log", "a") as f:
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        f.write("\n%s"%curr_time)
        for i in choices:
            f.write("\n\t购买:%-10s 价格:%s"%(goods_list[i][0], goods_list[i][1]))
        f.write("\t\t总计:%s"%sum)

def main_shop():   # 定义主程序
    user_login()
    while True:
        print_good_list()
        choice_a = input("请选择您所需要的商品单号:")
        choice = str(choice_a)
        if choice in goods_list:
            choices.append(choice)   # 将字典的key加到choices中，打印购物车时会用到
            goods = goods_list[choice][0]
            shop_goods.append(goods)
            print("加入购物车成功！")
        elif choice == "q":
            break
        elif choice == "c":  # c为结算并记录日志、更改账户
            showcar()
            acc_change()
            write_log()
            sys.exit()
