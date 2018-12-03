import redis, json, datetime

now_datetime = lambda: datetime.datetime.now().__str__()


def bdict2dict(bdict, key=None):
    """
    @bdict: bytes dict like b{'keys': val}"
    @key: key bytes or str, if is None no need key

    @return Python dict
    %% byte dict --> str --> dict
    """
    try:
        if bdict is None: return None
        if key is None: return eval(str(bdict, "utf-8"))
        key = key if isinstance(key, bytes) else bytes(key, "utf-8")
        return eval(str(bdict.get(key, None), "utf-8"))
    except Exception as err:
        print(err)
        return None


def wrt_dict_into_redisHM(name, key, value, host='localhost', port=6379, db=0):
    """
    name db key<->vallue
    :param name: 键值对名称
    :param key: 键
    :param value: 值, Python字典
    :param host: host[default 'localhost']
    :param port: port[default 6379]
    :param db: db[default db0]
    :return:
    """
    r = redis.Redis(host=host, port=port, db=db)
    r.hset(name, key, str(value))
    r.save()
    return 0


def show_redisHM(name, key, host='localhost', port=6379, db=0):
    r = redis.Redis(host=host, port=port, db=db)
    return r.hget(name, key)