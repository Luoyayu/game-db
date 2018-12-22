from redishelp import *

r0 = redis.Redis(host=host, port=port, db=0, password=RedisPasswd)  # user redis db


class Backpack:
    def __init__(self):
        self.backpack = {
            'usage': 0,
            'item_lst': [],
            'equipment_lst': [],
            'lv': 1
        }
        self.bp_id = None

    def create_backpack(self, bp_id=None):
        if bp_id is None:
            self.bp_id = r0.incr("backpack_idx")
        self.storage()
        return self.bp_id

    def storage(self, bp_id=None):
        if bp_id: self.bp_id = bp_id
        return wrt_dict_into_redisHM("backpack", self.bp_id, self.backpack, db=0)

    def load(self, bp_id=None):
        if self.bp_id is None: self.bp_id = bp_id
        if self.bp_id is None: return "WRONG_bp_id"

        backpack_info = get_redisHM_items_as_dict("backpack", bp_id, db=0)
        if backpack_info is None: return "WRONG_bp_id"
        for key in backpack_info.keys():
            self.backpack = backpack_info[key]
        return 0

    def show_item_lst(self, bp_id):
        flag = self.load(bp_id)
        if not flag:
            return self.backpack['item_lst']
        return None

    def show_equipment_lst(self, bp_id):
        flag = self.load(bp_id)
        if not flag:
            return self.backpack['equipment_lst']
        return None

    def init_backpack(self, bp_id):
        flag = self.load(bp_id)
        if flag:
            print(flag)
            return -1
        self.backpack = {
            'usage': 0,
            'item_lst': [],
            'equipment_lst': [],
            'lv': 1
        }
        return self.storage(bp_id)

    def add_item(self, bp_id, item_id):
        if not self.load(bp_id):
            self.backpack['item_lst'].append(item_id)
            return self.storage(bp_id)
        return "WRONG_bp_id"

    def add_equipment(self, bp_id, eid):
        if not self.load(bp_id):
            self.backpack['equipment_lst'].append(eid)
            return self.storage(bp_id)
        return "WRONG_bp_id"

    def del_item(self, bp_id, item_id):
        if not self.load(bp_id):
            try:
                self.backpack['item_lst'].remove(item_id)
            except ValueError:
                return "ITEM_ID_NOT_EXIST"
            self.storage(bp_id)
            return 0
        return "WRONG_bp_id"

    def del_equipment(self, bp_id, eid):
        if not self.load(bp_id):
            try:
                self.backpack['equipment_lst'].remove(eid)
            except ValueError:
                return "EQUIPMENT_ID_NOT_EXIST"
            self.storage(bp_id)
            return 0
        return "WRONG_bp_id"
