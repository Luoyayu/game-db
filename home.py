from flask import Flask, session, request, render_template, redirect, url_for
import os
import redis

from termcolor import cprint
from gameflask.code.user import GeneralUser
from gameflask.code.role import Role
from gameflask.code.handbook import handbook
from gameflask.code.pokemon import Pokemon
from gameflask.code.redishelp import *

# 传递根目录
app = Flask(__name__)

# session
app.secret_key = os.urandom(24)
user = GeneralUser()
role = Role()


# 默认路径访问登录页面
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def registering():
    return "注册网页"


# 默认路径访问用户页面
# dashoard
@app.route('/main/')
def main():
    uid = user.uid
    role_id_list = user.user_info["role_id_list"][0]
    role.load(role_id_list)

    rolename = role.role_info["name"]
    # 图鉴宝可梦数量待写
    hd = handbook()
    tot = len(hd.get_all_pokemon())

    money = role.role_info["money"]
    job = role.role_info["job"]
    lv = role.role_info["lv"]

    power = role.role_info["power"]

    return render_template('main.html', rolename=rolename, tot=tot, money=money, job=job, lv=lv, power=power)


'''
index点击Login触发的路由事件
session读取网页发来的表单信息（Username，Password）
判断信息（弹窗，直接返回原网页）
返回用户页面main.html
'''


@app.route('/login', methods=['POST', 'GET'])
def getLoginRequest():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']

        # print('username',request.form.get('username'))
        # print('password',request.form.get('password'))
        # print(session['username'], session['password'])

        user.login_info['uid'] = session['username']
        user.login_info["passwd"] = session['password']
        flag = user.login(session['username'], session['password'])
        # flag=0
        cprint("登录状况: {}".format(str(flag), 'red'))

        if not flag:
            return redirect(url_for('main'))
        return render_template('index.html')

@app.route('/main/pokemon')
def showpokemon():
    uid = user.uid
    role_id_list = user.user_info["role_id_list"][0]
    role.load(role_id_list)
    pokemon_list = role.role_info['present']  # 宝可梦表的id

    print(pokemon_list)

    pokemons = []

    for pokemon_index in pokemon_list:
        one_pokemon = Pokemon()
        one_pokemon.load(pokemon_index)

        pokemon_dict = one_pokemon.pokemon_info
        pokemon_dict['url'] = "https://img.pokemondb.net/artwork/large/" + pokemon_dict['name'].lower() + ".jpg"
        pokemon_dict['id'] = pokemon_index
        pokemons.append(pokemon_dict)

    return render_template('mainpage/pokemon/pokemon.html', pokemons=pokemons)


@app.route('/main/pokemon_change_down<id>')
def pokemon_change_down(id=None):
    uid = user.uid
    role_id = user.user_info["role_id_list"][0]
    role.load(role_id)

    print(id)
    id = int(id)

    role.exit_pokemon(role_id, id)

    role.load(role_id)

    pokemon_list = role.role_info['present']  # 宝可梦表的id
    pokemons = []

    for pokemon_index in pokemon_list:
        one_pokemon = Pokemon()
        one_pokemon.load(pokemon_index)

        pokemon_dict = one_pokemon.pokemon_info
        pokemon_dict['url'] = "https://img.pokemondb.net/artwork/large/" + pokemon_dict['name'].lower() + ".jpg"
        pokemon_dict['id'] = pokemon_index

        pokemons.append(pokemon_dict)

    return render_template('mainpage/pokemon/pokemon.html', pokemons=pokemons)


@app.route('/main/pokemon_change_up<id>')
def pokemon_change_up(id=None):
    uid = user.uid
    role_id = user.user_info["role_id_list"][0]
    role.load(role_id)

    id = int(id)

    role.select_pokemon(role_id, id)

    role.load(role_id)
    dprint(role.role_info)

    pokemon_list = role.role_info['present']  # 宝可梦表的id
    pokemons = []

    for pokemon_index in pokemon_list:
        one_pokemon = Pokemon()
        one_pokemon.load(pokemon_index)

        pokemon_dict = one_pokemon.pokemon_info
        pokemon_dict['url'] = "https://img.pokemondb.net/artwork/large/" + pokemon_dict['name'].lower() + ".jpg"
        pokemon_dict['id'] = pokemon_index

        pokemons.append(pokemon_dict)

    return render_template('mainpage/pokemon/pokemon.html', pokemons=pokemons)


