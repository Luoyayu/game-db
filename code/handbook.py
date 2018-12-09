import gameflask.code.redishelp
from redishelp import *

r0 = redis.Redis(host=host, port=port, db=0, password=RedisPasswd)  # user redis db0


class handbook:
    def __init__(self):
        self.pokemon = {
            'name': None,
            'Type': [],
            'main_Abilities': None,
            'vice_Abilities': None,
            'height': None,
            'weight': None,

            'HP': None,
            'attack': None,
            'defense': None,
            'SpAtk': None,
            'Sp. Def': None,
            'speed': None,

            'catch_rate': None,
            'Friendship': None,
            'Growth Rate': None,

            'eV_yield': None,
            'egg_groups': None,
            'gender': None,
            'egg_cycles': None,

            'moves': []
        }
        self.move = {

        }

    def load_pokemon(self):
        pokemon_id = r0.incr("handbook_pokemon_idx")
        pass

    def storage_pokemon(self):
        pass

    def del_pokemon_by_name(self):
        pass

    def del_pokemon_by_idx(self):
        pass

    def search_pokemon_by_name(self):
        pass

    def search_pokemon_by_idx(self):
        pass

    def load_move(self):
        move_idx = r0.incr('handbook_move_idx')
        pass

    def del_move_by_name(self):
        pass

    def del_move_by_idx(self):
        pass

    def search_move_by_name(self):
        pass

    def search_move_by_idx(self):
        pass
