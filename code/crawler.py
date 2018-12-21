import bs4
from bs4 import BeautifulSoup
import requests


# https://img.pokemondb.net/artwork/+pokemon_name(小写)

def Craw_pokemon(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    source = requests.get("https://pokemondb.net/pokedex/" + name, headers=headers)
    # print(source.status_code)
    if source.status_code == 404:
        return "NAME_NOT_EXISTED"
    soup = BeautifulSoup(source.text, "html.parser")

    Type = []
    moves = []
    Local = 0
    Species = ""
    Height = 0
    Weight = 0
    main_Abilities = ""
    vice_Abilities = ""
    HP = 0
    ATK = 0
    defense = 0
    SpATK = 0
    SpDef = 0
    speed = 0

    catch_rate = 0
    friendship = 0
    base_exp = 0
    growth_rate = ""
    ev_yield = ""
    egg_groups = ""
    gender = ""
    egg_cycles = 0

    # print(soup.prettify())
    # exit()

    Type_cnt = 0
    Egg_Groups_cnt = 0
    Egg_cycles_cnt = 0
    Abilities_cnt = 0

    for tbody in soup.find_all('tbody'):
        for th in tbody.children:
            if isinstance(th, bs4.element.NavigableString):
                continue
            # print(th)
            # print(type(th))
            for ch in th.children:
                if isinstance(ch, bs4.element.NavigableString):
                    continue
                # print(ch.string)

                try:
                    rawString = ch.next_sibling.next_sibling.string
                except AttributeError:
                    rawString = None

                if ch.string == "Type" and Type_cnt == 0:
                    Type_cnt += 1
                    Type.append(ch.next_sibling.next_sibling.contents[1].string)
                    try:
                        Type.append(ch.next_sibling.next_sibling.contents[3].string)
                    except IndexError:
                        pass

                elif ch.string == "Species":
                    Species = rawString

                elif ch.string == "Height":
                    st = rawString.find(' ')
                    try:
                        Height = float(rawString[st + 2: len(rawString) - 3])
                    except ValueError as e:
                        print(e)

                elif ch.string == "Weight":
                    st = rawString.find('(')
                    try:
                        Weight = float(rawString[st + 1: len(rawString) - 3])
                    except ValueError as e:
                        print(e)

                elif ch.string == "Abilities" and Abilities_cnt == 0:
                    Abilities_cnt = 1
                    rawString = ch.next_sibling.next_sibling
                    cnt, lst = 0, ''
                    for s in rawString.strings:
                        if lst == '1' and cnt == 0:
                            main_Abilities = s
                            cnt = 1
                        if lst == '2' and cnt == 1:
                            vice_Abilities = s
                            break
                        if s[0].isdigit() and lst == s[0]:
                            break
                        elif s[0].isdigit():
                            lst = s[0]

                elif ch.string == "HP":
                    HP = int(rawString)

                elif ch.string == 'Attack':
                    ATK = int(rawString)

                elif ch.string == 'Defense':
                    defense = int(rawString)

                elif ch.string == "Sp. Atk":
                    SpATK = int(rawString)

                elif ch.string == 'Sp. Def':
                    SpDef = int(rawString)

                elif ch.string == "Speed":
                    speed = int(rawString)

                elif ch.string == "Catch rate":
                    rawString = ch.next_sibling.next_sibling
                    catch_rate = int(rawString.contents[0])

                elif ch.a and ch.a.string == "Friendship":
                    try:
                        friendship = int(ch.next_sibling.next_sibling.contents[0])
                    except ValueError:
                        friendship = None

                elif ch.string == "Base Exp.":
                    base_exp = int(rawString)

                elif ch.string == "Growth Rate":
                    growth_rate = rawString

                elif ch.string == "Gender":
                    rawString = ch.next_sibling.next_sibling
                    gender = rawString.contents[0].string

                elif ch.string == "EV yield":
                    ev_yield = rawString.strip()

                elif ch.string == "Egg Groups" and Egg_Groups_cnt == 0:
                    for s in ch.next_sibling.next_sibling.strings:
                        if s == '\n': continue
                        egg_groups += s


                elif ch.a and ch.a.string == "Egg cycles" and Egg_cycles_cnt == 0:
                    Egg_cycles_cnt += 1
                    egg_cycles = int(ch.next_sibling.next_sibling.contents[0])

                elif ch.string == "Local №":
                    Local = int(ch.next_sibling.next_sibling.contents[0].string)

    import re

    for x in soup.find_all(href=re.compile("/move/.")):
        moves.append(x.string)
        if len(moves) == 4: break

    #
    # print('姓名', name)
    # print('类型', Type)
    # print("物种", Species)
    # print('身高', Height)
    # print('体重', Weight)
    # print("主属性 ", main_Abilities)
    # print('副属性 ', vice_Abilities)
    # print('HP', HP)
    # print('ATK', ATK)
    # print('defense', defense)
    # print('SpATK', SpATK)
    # print('SpDef', SpDef)
    # print('speed', speed)
    #
    # print('catch_rate', catch_rate)
    # print('friendship', friendship)
    # print('base_exp', base_exp)
    # print('growth_rate', growth_rate)
    # print('ev_yield', ev_yield)
    # print('egg_groups', egg_groups)
    # print('gender', gender)
    # print('egg_cycles', egg_cycles)
    # print("Local", Local)
    # print('move', moves)
    # print("\n")

    pokemon = {
        "name": name,  # 姓名
        "type": Type,  # 类型
        "species": Species,  # 物种
        "height": Height,  # 身高
        "weight": Weight,  # 体重
        "main_ability": main_Abilities,  # 主属性
        "vice_ability": vice_Abilities,  # 副属性
        "hp": HP,  # 生命值
        "atk": ATK,  # 攻击值
        "def": defense,  # 防御值
        "spatk": SpATK,  # 特攻值
        "spdef": SpDef,  # 特防值
        "speed": speed,  # 速度
        "catch_rate": catch_rate,  # 捕获率
        "friendship": friendship,  # 友谊值
        "base_exp": base_exp,  # 基础经验值
        "growth_rate": growth_rate,  # 成长率
        "ev_yield": ev_yield,
        "egg_groups": egg_groups,  # 蛋组
        "egg_cycles": egg_cycles,  # 蛋群周期
        "gender": gender,  # 性别分布
        "location": Local,  # 可捕获位置
        "moves": moves  # 招式
    }
    import json
    with open("pokemon.json", "w") as f:
        json.dump(pokemon, f)
    # print("saved")
    return 0


def Craw_move(name):
    Type = ""
    Category = ""
    Power = 0
    Accuracy = None
    PP = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    source = requests.get("https://pokemondb.net/move/" + name, headers=headers)
    # print(source.status_code)
    if source.status_code == 404:
        return "MOVE_NOT_EXISTED"
    soup = BeautifulSoup(source.text, "html.parser")
    # print(soup.prettify())
    # exit()

    for tbody in soup.find_all('tbody'):
        for th in tbody.children:
            if isinstance(th, bs4.element.NavigableString):
                continue
            for ch in th.children:
                if isinstance(ch, bs4.element.NavigableString):
                    continue
                # print(ch)

                if ch.string == "Type":
                    Type = ch.next_sibling.next_sibling.string

                elif ch.string == "Category":
                    for s in ch.next_sibling.next_sibling.strings:
                        Category = s.strip()
                        break
                elif ch.string == "Power":
                    try:
                        Power = int(ch.next_sibling.next_sibling.string)
                    except ValueError:
                        Power = None
                elif ch.string == "Accuracy":
                    try:
                        Accuracy = int(ch.next_sibling.next_sibling.string)
                    except ValueError:
                        Accuracy = None
                        if "∞" == ch.next_sibling.next_sibling.string:
                            Accuracy = "∞"
                elif ch.string == 'PP':
                    for s in ch.next_sibling.next_sibling.strings:
                        PP = int(s)
                        break
    # print("招式名", name)
    # print('类型', Type)
    # print('分类', Category)
    # print('威力', Power)
    # print('命中', Accuracy)
    # print('pp值', PP)
    move = {
        "name": name.replace('-', ' '),  # 招式名
        "type": Type,  # 类型
        "category": Category,  # 分类
        "power": Power,  # 威力
        "accuracy": Accuracy,  # 命中,
        "pp": PP  # PP 值
    }

    import json
    with open("move.json", "w") as f:
        json.dump(move, f)
    # print("saved")
    return 0


if __name__ == '__main__':
    Craw_move("Tackle")