@app.route('/main/handbook')
def showhandbook():
    hd = handbook()
    pokemon_keys = hd.get_all_pokemon()

    # 无条件查找
    pokemons = []
    for pokemon_index in pokemon_keys:
        hd = handbook()
        hd.load_pokemon(pokemon_index)
        one_pokemon = hd.pokemon
        one_pokemon['key'] = pokemon_index
        pokemons.append(hd.pokemon)

    return render_template('mainpage/handbook/handbook.html', pokemons=pokemons)


# 详细的pokemon信息
@app.route('/main/handbook_<id>/')
def handbook_detail(id=None):
    hd = handbook()
    hd.load_pokemon(id)

    url = "https://img.pokemondb.net/artwork/large/" + hd.pokemon['name'].lower() + ".jpg"

    return render_template("mainpage/handbook/handbook_detail.html", url=url, moves=hd.pokemon['moves'],
                           one_pokemon=hd.pokemon)


# 按名查找
@app.route('/main/search_by_name', methods=['POST', 'GET'])
def search_by_name():
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name']

        hd = handbook()
        pokemon_index = hd.get_pokemon_id_by_name(pokemon_name)

        pokemons = []

        hd.load_pokemon(pokemon_index)
        one_pokemon = hd.pokemon
        one_pokemon['key'] = pokemon_index
        pokemons.append(hd.pokemon)

        return render_template('mainpage/handbook/handbook.html', pokemons=pokemons)


# 按类型查找
@app.route('/main/search_by_type', methods=['POST', 'GET'])
def search_by_type():
    if request.method == 'POST':
        pokemon_type = request.form.getlist('type')
        print(pokemon_type[0])

        hd = handbook()
        if (pokemon_type[0] == 'all'):
            pokemon_keys = hd.get_all_pokemon()
            print("is all")
        else:
            print("not all")
            pokemon_keys = hd.get_all_pokemon_by_type_name(pokemon_type[0])

        # 无条件查找
        pokemons = []
        for pokemon_index in pokemon_keys:
            hd = handbook()
            hd.load_pokemon(pokemon_index)
            one_pokemon = hd.pokemon
            one_pokemon['key'] = pokemon_index
            pokemons.append(hd.pokemon)

        return render_template('mainpage/handbook/handbook.html', pokemons=pokemons)


@app.route('/main/repertory')
def showrepertory():
    uid = user.uid
    role_id_list = user.user_info["role_id_list"][0]
    role.load(role_id_list)
    pokemon_list = role.role_info['pokemons']  # 宝可梦表的id

    pokemons = []

    for pokemon_index in pokemon_list:
        pokemon = Pokemon()
        pokemon.load(pokemon_index)

        # pokemon_dict = {}
        # pokemon_dict['name'] = one_pokemon.pokemon_info['name']
        # pokemon_dict['hp'] = one_pokemon.pokemon_info['hp']
        # pokemon_dict['lv'] = one_pokemon.pokemon_info['lv']
        # pokemon_dict['atk'] = one_pokemon.pokemon_info['atk']
        # pokemon_dict['def'] = one_pokemon.pokemon_info['def']
        # pokemon_dict['spatk'] = one_pokemon.pokemon_info['spatk']
        # pokemon_dict['spdef'] = one_pokemon.pokemon_info['spdef']
        # pokemon_dict['speed'] = one_pokemon.pokemon_info['speed']
        # pokemons.append(pokemon_dict)
        one_pokemon = pokemon.pokemon_info
        one_pokemon['key'] = pokemon_index
        pokemons.append(one_pokemon)

    return render_template('mainpage/repertory/repertory.html', pokemons=pokemons)


