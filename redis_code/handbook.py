import gameflask.redis_code.redishelp
from gameflask.redis_code.redishelp import *
from gameflask.redis_code.crawler import Craw_pokemon, Craw_move

r0 = redis.Redis(host=host, port=port, db=0, password=RedisPasswd)  # user redis db0


class handbook:
    def __init__(self):
        self.pokemon = {
            'name': None,
            'type': [],
            'species': None,
            'main_ability': None,
            'vice_ability': None,
            'height': None,
            'weight': None,

            'hp': None,
            'atk': None,
            'def': None,
            'spatk': None,
            'spdef': None,
            'speed': None,

            'catch_rate': None,
            'friendship': None,
            'base_exp': None,
            'growth_rate': None,

            'ev_yield': None,
            'egg_groups': None,
            'egg_cycles': None,
            'gender': None,
            'location': None,

            'moves': []
        }

        self.move = {
            "name": None,
            "type": None,
            "power": None,
            "accuracy": None,
            "pp": None
        }

        self.equipment = {
            'name': None,
            'atk': None,
            'def': None,
            'spatk': None,
            'spdef': None,
            'lv': None,
            'type': None
        }
        self.item = {
            'name': None,
            'description': None,
        }

    def craw_pokemon(self, pokemon_name, with_move=0):
        flag = Craw_pokemon(pokemon_name)
        if flag == 0:
            with open("pokemon.json", 'r') as f:
                crawed_pokemon = json.load(f)

            for key in crawed_pokemon.keys():
                self.pokemon[key] = crawed_pokemon[key]
        else:
            print("WRONG_POKEMON_NAME", pokemon_name)
        if with_move:
            for move in self.pokemon['moves']:
                move = move.replace(' ', '-').replace(',', '')
                print("craw", move)
                self.craw_move(move)
                # print(self.move)
                self.storage_move()

    def load_pokemon(self, pokemon_id):
        pokemon_info = get_redisHM_entry_as_dict('handbook_pokemon', pokemon_id, db=0)
        if pokemon_info is None:
            return "WRONG_POKEMON_ID"
        for key in pokemon_info.keys():
            self.pokemon[key] = pokemon_info[key]
        return 0

    def get_all_pokemon(self):
        blist = r0.hkeys("handbook_pokemon")
        return [int(x) for x in blist]

    def storage_pokemon(self, pokemon_id=None):
        if pokemon_id is None:
            pokemon_id = r0.hget("handbook_pokemon_name_id", self.pokemon['name'])
            if pokemon_id is None:
                pokemon_id = r0.incr("handbook_pokemon_idx")
        if self.pokemon['name'] is None: return "POKEMON_INFO_NOT_COMPLETED"
        r0.hset('handbook_pokemon_name_id', self.pokemon['name'], pokemon_id)
        wrt_dict_into_redisHM('handbook_pokemon', pokemon_id, self.pokemon, db=0)

        for typ in self.pokemon['type']:
            lst = r0.get("handbook_pokemon_" + typ)
            if lst is None:
                lst = []
            else:
                lst = eval(lst)
            lst.append(pokemon_id)
            lst = list(set(lst))
            r0.set("handbook_pokemon_" + typ, str(lst))

    def get_pokemon_id_by_name(self, name):
        pokemon_id = r0.hget("handbook_pokemon_name_id", name)
        if pokemon_id is None: return None
        return int(pokemon_id)

    def get_all_pokemon_by_type_name(self, type_name):
        type_name = type_name.capitalize()
        lst = r0.get("handbook_pokemon_" + type_name)
        if lst is None: return None
        return eval(lst)

    def del_pokemon_by_name(self, name):
        pokemon_id = self.get_pokemon_id_by_name(name)
        if pokemon_id is None: return "WRONG_POKEMON_NAME"
        r0.hdel("handbook_pokemon", pokemon_id)
        r0.hdel("handbook_pokemon_name_id", name)
        r0.save()

    def del_pokemon_by_id(self, pokemon_id):
        pokemon_info = get_redisHM_entry_as_dict("handbook_pokemon", pokemon_id, db=0)
        if pokemon_info is None: return "WRONG_POKEMON_ID"
        r0.hdel("handbook_pokemon", pokemon_id)
        r0.hdel("handbook_pokemon_name_id", pokemon_info['name'])
        r0.save()

    def search_pokemon_by_name(self, name):
        pokemon_id = self.get_pokemon_id_by_name(name)
        if pokemon_id is None: return "WRONG_POKEMON_NAME"
        self.load_pokemon(pokemon_id)
        return pokemon_id

    def search_pokemon_by_id(self, pokemon_id):
        self.load_pokemon(pokemon_id)
        return pokemon_id

    def craw_move(self, move_name):
        flag = Craw_move(move_name)
        if flag == 0:
            with open("move.json", 'r') as f:
                crawed_move = json.load(f)

            for key in crawed_move.keys():
                self.move[key] = crawed_move[key]
        else:
            print("WRONG_MOVE_NAME", move_name)

    def load_move(self, move_id):
        move_info = get_redisHM_entry_as_dict("handbook_move", move_id, db=0)
        if move_info is None: return "WRONG_MOVE_ID"

        for key in move_info.keys():
            self.move[key] = move_info[key]
        return 0

    def get_all_move(self):
        blist = r0.hkeys("handbook_move")
        return [int(x) for x in blist]

    def storage_move(self, move_id=None):
        if move_id is None:
            move_id = r0.hget("handbook_move_name_id", self.move['name'])
            if move_id is None:
                move_id = r0.incr("handbook_move_idx")
        if self.move['name'] is None: return "MOVE_INFO_NOT_COMPLETED"
        r0.hset('handbook_move_name_id', self.move['name'], move_id)
        wrt_dict_into_redisHM('handbook_move', move_id, self.move, db=0)

    def get_move_id_by_name(self, name):
        move_id = r0.hget("handbook_move_name_id", name)
        if move_id is None: return None
        return int(move_id)

    def del_move_by_name(self, name):
        move_id = self.get_move_id_by_name(name)
        if move_id is None: return "WRONG_MOVE_NAME"
        r0.hdel("handbook_move", move_id)
        r0.hdel("handbook_move_name_id", name)
        r0.save()

    def del_move_by_id(self, move_id):
        move_info = get_redisHM_entry_as_dict("handbook_move", move_id, db=0)
        if move_info is None: return "WRONG_MOVE_ID"
        r0.hdel("handbook_move_name_id", move_info['name'])
        r0.hdel('handbook_move', move_id)
        r0.save()

    def search_move_by_name(self, name):
        move_id = self.get_move_id_by_name(name)
        if move_id is None: return "WRONG_MOVE_NAME"
        self.load_move(move_id)
        return move_id

    def search_move_by_id(self, move_id):
        self.load_move(move_id)
        return 0

    def load_equipment(self, eid):
        equipment_info = get_redisHM_entry_as_dict("handbook_equipment", eid, db=0)
        if equipment_info is None: return "WRONG_EID"
        for key in equipment_info.keys():
            self.equipment[key] = equipment_info[key]
        return 0

    def get_all_equipment(self):
        blist = r0.hkeys("handbook_equipment")
        return [int(x) for x in blist]

    def storage_equipment(self, eid=None):
        if eid is None:
            eid = r0.hget("handbook_equipment_name_id", self.equipment['name'])
            if eid is None:
                eid = r0.incr("handbook_equipment_idx")
        if self.equipment['name'] is None: return "EQUIPMENT_INFO_NOT_COMPLETED"
        r0.hset('handbook_equipment_name_id', self.equipment['name'], eid)
        wrt_dict_into_redisHM('handbook_equipment', eid, self.equipment, db=0)

    def get_equipment_id_by_name(self, name):
        eid = r0.hget("handbook_equipment_name_id", name)
        if eid is None: return None
        return int(eid)

    def load_equipment_by_name(self, ename):
        eid = self.get_equipment_id_by_name(ename)
        if eid is None: return "WRONG_EQUIPMENT_NAME"
        self.load_equipment(eid)
        return eid

    def load_equipment_by_id(self, eid):
        self.load_equipment(eid)
        return 0

    def del_equipment_by_name(self, ename):
        eid = self.get_equipment_id_by_name(ename)
        if eid is None: return "WRONG_EQUIPMENT_NAME"
        r0.hdel("handbook_equipment", eid)
        r0.hdel("handbook_equipment_name_id", ename)
        r0.save()

    def del_equipment_by_id(self, eid):
        equipment_info = get_redisHM_entry_as_dict("handbook_equipment", eid, db=0)
        if equipment_info is None: return "WRONG_EQUIPMENT_ID"
        r0.hdel("handbook_equipment", eid)
        r0.hdel("handbook_equipment_name_id", equipment_info['name'])
        r0.save()


