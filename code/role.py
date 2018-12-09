from gameflask.code.redishelp import *

r0 = redis.Redis(host=host, port=port, db=0, password=RedisPasswd)  # user redis db


class Role:
    def __init__(self):
        self.role_info = {
            'role_name': None,
            'exp': None,
            'lv': None,
            'sex': None,
            'created_datetime': None,
            'job': None,
            'server_part': None,
            'power': None,
            'backpack_id': None,  # 拥有的背包ID
            'pokemons': []  # 拥有的宝可梦ID列表
        }
        self.uid = None  # 账号ID
        self.rid = None  # 角色ID
        self.role_template_num = 0  # 角色模板ID

    def create_role(self, uid, role_name, sex, job, server_part):
        """
        创建角色, 更新账号信息
        :param uid: 账号ID
        :param role_name: 角色名
        :param sex: 性别 ['男', '女', '保密']
        :param job: 职业 ['战士', '法师', '刺客']
        :param server_part: 区服 ["华东", '华北', '华南', '华西', '华中']
        :return:
        """
        if len(role_name) > 20: return "TOO_LONG_ROLE_NAME"
        if job not in ['战士', '法师', '刺客']: return "WRONG_JOB"
        if server_part not in ["华东", '华北', '华南', '华西', '华中']: return "WRONG_SERVER_PART"
        if sex not in ['男', '女', '保密']: return "WRONG_SEX"

        self.uid = uid
        self.rid = r0.incr('role_id')

        self.role_info['role_name'] = role_name
        self.role_info['exp'] = 0
        self.role_info['lv'] = 0
        self.role_info['sex'] = sex
        self.role_info['created_datetime'] = now_datetime()
        self.role_info['job'] = job
        self.role_info['server_part'] = server_part
        self.role_info['power'] = 0
        self.role_info['backpack_id'] = r0.incr('backpack_id')

        user_info = get_redisHM_items_as_dict('user', uid, db=0)
        user_info['role_id_list'].append(self.rid)
        wrt_dict_into_redisHM('user', uid, user_info, db=0)

        return self.storage()

    def storage(self):
        """
        save self.role_info to redis role db
        先填充role1.role_info !
        """
        if self.rid is None:
            return "NO_RID"
        return wrt_dict_into_redisHM("role", self.rid, self.role_info, db=0)

    def load(self, rid=None):
        if rid is None:
            if self.rid is None:
                return "NO_RID"
        else:
            self.rid = rid
        role_info = get_redisHM_items_as_dict('role', rid, db=0)
        if role_info is None:
            return "WRONG_RID"
        for key, value in role_info:
            self.role_info[key] = value
        return 0

    def delete(self, uid=None, rid=None):
        """
        删除角色信息, 更新账号信息
        :return:
        """
        if rid is None:
            if self.rid is None:
                return "NO_RID"
        else:
            self.rid = rid

        if rid is None:
            if self.rid is None:
                return "NO_UID"
        else:
            self.rid = uid

        if delete_redisHM_items('role', self.rid, db=0):
            return "WRONG_RID"

        user_info = get_redisHM_items_as_dict('user', self.uid, db=0)
        try:
            user_info['role_id_list'].remove(self.rid)
        except ValueError:
            return "THE_USER_DONOT_HAVE_THIS_RID"

        # FIXME: 删除宝可梦实例, 背包实例等
        return wrt_dict_into_redisHM('user', self.uid, user_info, db=0)


def test_create_role():
    r0.delete('role')  # just for test
    r0.delete("role_id")
    r0.delete("backpack_id")

    role1 = Role()

    flag = role1.create_role(
        uid=1,
        role_name='小智',
        sex='男',
        job='战士',
        server_part='华中'
    )
    assert flag == 0
    cprint("create_role: " + str(flag), 'red')
    dprint(role1.role_info)
    from gameflask.code.user import GeneralUser
    user1 = GeneralUser()
    user1.load(uid=1)
    dprint(user1.user_info)


def test_delete():
    role1 = Role()
    role1.uid = 1
    flag = role1.delete(rid=1)
    cprint(str(flag))
    from gameflask.code.user import GeneralUser
    user1 = GeneralUser()
    user1.load(uid=1)
    dprint(user1.user_info)


def main():
    pass


if __name__ == "__main__":
    test_create_role()
