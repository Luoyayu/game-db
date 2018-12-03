from gameflask.code.redishelp import *

r0 = redis.Redis(host='localhost', port=6379, db=0)  # user redis db


class Role:
    def __int__(self):
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
        :param server_part: 区服 ["华东", '华北', '华南', '华西']
        :return:
        """
        if len(role_name) > 20: return "TOO_LONG_ROLE_NAME"
        if job not in ['战士', '法师', '刺客']: return "WRONG_JOB"
        if server_part not in ["华东", '华北', '华南', '华西']: return "WRONG_SERVER_PART"
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

        user_info = get_redisHM_items_as_dict('user', uid)
        user_info['role_id_list'].append(self.rid)
        wrt_dict_into_redisHM('user', uid, user_info)

        return self.storage()

    def storage(self):
        """
        save self.role_info to redis role db
        先填充role1.role_info !
        """
        if self.rid is None:
            return "NO_RID"
        return wrt_dict_into_redisHM("user", self.rid, self.role_info)

    def load(self):
        pass

    def delete(self, rid=None):
        """
        删除角色信息, 更新账号信息
        :return:
        """
        if rid is None:
            if self.rid is None:
                return "NO_RID"
            else:
                self.rid = rid
        delete_redisHM_items('role', self.rid)
        user_info = get_redisHM_items_as_dict('user', self.uid)
        user_info['role_id_list'].pop(self.rid)
        # FIXME: 删除宝可梦实例, 背包实例等
        return wrt_dict_into_redisHM('user', self.uid, user_info)