def test_handbook_pokemon():
    r0.delete("handbook_pokemon_idx")
    handbook0 = handbook()
    temp = {
        'name': None,
        'type': [],
        'main_ability': None,
        'vice_ability': None,
        'height': None,
        'weight': None,

        'HP': None,
        'attack': None,
        'defense': None,
        'SpAtk': None,
        'SpDef': None,
        'speed': None,

        'catch_rate': None,
        'friendship': None,
        'growth_rate': None,

        'ev_yield': None,
        'egg_groups': None,
        'gender': None,
        'egg_cycles': None,
    }
    for i in range(10):
        temp['name'] = "姓名" + str(i)
        handbook0.pokemon = temp
        handbook0.storage_pokemon()
    handbook0.del_pokemon_by_name("姓名7")
    handbook0.del_pokemon_by_id(9)
    print(handbook0.search_pokemon_by_id(1))
    print(handbook0.pokemon['name'])
    print(handbook0.search_pokemon_by_name("姓名1"))


def test_handbook_move():
    r0.delete("handbook_move_idx")
    handbook0 = handbook()
    temp = {
        "name": None,
        "type": None,
        "power": None,
        "acc": None,
        "pp": None
    }
    for i in range(10):
        temp['name'] = "招式" + str(i)
        handbook0.move = temp
        handbook0.storage_move()
    handbook0.del_move_by_name("招式7")
    handbook0.del_move_by_id(9)
    print(handbook0.search_move_by_id(1))
    print(handbook0.move['name'])
    print(handbook0.search_move_by_name("招式1"))