# 详细的pokemon信息
@app.route('/main/repertory_<id>/')
def repertory_detail(id=None):
    id = int(id)
    rid = user.user_info['role_id_list'][0]
    role.load(rid)
    pokemon = Pokemon()
    pokemon.load(id)
    hd = handbook()
    equipments = []
    for eq in pokemon.pokemon_info['equipment']:
        hd.load_equipment(eq)
        one_equipment={}
        one_equipment['name'] = hd.equipment['name']
        one_equipment['id'] = eq
        equipments.append(one_equipment)

    empty_equipments = []

    # 添加装备
    from gameflask.code.backpack import Backpack
    bp = Backpack()
    bp_id = role.role_info['backpack_id']
    bp.load(bp_id)
    equipment_ids = bp.backpack['equipment_lst']
    for i, eq in enumerate(equipment_ids):
        hd = handbook()
        if eq[1]==-1:
            one_empty_equipment = {}
            one_empty_equipment['id'] = eq[0]
            dprint(one_empty_equipment)
            hd.load_equipment(eq[0])
            one_empty_equipment['name'] = hd.equipment['name']
            empty_equipments.append(one_empty_equipment)

    url = "https://img.pokemondb.net/artwork/large/" + pokemon.pokemon_info['name'].lower() + ".jpg"

    return render_template("mainpage/repertory/repertory_detail.html",poke_id=id,url=url, moves=pokemon.pokemon_info['moves'], equipments=equipments,
                           empty_equipments=empty_equipments,
                           one_pokemon=pokemon.pokemon_info)


@app.route('/main/equipment')
def showequipment():
    rid = user.user_info['role_id_list'][0]
    role.load(rid)
    bp_id = role.role_info['backpack_id']
    from gameflask.code.backpack import Backpack
    bp = Backpack()

    bp.load(bp_id)

    equipment_ids = bp.backpack['equipment_lst']
    _equipments = [None for i in range(len(equipment_ids))]
    print('isa', equipment_ids)
    from gameflask.code.pokemon import Pokemon
    for i, eq in enumerate(equipment_ids):
        hd = handbook()

        hd.load_equipment(eq[0])
        pok = Pokemon()
        pok.load(eq[1])
        hd.equipment['owner'] = pok.pokemon_info['name']

        _equipments[i] = hd.equipment
        print(_equipments)

    return render_template('mainpage/equipment/equipment.html', equipments=_equipments)

@app.route('/main/equipment_down', methods=['POST', 'GET'])
def equipment_down():
    eq_id = int(request.args.get('eq_id'))
    poke_id = int(request.args.get('poke_id'))

    id = int(poke_id)
    rid = user.user_info['role_id_list'][0]
    role.load(rid)
    pokemon = Pokemon()
    pokemon.load(id)

    bp_id = role.role_info['backpack_id']
    pokemon.unequip(bp_id, eq_id)
    pokemon.load(id)

    hd = handbook()
    equipments = []
    for eq in pokemon.pokemon_info['equipment']:
        hd.load_equipment(eq)
        one_equipment = {}
        one_equipment['name'] = hd.equipment['name']
        one_equipment['id'] = eq
        equipments.append(one_equipment)

    empty_equipments = []

    # 添加装备
    from gameflask.code.backpack import Backpack
    bp = Backpack()
    bp_id = role.role_info['backpack_id']
    bp.load(bp_id)
    equipment_ids = bp.backpack['equipment_lst']
    for i, eq in enumerate(equipment_ids):
        hd = handbook()
        if eq[1] == -1:
            one_empty_equipment = {}
            one_empty_equipment['id'] = eq[0]
            hd.load_equipment(eq[0])
            one_empty_equipment['name'] = hd.equipment['name']
            empty_equipments.append(one_empty_equipment)

    url = "https://img.pokemondb.net/artwork/large/" + pokemon.pokemon_info['name'].lower() + ".jpg"

    return render_template("mainpage/repertory/repertory_detail.html", poke_id=id, url=url,
                           moves=pokemon.pokemon_info['moves'], equipments=equipments,
                           empty_equipments=empty_equipments,
                           one_pokemon=pokemon.pokemon_info)


@app.route('/main/equipment_up', methods=['POST', 'GET'])
def equipment_up():
    eq_id = int(request.values.get('eq_id'))
    poke_id = int(request.args.get('poke_id'))

    id = int(poke_id)
    rid = user.user_info['role_id_list'][0]
    role.load(rid)
    pokemon = Pokemon()
    pokemon.load(id)

    print("up_id",id)
    print("up_poke_id",pokemon.pokemon_id)

    bp_id = role.role_info['backpack_id']
    pokemon.equip(bp_id, eq_id)
    pokemon.load(id)

    hd = handbook()
    equipments = []
    for eq in pokemon.pokemon_info['equipment']:
        hd.load_equipment(eq)
        one_equipment = {}
        one_equipment['name'] = hd.equipment['name']
        one_equipment['id'] = eq
        equipments.append(one_equipment)

    empty_equipments = []

    # 添加装备
    from gameflask.code.backpack import Backpack
    bp = Backpack()
    bp_id = role.role_info['backpack_id']
    bp.load(bp_id)
    equipment_ids = bp.backpack['equipment_lst']
    for i, eq in enumerate(equipment_ids):
        hd = handbook()
        if eq[1] == -1:
            one_empty_equipment = {}
            one_empty_equipment['id'] = eq[0]
            hd.load_equipment(eq[0])
            one_empty_equipment['name'] = hd.equipment['name']
            empty_equipments.append(one_empty_equipment)

    url = "https://img.pokemondb.net/artwork/large/" + pokemon.pokemon_info['name'].lower() + ".jpg"

    return render_template("mainpage/repertory/repertory_detail.html", poke_id=id, url=url,
                           moves=pokemon.pokemon_info['moves'], equipments=equipments,
                           empty_equipments=empty_equipments,
                           one_pokemon=pokemon.pokemon_info)

