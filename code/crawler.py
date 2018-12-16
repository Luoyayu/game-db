import bs4
from bs4 import BeautifulSoup
import requests

source = requests.get("https://pokemondb.net/pokedex/abra")
soup = BeautifulSoup(source.text, "html.parser")

Type = []
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
growth_rate = ""
ev_yield = ""
egg_groups = ""
gender = ""
egg_cycles = 0

# print(soup.prettify())
for tbody in soup.find_all('tbody'):
    for th in tbody.children:
        if isinstance(th, bs4.element.NavigableString):
            continue
        # print(th)
        # print(type(th))
        for ch in th.children:

            if isinstance(ch, bs4.element.NavigableString):
                continue
            # print(ch)
            if ch.string == "Type":
                # print("IN Type!!!!!!!!")
                # print(ch.next_sibling.next_sibling.contents[1].string)
                # print(ch.next_sibling.next_sibling.contents[3].string)

                Type.append(ch.next_sibling.next_sibling.contents[1].string)
                try:
                    Type.append(ch.next_sibling.next_sibling.contents[3].string)
                except IndexError:
                    pass

            if ch.string == "Height":
                rawString = ch.next_sibling.next_sibling.string
                # print(rawString)
                st = ch.next_sibling.next_sibling.string.find(' ')
                try:
                    # print(float(rawString[st + 2: len(rawString) - 3]))
                    Height = float(rawString[st + 2: len(rawString) - 3])
                except ValueError as e:
                    print(e)
                    exit("!")

            if ch.string == "Weight":
                rawString = ch.next_sibling.next_sibling.string
                # print(rawString)
                st = ch.next_sibling.next_sibling.string.find(' ')
                try:
                    # print(float(rawString[st + 2: len(rawString) - 3]))
                    Weight = float(rawString[st + 2: len(rawString) - 3])
                except ValueError as e:
                    print(e)
                    exit("!")

            if ch.string == "Abilities":
                rawString = ch.next_sibling.next_sibling
                spanas = rawString.span.a
                cnt = 0
                for s in spanas.strings:
                    if cnt == 0: main_Abilities = s;
                    if cnt == 1: vice_Abilities = s;
                    cnt += 1
                    if cnt >= 2: break

            if ch.string == "HP":
                rawString = ch.next_sibling.next_sibling
                HP = rawString.string

            if ch.string == 'Attack':
                rawString = ch.next_sibling.next_sibling
                SpATK = rawString.string

            if ch.string == 'Defense':
                rawString = ch.next_sibling.next_sibling
                defense = rawString.string

            if ch.string == "Sp. Atk":
                rawString = ch.next_sibling.next_sibling
                SpATK = rawString.string

            if ch.string == 'Sp. Def':
                rawString = ch.next_sibling.next_sibling
                SpDef = rawString.string

            if ch.string == "Speed":
                rawString = ch.next_sibling.next_sibling
                speed = rawString.string

            if ch.string == ""

print(Type)
print(Height)
print(Weight)
print("主属性 ", main_Abilities)
print('副属性 ', vice_Abilities)
print(HP)
print(SpATK)
print("\n")