def test_craw_and_save(name):
    handbook0 = handbook()
    handbook0.craw_pokemon(name)
    # dprint(handbook0.pokemon)
    handbook0.storage_pokemon()


def test_pokemon():
    handbook0 = handbook()
    handbook0.load_pokemon(80)
    dprint(handbook0.pokemon)


def test_craw_100_pokemon():
    l_ti = ti()
    r0.delete("handbook_pokemon")
    r0.delete("handbook_pokemon_name_id")
    r0.delete("handbook_pokemon_idx")
    cnt = 1
    with open("pokemon_list", 'r') as f:
        for line in f:
            name = line.strip()
            print("{} ready for {}".format(cnt, name))
            cnt += 1
            test_craw_and_save(name)
            # if cnt == 20: break

    print("finish, {}s".format(ti() - l_ti))


def test_search_pokemon_by_type():
    hd = handbook()
    print(hd.get_all_pokemon_by_type_name("Flyin"))
    print(hd.get_all_pokemon_by_type_name("Flying"))
    print(hd.get_all_pokemon_by_type_name("grass"))
    print(hd.get_all_pokemon_by_type_name("water"))


def test_create_equipment():
    r0.delete("handbook_equipment_idx")
    hd = handbook()
    f = open("equipments.json", 'r', encoding='utf-8')
    equipmentList = json.load(f)
    # print(equipmentList)
    for e in equipmentList:
        hd.equipment = e
        hd.storage_equipment()


if __name__ == '__main__':
    test_create_equipment()
    # test_craw_100_pokemon()
    # test_search_pokemon_by_type()
    # hd = handbook()
    # print(hd.get_all_pokemon())
    # test_pokemon()
    # print(str([1, 2, 3, 4]))
    # r0.set("test", str([1, 2, 3, 4]))

    # test = r0.get("test1")
    # print(test)
    # print(eval(test)[0])
