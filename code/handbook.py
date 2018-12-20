import gameflask.code.redishelp
from redishelp import *
from crawler import craw

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

            'HP': None,
            'Atk': None,
            'Def': None,
            'SpAtk': None,
            'SpDef': None,
            'Speed': None,

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
            "acc": None,
            "pp": None
        }

    def craw_pokemon(self, pokemon_name):
        flag = craw(pokemon_name)
        if flag == 0:
            with open("pokemon.json", 'r') as f:
                crawed_pokemon = json.load(f)

            for key in crawed_pokemon.keys():
                self.pokemon[key] = crawed_pokemon[key]
        else:
            print("WRONG_POKEMON_NAME", pokemon_name)

    def load_pokemon(self, pokemon_id):
        pokemon_info = get_redisHM_items_as_dict('handbook_pokemon', pokemon_id, db=0)
        if pokemon_info is None:
            return "WRONG_POKEMON_ID"
        for key in pokemon_info.keys():
            self.pokemon[key] = pokemon_info[key]
        return 0

    def storage_pokemon(self, pokemon_id=None):
        if pokemon_id is None:
            pokemon_id = r0.incr("handbook_pokemon_idx")
        r0.hset('handbook_pokemon_name_id', self.pokemon['name'], pokemon_id)
        wrt_dict_into_redisHM('handbook_pokemon', pokemon_id, self.pokemon, db=0)

    def get_pokemon_id_by_name(self, name):
        pokemon_id = r0.hget("handbook_pokemon_name_id", name)
        if pokemon_id is None: return None
        return int(pokemon_id)

    def del_pokemon_by_name(self, name):
        pokemon_id = self.get_pokemon_id_by_name(name)
        if pokemon_id is None: return "WRONG_POKEMON_NAME"
        r0.hdel("handbook_pokemon", pokemon_id)
        r0.hdel("handbook_pokemon_name_id", name)
        r0.save()

    def del_pokemon_by_id(self, pokemon_id):
        pokemon_info = get_redisHM_items_as_dict("handbook_pokemon", pokemon_id, db=0)
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

    def load_move(self, move_id):
        move_info = get_redisHM_items_as_dict("handbook_move", move_id, db=0)
        if move_info is None: return "WRONG_MOVE_ID"

        for key in move_info.keys():
            self.move[key] = move_info[key]
        return 0

    def storage_move(self, move_id=None):
        if move_id is None:
            move_id = r0.incr("handbook_move_idx")
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
        move_info = get_redisHM_items_as_dict("handbook_move", move_id, db=0)
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


if __name__ == '__main__':
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

    print("finish, {}s".format(ti() - l_ti))
