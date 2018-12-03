from redishelp import *

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
            'backpack_id': None,  # 背包ID
            'pokemons': []  # 宝可梦ID列表
        }
        self.uid = None
        self.rid = None
        self.role_template_num = 0

    def create_role(self, uid, role_name, sex, job, server_part):
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

        user_info = bdict2dict(r0.hget('user', uid))
        user_info['role_id'].append(self.rid)
        wrt_dict_into_redisHM('user', uid, user_info)

        return self.storage()

    def storage(self):
        """
        save self.role_info to redis role db
        """
        return wrt_dict_into_redisHM("user", self.rid, self.role_info)
