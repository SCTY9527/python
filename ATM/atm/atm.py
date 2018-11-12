#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author '单人行

import os,sys,time,json
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

ATM_menu_show = [
    "1.账户查询",
    "2.账户添加",
    "3.账户注销",
    "4.账户转账",
    "5.账户提现",
    "6.冻结解冻",
    "7.每月还款",
    "8.打印账单"
]


def write_atm_log(lines):     # 定义日志记录功能
    curr_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    with open(BASE_DIR + "/logs/atm.log", "a") as f:
        f.write("%s %s\n"%(curr_time,lines))

def get_info(user_name):
    if os.path.isfile(BASE_DIR+'/accounts/'+user_name+'.json'):
        with open(BASE_DIR+'/accounts/'+user_name+'.json', "r") as f:
            acc_name = json.loads(f.read())
            return acc_name

def select():   #定义查询功能
    while True:
        username = input("请输入要查询的用户(按'q'退出):")
        if os.path.isfile(BASE_DIR+'/accounts/'+username+'.json'):
            with open(BASE_DIR+'/accounts/'+username+'.json', "r") as f:
                user = json.loads(f.read())
                print(user)
                log = "查询用户：" + username
        elif username == "q":
            sys.exit()
        else:
            print("你所查询的用户不存在!")
            log = "查询用户" + username +"不存在!"
        write_atm_log(log)

def add():     # 定义添加账户功能
    while True:
        username = input("请输入用户名(按'q'退出):")
        if not os.path.isfile(BASE_DIR+'/accounts/'+username+'.json'):
            password = input("请输入密码:")
            balance = input("请输入存款金额:")
            limit = input("请设置信用额度：")
            info = {"username":username,"password":password,"balance":balance,"limit":limit,'frozon':False}
            with open(BASE_DIR+'/accounts/'+username+'.json', "a") as f:   #添加账户文件
                f.write(json.dumps(info))
            open(BASE_DIR+'/logs/'+username+'.log',"a")    # 添加日志文件
            log = "添加账户" + username + "成功!"
        elif username == "q":
            break
        else:
            print("你输入的账户已存在!")
            log = "账户已存在，添加失败!"
        write_atm_log(log)

def remove():   # 定义删除账号功能
    username = input("请输入要注销的账户:")
    password = input("请输入账户密码:")
    user = get_info(username)
    if password == user["password"]:          # 打开此账户文件并判断密码是否正确
        print("登录成功!")
        os.remove(BASE_DIR+'/accounts/'+username+'.json')
        print("注销用户%s成功!"%username)
        write_atm_log("注销用户%s成功!"%username)
    else:
        print("密码错误，你没有权利注销此账户!")
    if os.path.isfile(BASE_DIR+'/logs/'+username+'.log'):  #判断是否存在用户日志文件，在的话就删除
        os.remove(BASE_DIR+'/logs/'+username+'.log')
        print("注销用户%s的日志成功!"%username)
        write_atm_log("注销用户%s的日志成功!"%username)
    else:
        print("你输入的账户不存在!")
        write_atm_log("你输入的用户%s不存在" %username)