@app.route('/main/tool')
def showtool():
    rid = user.user_info['role_id_list'][0]
    role.load(rid)
    bp_id = role.role_info['backpack_id']
    from gameflask.code.backpack import Backpack
    bp = Backpack()
    item_list = bp.show_item_lst(bp_id)

    tool = {
        'red0_num': 0,
        'red1_num': 0,
        'blue_num': 0,
        'W_num': 0
    }
    for x in item_list:
        if x[0] == 1:
            tool['red0_num'] = x[1]
        elif x[0] == 2:
            tool['red1_num'] = x[1]
        elif x[0] == 3:
            tool['blue_num'] = x[1]
        else:
            tool['W_num'] = x[1]

    return render_template('mainpage/tool/tool.html', tool=tool)

@app.route('/main/tool_buy<tool_id>')
def toolbuy(tool_id):
    rid = user.user_info['role_id_list'][0]
    role.load(rid)
    bp_id = role.role_info['backpack_id']
    from gameflask.code.backpack import Backpack
    bp = Backpack()

    tool_id = int(tool_id)

    money = role.role_info['money']
    if(tool_id==1):mm = 200
    elif(tool_id==2):mm = 500
    elif(tool_id==3):mm = 500
    elif(tool_id==4):mm = 1000

    if(money > mm):
        role.role_info['money'] = money-mm
        role.storage()
        bp.add_item(bp_id,tool_id)
    item_list = bp.show_item_lst(bp_id)

    tool = {
        'red0_num': 0,
        'red1_num': 0,
        'blue_num': 0,
        'W_num': 0
    }
    for x in item_list:
        if x[0] == 1:
            tool['red0_num'] = x[1]
        elif x[0] == 2:
            tool['red1_num'] = x[1]
        elif x[0] == 3:
            tool['blue_num'] = x[1]
        else:
            tool['W_num'] = x[1]

    return render_template('mainpage/tool/tool.html', tool=tool)



@app.route('/user/userpage')
def userpage():
    uid = user.uid
    role_id_list = user.user_info["role_id_list"][0]
    role.load(role_id_list)
    role_info = role.role_info
    user_info = user.user_info

    return render_template('user/userpage.html', user=user_info, uid=user.uid, role=role_info)


# 改变角色信息
@app.route('/user/role_change')
def role_change():
    return render_template('user/role_change.html')


@app.route('/user/role_change_over', methods=['POST', 'GET'])
def role_change_over():
    if request.method == 'POST':
        role_name = request.form['role_name']

        uid = user.uid
        role_id_list = user.user_info["role_id_list"][0]
        role.load(role_id_list)

        role.role_info['name'] = role_name
        role.storage()

        role_info = role.role_info
        user_info = user.user_info

        return render_template('user/userpage.html', user=user_info, uid=user.uid, role=role_info)


# 改变用户信息
@app.route('/user/user_change')
def user_change():
    return render_template('user/user_change.html')


@app.route('/user/user_change_over', methods=['POST', 'GET'])
def user_change_over():
    if request.method == 'POST':
        passwd = request.form['passwd']

        uid = user.uid
        user.user_info['passwd'] = passwd
        user.storage()

        role_id_list = user.user_info["role_id_list"][0]
        role.load(role_id_list)
        role_info = role.role_info
        user_info = user.user_info

        return render_template('user/userpage.html', user=user_info, uid=user.uid, role=role_info)


@app.route('/main/logout')
def logout():
    return render_template('index.html')


# 程序入口
if __name__ == "__main__":
    app.run(host='localhost')
