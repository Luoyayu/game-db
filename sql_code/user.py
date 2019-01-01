# -*- coding: UTF-8 -*-

from gameflask.sql_code.mysqlhelp import *
from pyvalidators.idcard import is_valid_idcard
from pyvalidators.ipaddr import IPAddrValidator

r0, cursor = None, None
try:
    r0 = r()
    cursor = r0.cursor()
except Exception as e:
    print(e.args[1])


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
            "permission": None,
            "status": None
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

        self.uid = None

        self.user_info["id_card_number"] = id_card_number
        self.user_info["real_name"] = real_name
        self.user_info["sex"] = sex
        self.user_info["account_name"] = account_name
        self.user_info["passwd"] = passwd
        self.user_info["ip"] = ip
        self.user_info['permission'] = 0
        self.user_info["register_datetime"] = now_datetime()
        self.user_info['status'] = 0

        flag = wrt_dict_into_table('game.user', cursor, self.user_info)
        r0.commit()
        return flag

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

        user_info = get_table_entry_as_dict(
            sql_cmd="select * from game.user where game.user.ID=" + str(uid),
            cursor=cursor,
            flag='one')

        if user_info is None: return "UID_NOT_EXIST"
        if user_info['passwd'] != passwd: return "WRONG_PASSWD"

        self.uid = uid
        for key, value in user_info.items():
            self.user_info[key] = value

        self.user_info['last_login_datetime'] = now_datetime()
        self.user_info['status'] = 1

        return update_table_entry(
            table='user.game',
            cursor=cursor,
            where=['ID', self.uid],
            data={
                'last_login_datetime': now_datetime(),
                'status': 1
            })

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

        return update_table_entry(
            table='user.game',
            cursor=cursor,
            where=['ID', self.uid],
            data={
                'last_logout_datetime': now_datetime(),
                'status': 0
            })

    def load(self, uid=None):
        """
        load user if uid not exist return error
        :param uid:
        :return:
        """
        if uid is None and self.uid is None:
            return "NO_UID"
        self.uid = self.uid if uid is None else uid
        user_info = get_table_entry_as_dict(
            sql_cmd="select * from game.user where game.user.ID=" + str(self.uid),
            cursor=cursor,
            flag='one')
        if user_info is None:
            return "UID_NOT_EXIST"
        for key, value in user_info.items():
            self.user_info[key] = value
        return 0

    def delete(self, uid=None):
        pass
