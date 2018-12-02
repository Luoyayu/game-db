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
            "role_id": [],  # 角色ID列表索引
        }
        self.uid = user_r.incr("user_id")
        self.login_info = {
            "uid": None,
            "passwd": None
        }
        self.status = 0

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
        self.storage()
        return 0

    def storage(self):
        """
        save self.user_info to redis user db
        """
        return wrt_dict_into_redisHM("user", self.uid, self.user_info)

    def login(self, uid, passwd):
        self.login_info['uid'] = uid
        self.login_info['passwd'] = passwd
        user_info = bdict2dict(user_r.hget('user', uid))
        if user_info is None:
            return -7
        if user_info['passwd'] != passwd:
            return -6
        else:
            self.status = 1
            for key, value in user_info.items():
                self.user_info[key] = user_info[key]
            self.user_info['last_login_datetime'] = now_datetime()
            return 0

    def logout(self):
        if self.status == 0: return -8
        self.status = 0
        self.user_info['last_logout_datetime'] = now_datetime()
        self.storage()
        user_r.save()  # save to disk
        return 0


def test_registering():
    user1 = GeneralUser()
    user_r.set('user_id', 0)  # just for test

    flag = user1.registering(
        id_card_number="220582197707198132",
        real_name="小刚",
        sex="男",
        account_name="爱玩的小刚同学",
        passwd="PASSWD",
        ip="127.0.0.1"
    )

    cprint("registering: " + err_code[flag], 'red')
    if not flag:  # 注册成功
        cprint("storage: " + err_code[user1.storage()], color='red')

    cprint('debug user info:', 'green')
    print(user1.user_info)


def test_login():
    user1 = GeneralUser()
    cprint("login: " + err_code[user1.login(uid=111, passwd='PASSWD')], 'red')

    cprint('login: ' + err_code[user1.login(1, 'passwd')], 'red')

    cprint('login: ' + err_code[user1.login(1, 'PASSWD')], 'red')

    cprint('debug user info:', 'green')
    print(user1.user_info)


def test_logout():
    user1 = GeneralUser()
    cprint('logout: ' + err_code[user1.logout()], 'red')

    user1.login(1, 'PASSWD')
    cprint('logout: ' + err_code[user1.logout()], 'red')


def main():
    pass


if __name__ == "__main__":
    main()
