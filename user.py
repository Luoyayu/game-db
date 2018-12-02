# -*- coding: UTF-8 -*-
import random
from redishelp import *
from termcolor import cprint
from pyvalidators.idcard import is_valid_idcard
from pyvalidators.ipaddr import IPAddrValidator

user_r = redis.Redis(host='localhost', port=6379, db=0)  # user redis db


class GeneralUser:
    def __init__(self):
        self.user_info = {  # 用户信息
            "id_card_number": None,
            "real_name": None,
            "sex": None,
            "account_name": None,
            "passwd": None,
            "ip": None,
            "last_login_datetime": None,
            "last_logout_datetime": None,
            "register_datetime": None,
            "permission": None,  # 权限 普通用户为0
            "account_id": [],  # 账号ID列表索引
        }
        self.uid = user_r.incr("user_id")
        self.login_info = {
            "uid": None,
            "passwd": None
        }
        self.status = -1

    def registering(self, id_card_number, real_name, sex, account_name, passwd, ip):
        """
        @参数: 身份证(str), 真实姓名(str), 性别(str), 账户名(str), 密码(str), IP(str)
        @功能: 完成用户字典建立
        """
        if is_valid_idcard(str(id)): return -1
        if len(real_name) > 6: return -2
        if len(account_name) > 25: return -3
        if sex not in ['男', '女', '保密']: return -4
        if not IPAddrValidator.is_valid(str(ip)): return -5

        self.user_info["id_card_number"] = id_card_number
        self.user_info["real_name"] = real_name
        self.user_info["sex"] = sex
        self.user_info["account_name"] = account_name
        self.user_info["passwd"] = passwd
        self.user_info["ip"] = ip
        self.user_info['permission'] = 0
        self.user_info["register_datetime"] = now_datetime()
        return 0

    def storage(self):
        wrt_dict_into_redisHM("user", self.uid, self.user_info)
        return 0

    def login(self):
        user_info = bdict2dict(user_r.hget('user', self.login_info['uid']))
        if user_info is None:
            return -7
        if user_info['passwd'] != self.login_info['passwd']:
            return -6
        else:
            self.status = 1
            for key, value in user_info.items():
                self.user_info[key] = user_info[key]
            self.user_info['last_login_datetime'] = now_datetime()
            return 0

    def logout(self):
        self.status = 0
        self.user_info['last_logout_datetime'] = now_datetime()
        self.storage()
        user_r.save()  # save to disk
        return 0


def test():
    user1 = GeneralUser()
    user_r.set('user_id', 0)  # just for test

    # flag = user1.registering(
    #     id_card_number="220582197707198132",
    #     real_name="小刚",
    #     sex="男",
    #     account_name="爱玩的小刚同学",
    #     passwd="PASSWD",
    #     ip="127.0.0.1"
    # )
    #
    # cprint("registering: " + err_code[flag], 'red')
    # if not flag:
    #     cprint("storage: " + err_code[user1.storage()], color='red')
    #
    # cprint('debug user info:', 'green')
    # print(user1.user_info)

    user1.login_info['uid'] = 111
    user1.login_info["passwd"] = 'PASSWD'
    cprint("login: " + err_code[user1.login()], 'red')

    user1.login_info['uid'] = 1
    user1.login_info['passwd'] = 'passwd'
    cprint('login: ' + err_code[user1.login()], 'red')

    user1.login_info['uid'] = 1
    user1.login_info['passwd'] = 'PASSWD'
    cprint('login: ' + err_code[user1.login()], 'red')

    cprint('debug user info:', 'green')
    print(user1.user_info)

    cprint('logout: ' + err_code[user1.logout()], 'red')


if __name__ == "__main__":
    test()
