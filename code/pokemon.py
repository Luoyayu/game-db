from gameflask.code.redishelp import *

r1 = redis.Redis(host=host, port=port, db=1, password=RedisPasswd)  # user redis db1


class Pokemon:
    def __init__(self):
        self.pokemon_info = {
            'name': None,
            'type': [],
            'species': None,
            'lv': None,
            'exp': None,
            'equipment': [],
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
            'growth_rate': None,
            'base_exp': None,
            'ev_yield': None,
            'egg_groups': None,
            'egg_cycles': None,
            'gender': None,

            'location': None,
            'moves': []
        }
        self.pokemon_id = None
        self.rid = None

    def create_pokemon(self, rid, pokemon_id):
        """
        创建宝可梦, 初始化宝可梦信息信息，并且更新角色信息
        :param pokemon_id:
        :param rid: 角色ID
        :return:
        """
        # if rid not exit “打印错误”
        from gameflask.code.handbook import handbook
        self.pokemon_id = r1.incr('pokemon_idx')
        hd = handbook()
        hd.load_pokemon(pokemon_id)
        for key in hd.pokemon.keys():
            self.pokemon_info[key] = hd.pokemon[key]
        self.pokemon_info['lv'] = 0
        self.pokemon_info['exp'] = self.pokemon_info['base_exp']
        role_info = get_redisHM_items_as_dict('role', rid, db=1)
        if role_info is None: return "WRONG_RID"
        role_info['pokemons'].append(self.pokemon_id)
        wrt_dict_into_redisHM('role', rid, role_info, db=1)

        return self.storage()

    def storage(self):
        if self.pokemon_id is None:
            return "NO_POKEMON_ID"
        return wrt_dict_into_redisHM("pokemon", self.pokemon_id, self.pokemon_info, db=1)

    def load(self, pokemon_id=None):
        if pokemon_id is None:
            if self.pokemon_id is None:
                return "NO_POKEMON_ID"
        else:
            self.pokemon_id = pokemon_id
        pokemon_info = get_redisHM_items_as_dict('pokemon', pokemon_id, db=1)
        if pokemon_info is None:
            return "WRONG_POKEMON_ID"
        for key in pokemon_info:
            self.pokemon_info[key] = pokemon_info[key]
        return 0

    def delete(self, rid=None, pokemon_id=None):
        """
        删除角色的宝可梦信息, 更新角色信息
        :return:
        """
        if pokemon_id is None:
            if self.pokemon_id is None:
                return "WRONG_POKEMON_ID"
        else:
            self.pokemon_id = pokemon_id

        if rid is None:
            if self.rid is None:
                return "NO_RID"
        else:
            self.rid = rid

        if delete_redisHM_items('pokemon', self.pokemon_id, db=1):
            return "WRONG_POKEMON_ID"

        role_info = get_redisHM_items_as_dict('role', rid, db=1)
        if role_info is None: return "WRONG_RID"

        try:
            role_info['pokemons'].remove(self.pokemon_id)
        except ValueError:
            return "THE_ROLE_DO_NOT_HAVE_THIS_POKEMON_ID"

        return wrt_dict_into_redisHM('role', rid, role_info, db=1)

    def equip(self, eid):
        self.pokemon_info['equipment'].append(eid)
        return self.storage()

    def get_power(self, name=None):
        from gameflask.code.handbook import handbook
        hd = handbook()
        if name is None:
            power = self.pokemon_info['atk']
            for equipment in self.pokemon_info['equipment']:
                hd.search_equipment_by_id(equipment)
                power += hd.equipment['atk']
            return power

        else:
            hd.search_move_by_name(name)
            if hd.move['power'] is None:
                return 0
            else:
                power = hd.move["power"] * 2
                for equipment in self.pokemon_info['equipment']:
                    hd.search_equipment_by_id(equipment)
                    power += hd.equipment['atk']
                return power

    def attacked(self, power):
        real_hurt = power - self.pokemon_info['def']
        if real_hurt > 0:
            hp = self.pokemon_info['hp'] - real_hurt
            if hp <= 0:
                self.pokemon_info['hp'] = 0
                return "POKEMON_IS_DEAD"
            else:
                self.pokemon_info['hp'] = hp
        return 0


def test_create_pokemon(id):
    # r1.delete('pokemon')  # just for test
    # r1.delete("pokemon_id")

    pokemon1 = Pokemon()

    flag = pokemon1.create_pokemon(rid=1, pokemon_id=id)
    assert flag == 0
    cprint("create_pokemon: " + str(flag), 'red')
    dprint(pokemon1.pokemon_info)
    from gameflask.code.role import Role
    role1 = Role()
    role1.load(rid=1)
    dprint(role1.role_info)


def test_delete(id1, id2):
    pokemon1 = Pokemon()
    # pokemon1.rid = 1
    flag = pokemon1.delete(rid=id1, pokemon_id=id2)
    cprint(str(flag))
    from gameflask.code.role import Role
    role1 = Role()
    role1.load(rid=1)
    dprint(role1.role_info)


def test_fighting():
    pokemon1 = Pokemon()
    pokemon2 = Pokemon()
    pokemon1.load(pokemon_id=1)
    pokemon2.load(pokemon_id=2)
    pokemon1.equip(1)
    # dprint(pokemon1.pokemon_info)
    # dprint(pokemon2.pokemon_info)
    for i in range(10):
        if pokemon2.attacked(pokemon1.get_power(name='Peck')) == "POKEMON_IS_DEAD":
            print("pokemon2 is dead\n")
            break
        if pokemon1.attacked(pokemon2.get_power(name='Disable')) == "POKEMON_IS_DEAD":
            print("pokemon1 is dead\n")
            break
        print(pokemon1.pokemon_info['name'], ":", pokemon1.pokemon_info['hp'], "\n")
        print(pokemon2.pokemon_info['name'], ":", pokemon2.pokemon_info['hp'], "\n")


if __name__ == "__main__":
    # test_create_pokemon(82)
    # test_create_pokemon(46)
    test_fighting()
# test_delete(1,3)
