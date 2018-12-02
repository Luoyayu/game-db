import redis
import json


def bdict2dict(bdict, key=None):
    """
    @bdict: bytes dict like b{'keys': val}"
    @key: key bytes or str, if is None no need key

    @return Python dict
    %% byte dict --> str --> dict
    """
    try:
        if key is None: return eval(str(bdict, "utf-8"))
        key = key if isinstance(key, bytes) else bytes(key, "utf-8")
        return eval(str(bdict.get(key, None), "utf-8"))
    except Exception as err:
        print(err)
        return None


def test_redis_HashMap():
    r0 = redis.Redis(host='localhost', port=6379, db=0)  # connect to db0
    r0.save()
    userHM = r0.hgetall("user")  # lookup 'user' hashmap
    userHMkeys = r0.hkeys("user")  # get hashmap all keys (bytes)

    print("keys: ", userHMkeys)

    new_user = {
        1: {'id': 1, 'name': 'player1'},
        2: {'id': 2, 'name': 'player2'},
        3: {'id': 3, 'name': 'player3'},
        4: {'id': 4, 'name': 'player4'},
    }

    for key, val in new_user.items():
        r0.hset("user", key, str(val))  # insert key-value entry into db0 'user' Hashmap

    users = {}  # user list
    for key in userHM.keys():
        users[key] = bdict2dict(userHM, key)  # read to Python list

    for key in userHM.keys():
        if (int(key) > 3):
            r0.hdel("user", key)  # del entry by key(int or bytes)

    user1 = bdict2dict(r0.hget("user", userHMkeys[0]))  # got single value
    print(user1)


def test_redis_List():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.delete('role')
    r.lpush('role', '1')


def test_redis_Set():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.delete('account_name')

