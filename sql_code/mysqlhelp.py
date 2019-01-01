import pymysql as redis
from termcolor import cprint as colorful_print
import datetime, time, pprint, copy, json, random

# mysql setting
# =======================
host = 'localhost'
user = 'root'
passwd = 'sql'
port = 3306
charset = 'utf8'
db = "game"
# =======================

reasonable_color = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

r = lambda: redis.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset)
cprint = lambda **kwargs: colorful_print(''.join((kwargs['text'])), color=kwargs['color'])
eprint = lambda text: colorful_print(''.join((text)), color='green', on_color='on_red')
now_datetime = lambda: datetime.datetime.now().__str__()
dprint = lambda dict: pprint.PrettyPrinter(indent=4).pprint(dict)
ti = lambda: time.time()


def get_table_entry_as_dict(sql_cmd, cursor, flag):
    """
    mysql表项转成Python字典, [one, all]
    :param sql_cmd: sql script snippet
    :param cursor: sql connection cursor
    :return: `all` 包含字典的列表 or `one` 字典 or -1 if error
     :param flag: 'one' 获取一项, 'all' 获取所有项
    """
    try:
        cursor.execute(sql_cmd)
    except Exception as e:
        return e.args[1]
    else:
        if flag == 'one':
            data = cursor.fetchone()
        elif flag == 'all':
            data = cursor.fetchall()
        else:
            return "get_table_entry_as_dict: one/all?"
        descpt = cursor.description
        if descpt is None or data is None: return "ERROR_NONE"
        descpt = [y[0] for y in [list(x) for x in descpt]]
        if isinstance(data[0], tuple):
            return [dict(zip(descpt, x)) for x in data]
        else:
            return dict(zip(descpt, data))


def wrt_dict_into_table(table, cursor, data):
    """
    在table中创建一个新的表项
    :param table: 表名
    :param cursor: cursor
    :param data: 字典
    :return:
    """
    descpt = ','.join(list(data.keys()))
    data = dict(zip(data.keys(), [str(x) if isinstance(x, datetime.datetime) else x for x in data.values()]))
    data = str(list(data.values())).replace('[', '').replace(']', '').replace("'NULL'", "NULL").replace('None', 'NULL')
    try:
        sql_cmd = "INSERT INTO {} ({}) VALUES({});".format(table, descpt, data)
        print(sql_cmd)
        cursor.execute(sql_cmd)
    except Exception as e:
        return e.args[1]
    return 0


def update_table_entry(table, cursor, where, data):
    set_str = ""
    for k, v in data.items():
        if isinstance(v, str):
            set_str += "{} = '{}',".format(k.replace("'", ''), v)
        elif v is None:
            set_str += "{} = NULL,".format(k.replace("'", ''))
        else:
            set_str += "{} = {},".format(k.replace("'", ''), v)
    set_str = set_str[:-1]

    sql_cmd = "update {} \n set {} \n where {}.{} = {}".format(table, set_str, table, where[0], where[1])
    print(sql_cmd)
    try:
        cursor.execute(sql_cmd)
    except Exception as e:
        return e.args[1]
    return 0


if __name__ == '__main__':
    r0, cursor = None, None
    try:
        r0 = r()
        cursor = r0.cursor()
    except redis.Error as e:
        print(e)
        print("连接失败")

    print(update_table_entry('game.user', cursor, ['ID', 131],
                             {'account_name': "爱玩的小华同学", 'real_name': '小华', 'ip': None}))
    r0.commit()
