from gameflask.redis_code.redishelp import *

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

        backpack_info = get_redisHM_entry_as_dict("backpack", bp_id, db=0)
        if backpack_info is None: return "WRONG_bp_id"
        for key in backpack_info.keys():
            self.backpack[key] = backpack_info[key]
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
            for i, item in enumerate(self.backpack['item_lst']):
                if item[0] == item_id:  # [[item_idx, owner], ...]
                    self.backpack['item_lst'][i][1] += 1
                    self.backpack['usage'] += 1
                    return self.storage(bp_id)
            self.backpack['item_lst'].append([item_id, 1])
            return self.storage(bp_id)
        return "WRONG_bp_id"

    def add_equipment(self, bp_id, eid):  # [[1, 2]] 1eq owner is 2
        if not self.load(bp_id):
            self.backpack['equipment_lst'].append([eid, -1])
            self.backpack['usage'] += 1
            return self.storage(bp_id)
        return "WRONG_bp_id"

    def del_item(self, bp_id, item_id):
        flag = 0
        if not self.load(bp_id):
            try:
                for i, item in enumerate(self.backpack['item_lst']):
                    if item_id == item[0]:
                        flag = 1
                        self.backpack['item_lst'][i][1] -= 1
                        self.backpack['usage'] -= 1
                        if self.backpack['item_lst'][i][1] == 0:
                            self.backpack['item_lst'].remove([item_id, 0])
                        return self.storage(bp_id)
            except ValueError:
                return "ITEM_ID_NOT_EXISTED"
            if flag == 0:
                return "ITEM_ID_NOT_EXISTED"
            return self.storage(bp_id)
        return "WRONG_bp_id"

    def del_equipment(self, bp_id, eid):
        flag = 0
        if not self.load(bp_id):
            try:
                for eq in self.backpack['equipment_lst']:
                    if eq[0] == eid:
                        self.backpack['equipment_lst'].remove(eq)
                        flag = 1
                        self.backpack['usage'] -= 1
            except ValueError:
                return "EQUIPMENT_ID_NOT_EXIST"
            if flag == 0:
                return "EQUIPMENT_ID_NOT_EXIST"
            return self.storage(bp_id)
        return "WRONG_bp_id"


def test_equipment():
    r0.delete("backpack_idx")
    r0.delete("backpack")
    bp = Backpack()
    from gameflask.redis_code.handbook import handbook
    hd = handbook()
    bp_id = bp.create_backpack()
    print('backpack id is', bp_id)

    bp.add_equipment(bp_id=bp_id, eid=1)
    print(bp.show_equipment_lst(bp_id))  # [1, -1]

    bp.add_equipment(bp_id=bp_id, eid=1)  # [[1, -1], [1, -1]]
    print(bp.show_equipment_lst(bp_id))

    bp.add_equipment(bp_id=bp_id, eid=2)  # [[1, -1], [1, -1], [2, -1]]
    print(bp.show_equipment_lst(bp_id))

    bp.del_equipment(bp_id, 1)
    print(bp.show_equipment_lst(bp_id))  # [[1, -1], [2, -1]]

    bp.del_equipment(bp_id, 1)
    print(bp.show_equipment_lst(bp_id))  # [[2, -1]]

    print(bp.del_equipment(bp_id, 1))  # EQUIPMENT_ID_NOT_EXIST
    print(bp.show_equipment_lst(bp_id))  # [[2, -1]]

    # hd.load_equipment(eid=2)
    # dprint(hd.equipment)


def test_item():
    bp_id = 1
    backpack = Backpack()
    backpack.load(bp_id)
    backpack.backpack['item_lst'] = []
    backpack.storage()

    backpack.load(bp_id)
    print(backpack.show_item_lst(bp_id))  # []

    print(backpack.add_item(bp_id, 1))
    print(backpack.show_item_lst(bp_id))  # [[1, 1]]

    print(backpack.add_item(bp_id, 1))
    print(backpack.show_item_lst(bp_id))  # [[1, 2]]

    print(backpack.add_item(bp_id, 2))
    print(backpack.show_item_lst(bp_id))  # [[1, 2], [2, 1]]

    print(backpack.del_item(bp_id, 2))
    print(backpack.show_item_lst(bp_id))

    print(backpack.del_item(bp_id, 2))
    print(backpack.show_item_lst(bp_id))


def init_item():
    item1 = {
        'name': '小血瓶',
        'description': '小血瓶 能恢复50HP'
    }
    item2 = {
        'name': '中血瓶',
        'description': '中血瓶 能恢复100HP'
    }
    item3 = {
        'name': '小蓝瓶',
        'description': '小血瓶 能恢复100PP'
    }
    item4 = {
        'name': '精灵球',
        'description': '精灵球 有概率捕获宝可梦'
    }
    wrt_dict_into_redisHM("handbook_item", 1, item1, db=0)
    wrt_dict_into_redisHM("handbook_item", 2, item2, db=0)
    wrt_dict_into_redisHM("handbook_item", 3, item3, db=0)
    wrt_dict_into_redisHM("handbook_item", 4, item4, db=0)


if __name__ == '__main__':
    test_equipment()