def transfer():
    """
    1、先输入账户密码
    2、判断用户是否冻结
    3、判断密码是否正确
    4、输入转入方账户是否存在
    5、判断转入方用户是否冻结
    6、判断用户金额是否充足
    """
    username = input("请输入你的账号:")
    password = input("请输入你的密码:")
    user = get_info(username)
    if user["frozon"]:   # 2、判断：用户冻结
        print("你的账户已冻结，无法转账!")
        log = "账户" + username + "已冻结,无法转账!"
        write_atm_log(log)
    else:                 # 判断：用户没冻结
        if password == user["password"]:   # 3、密码正确
            print("登录成功!")
            tran_user = input("请输入转入方账号:")
            t_user = get_info(tran_user)
            if t_user["frozon"]:   # 5、转入方账户冻结
                print("%s已被冻结，转账失败!"%tran_user)
                log = tran_user +"已被冻结，"+"用户"+username+"向"+tran_user+"转账失败!"
                write_atm_log(log)
            else:                   # 转入方账户没冻结
                tran_num = input("请输入转账金额:")
                if int(tran_num) - t_user["balance"] < t_user["limit"]:  #6、转账金额足够
                    user["balance"] -= int(tran_num)
                    t_user["balance"] += int(tran_num)
                    with open(BASE_DIR+'/accounts/'+username+'.json', "w") as f2:
                        f2.write(json.dumps(user))
                    with open(BASE_DIR+'/accounts/'+tran_user+'.json', "w") as f3:
                        f3.write(json.dumps(t_user))
                    log = "用户"+username+"向"+"用户"+tran_user+"转账"+tran_num+"!"
                    write_atm_log(log)
                else:       # 转账金额不够
                    print("你的信用额度不够，转账失败!")
                    log = username + "信用额度不够，向" + tran_user + "转账失败!"
                    write_atm_log(log)
        else:
            print("密码错误，请重新输入!")

def withdraw():
    username = input("请输入用户名:")
    password = input("请输入密码:")
    user = get_info(username)
    if password == user["password"]:
        print("用户登录成功!")
        with_amount = input("请输入提现金额:")
        if user["balance"] > int(with_amount):
            print("提现成功!")
            user["balance"] -= int(with_amount)
            with open(BASE_DIR+'/accounts/'+username+'.json', "w") as f1:
                f1.write(json.dumps(user))
                write_atm_log("用户%s提现%s!"%(username,with_amount))
        else:
            print("余额不足，提现失败!")
            write_atm_log("余额不足，用户%s提现失败!"%username)
    else:
        print("密码错误，用户登录失败!")

def frozen():
    username = input("请输入用户名:")
    password = input("请输入密码:")
    user = get_info(username)
    if password == user["password"]:
        print("用户登录成功!")
        choice = input("冻结按1,解冻按2:")
        if choice == "1":
            user["frozon"] = True
            print("冻结用户成功!")
            write_atm_log("冻结用户%s成功!"%username)
        elif choice == "2":
            user["frozon"] = False
            print("解冻用户%s成功!"%username)
            write_atm_log("解冻用户%s成功!"%username)
    else:
        print("密码错误，登录失败!")

def repayment():
    username = input("请输入用户名:")
    password = input("请输入密码:")
    user = get_info(username)
    if password == user["password"]:
        print("用户登录成功!")
        balance = user["balance"]
        if balance > 0:
            print("你目前的余额为%s，不需要还款!"%balance)
        else:
            print("你目前的余额为%s，需要还款%s!"%(balance,balance))
            repay_ment = input("请输入还款金额:")
            user["balance"] += int(repay_ment)
            with open(BASE_DIR+'/accounts/'+username+'.json', "w") as f1:
                f1.write(json.dumps(user))
                print("用户%s还款%s成功!"%(username,repay_ment))
                write_atm_log("用户%s还款%s成功!"%(username,repay_ment))
    else:
        print("密码错误,用户登录失败!")

def printbill():
    username = input("请输入用户名:")
    password = input("请输入密码:")
    user = get_info(username)
    if password == user["password"]:
        print("用户登录成功!")
    date1 = input("输入打印账单开始日期,格式:2018-04-03 12:00:00>>>:")
    date2 = input("输入打印账单结束日期,格式:2018-04-03 20:00:00>>>:")
    with open(BASE_DIR+'/logs/'+username+'.log','r') as f:
        for i in f:
            if i[:19] >= date1 and i[:19] < date2:
                print(i.strip())
    write_atm_log("打印用户%s的账单%s到%s" %(username,date1,date2))

atm_menu = {
    "1":select,
    "2":add,
    "3":remove,
    "4":transfer,
    "5":withdraw,
    "6":frozen,
    "7":repayment,
    "8":printbill
}

def main_atm():
    print("----ATM选项菜单----")
    for i in ATM_menu_show:
        print("   %s"%i)
    choice = input("请输入服务选项:")
    atm_menu[choice]()