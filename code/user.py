# -*- coding: UTF-8 -*-
from gameflask.code.redishelp import *

from pyvalidators.idcard import is_valid_idcard
from pyvalidators.ipaddr import IPAddrValidator

r0 = redis.Redis(host=host, port=port, db=0, password=RedisPasswd)  # user redis db


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
            "role_id_list": [],  # 角色ID列表索引
            "status": None  # 状态
        }
        self.uid = None
        self.login_info = {
            "uid": None,
            "passwd": None
        }

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
        self.user_info['status'] = 0
        self.storage()
        return 0

    def storage(self):
        """
        save self.user_info to redis user db
        先填充user1.user_info !
        """
        if self.uid is None:
            return "NO_UID"
        return wrt_dict_into_redisHM("user", self.uid, self.user_info, db=0)

    def login(self, uid=None, passwd=None):
        """
        :param uid:
        :param passwd:
        如果登录参数为空, 将从user1.login_info中获得
        user1.login(uid, passed)
        或者先填充 user1.login_info['uid'], user1.login_info['passwd'] 调用user1.login()
        :return:
        """
        uid = self.login_info['uid'] if uid is None else uid
        passwd = self.login_info['passwd'] if passwd is None else passwd
        if uid is None: return "UID_IS_NONE"
        if passwd is None: return "PASSWD_IS_NONE"

        self.login_info['uid'] = uid
        self.login_info['passwd'] = passwd
        user_info = get_redisHM_items_as_dict('user', uid, db=0)

        if user_info is None: return "UID_NOT_EXIST"
        if user_info['passwd'] != passwd: return "WRONG_PASSWD"

        self.uid = uid
        for key, value in user_info.items():
            self.user_info[key] = value
        self.user_info['last_login_datetime'] = now_datetime()
        self.user_info['status'] = 1
        return self.storage()

    def logout(self, uid=None):
        """
        登出, user1.logout(uid), 或者user1.logout()
        :param uid:
        :return:
        """
        if uid is None and self.uid is None:
            return "NO_UID"
        else:
            self.uid = self.uid if uid is None else uid
            if self.load():  # fill self.user_info
                return "UID_NOT_EXIST"
        if self.user_info['status'] == 0: return "NOT_ONLINE"

        self.user_info['status'] = 0
        self.user_info['last_logout_datetime'] = now_datetime()
        return self.storage()

    def load(self, uid=None):
        """
        load user if uid not exist return error
        :param uid:
        :return:
        """
        if uid is None and self.uid is None:
            return "NO_UID"
        self.uid = self.uid if uid is None else uid
        user_info = get_redisHM_items_as_dict(name='user', key=self.uid, db=0)
        if user_info is None:
            return "UID_NOT_EXIST"
        for key, value in user_info.items():
            self.user_info[key] = value
        return 0

    # TODO DELETE USER

    # def delete(self, uid=None):
    #     if uid is None:
    #         if self.uid is None:
    #             return "NO_UID"
    #         else:
    #             self.uid = uid
    #     return delete_redisHM_items('user', self.uid)


def test_registering():
    user1 = GeneralUser()
    r0.set('user_id', 0)  # just for test

    r0.delete('id_card_number_set')  # # just for test
    r0.delete('account_name_set')  # # just for test

    flag = user1.registering(
        id_card_number="220582197707198132",
        real_name="小刚",
        sex="男",
        account_name="爱玩的小刚同学",
        passwd="PASSWORD",
        ip="127.0.0.1"
    )
    assert flag == 0, 'registering failed'
    cprint("registering: " + str(flag), 'red')
    if not flag:  # 注册成功
        flag = user1.storage()
        assert flag == 0, 'storage failed'
        cprint("storage: " + str(flag), color='red')

    flag = user1.registering(
        id_card_number="220582197707198132",
        real_name="小盟",
        sex="男",
        account_name="爱玩的小盟同学",
        passwd="PASSWORD",
        ip="127.0.0.1"
    )
    assert flag == "EXISTED_ID_CARD_NUMBER"
    cprint("registering: " + str(flag), 'red')

    flag = user1.registering(
        id_card_number="220582197707198133",
        real_name="小盟",
        sex="男",
        account_name="爱玩的小刚同学",
        passwd="PASSWORD",
        ip="127.0.0.1"
    )
    assert flag == "EXISTED_ACCOUNT_NAME"
    cprint("registering: " + str(flag), 'red')

    cprint('debug user info:', 'green')
    dprint(user1.user_info)


def test_login():
    # unittest
    user1 = GeneralUser()

    flag = user1.login(uid=111, passwd='PASSWORD')
    assert flag == "UID_NOT_EXIST"
    dprint(user1.login_info)
    cprint("login1: " + str(flag), 'red')

    flag = user1.login(1, 'password')
    assert flag == "WRONG_PASSWD"
    dprint(user1.login_info)
    cprint('login1: ' + str(flag), 'red')

    flag = user1.login(1, 'PASSWORD')
    assert flag == 0
    dprint(user1.login_info)
    cprint('login1: ' + str(flag), 'red')

    user2 = GeneralUser()

    user2.login_info['uid'] = 1
    user2.login_info['passwd'] = 'PASSWORD'

    flag = user2.login()
    assert flag == 0
    dprint(user1.login_info)
    cprint('login2: ' + str(flag), 'red')

    user3 = GeneralUser()

    flag = user3.login()
    assert flag == 'UID_IS_NONE'
    dprint(user3.login_info)
    cprint('login3: ' + str(flag), 'red')

    user3.login_info['uid'] = 1

    flag = user3.login()
    assert flag == 'PASSWD_IS_NONE'
    dprint(user3.login_info)
    cprint('login3: ' + str(flag), 'red')

    cprint('debug user info:', 'green')
    dprint(user1.user_info)


def test_logout():
    user1 = GeneralUser()
    cprint('logout: ' + str(user1.logout()), 'red')

    flag = user1.login(1, 'PASSWORD')
    assert flag == 0

    flag = user1.logout()
    assert flag == 0
    assert user1.user_info['status'] == 0

    cprint('logout: ' + str(flag), 'red')

    dprint(user1.user_info)


def test_main():
    cprint("begin test", 'blue')
    user1 = GeneralUser()


if __name__ == "__main__":
    cprint('test over', 'blue')
