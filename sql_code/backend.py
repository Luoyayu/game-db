from gameflask.sql_code.mysqlhelp import *

r0, cursor = None, None
try:
    r0 = r()
    cursor = r0.cursor()
except redis.Error as e:
    print(e)
    print("连接失败")


def test_add_user():
    cursor.execute("SELECT VERSION()")
    print("Database version:", cursor.fetchone()[0])

    # add_user = """INSERT INTO game.user(ID, real_name, account_name, id_card_number, passwd, ip, last_login_datetime,
    #                last_logout_datetime, register_datetime, permission, sex)
    #                VALUES(NULL, '小明', '爱玩的小明同学', '220582197707198131', '123456', '127.0.0.1', '2018-12-27 06:32:58',
    #                '2018-12-27 10:33:07', '2018-12-28 06:30:16', 0, '男');"""
    # try:
    #     cursor.execute(add_user)
    #     r0.commit()
    # except redis.err.IntegrityError as e:
    #     cprint(text=e.args[1], color='red')
    #     r0.rollback()

    # sql_cmd = "SELECT * FROM game.user where real_name='小刚'"
    #
    # user_lst = get_table_entry_as_dict(sql_cmd, cursor, 'one')
    # if not isinstance(user_lst, str):
    #     print(len(user_lst))
    #     print(user_lst)
    #     print(type(user_lst['last_login_datetime']))
    # else:
    #     print(user_lst)

    _dict = {'ID': 'NULL',
             'real_name': '小花',
             'account_name': '爱玩的小花同学',
             'id_card_number': 220582197707198132,
             'passwd': '123456',
             'ip': '127.0.0.1',
             'last_login_datetime': datetime.datetime(2018, 12, 27, 6, 32, 58),
             'last_logout_datetime': datetime.datetime(2018, 12, 27, 10, 33, 7),
             'register_datetime': datetime.datetime(2018, 12, 28, 6, 30, 16),
             'permission': 0,
             'sex': '男'}

    _dict2 = {'ID': 'NULL',
              'real_name': '小明',
              'account_name': '爱玩的小明同学',
              'id_card_number': 220582197707198135,
              'passwd': '123456',
              'last_login_datetime': datetime.datetime(2018, 12, 27, 6, 32, 58),
              'last_logout_datetime': datetime.datetime(2018, 12, 27, 10, 33, 7),
              'register_datetime': datetime.datetime(2018, 12, 28, 6, 30, 16),
              'sex': '男'}

    print(wrt_dict_into_table('game.user', cursor, _dict2))
    r0.commit()
    r0.close()
    print("close normally")


def test_mysql_to_dict():
    pass


if __name__ == '__main__':
    test_add_user()
