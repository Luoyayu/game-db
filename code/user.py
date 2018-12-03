# -*- coding: UTF-8 -*-
import random
from redishelp import *
from termcolor import cprint
from pyvalidators.idcard import is_valid_idcard
from pyvalidators.ipaddr import IPAddrValidator

r0 = redis.Redis(host='localhost', port=6379, db=0)  # user redis db


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
        self.uid = None
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
        if is_valid_idcard(str(id)): return "WRONG_ID_CARD_NUMBER"
        if len(real_name) > 6: return "TOO_LONG_REAL_NAME"
        if len(account_name) > 25: return "TOO_LONG_ACCOUNT_NAME"
        if len(passwd) < 8: return "TOO_SHORT_PASSWD"
        if sex not in ['男', '女', '保密']: return "WRONG_SEX"
        if not IPAddrValidator.is_valid(str(ip)): return "WRONG_IPADDR"

        if not r0.sadd('id_card_number_set', id_card_number): return "EXISTED_ID_CARD_NUMBER"
        if not r0.sadd('account_name_set', account_name): return "EXISTED_ACCOUNT_NAME"

        self.uid = r0.incr("user_id")
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
        user_info = bdict2dict(r0.hget('user', uid))
        if user_info is None:
            return "ID_NOT_EXIST"
        if user_info['passwd'] != passwd:
            return "WRONG_PASSWD"
        else:
            self.uid = uid
            self.status = 1
            for key, value in user_info.items():
                self.user_info[key] = value
            self.user_info['last_login_datetime'] = now_datetime()
            return 0

    def logout(self):
        if self.status == 0: return "NOT_ONLINE"
        self.status = 0
        self.user_info['last_logout_datetime'] = now_datetime()
        self.storage()
        r0.save()  # save to disk
        return 0


def test_registering():
    user1 = GeneralUser()
    r0.set('user_id', 0)  # just for test

    flag = str(user1.registering(
        id_card_number="220582197707198132",
        real_name="小刚",
        sex="男",
        account_name="爱玩的小刚同学",
        passwd="PASSWORD",
        ip="127.0.0.1"
    ))

    cprint("registering: " + flag, 'red')
    if not flag:  # 注册成功
        cprint("storage: " + user1.storage(), color='red')

    cprint('debug user info:', 'green')
    print(user1.user_info)


def test_login():
    user1 = GeneralUser()
    cprint("login: " + str(user1.login(uid=111, passwd='PASSWORD')), 'red')

    cprint('login: ' + str(user1.login(1, 'password')), 'red')

    cprint('login: ' + str(user1.login(1, 'PASSWORD')), 'red')

    cprint('debug user info:', 'green')
    print(user1.user_info)


def test_logout():
    user1 = GeneralUser()
    cprint('logout: ' + str(user1.logout()), 'red')

    user1.login(1, 'PASSWORD')
    cprint('logout: ' + str(user1.logout()), 'red')


def main():
    pass


if __name__ == "__main__":
    main()
