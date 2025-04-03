import random
class Dwarf(object):
    def __init__(self, name):
        self.name = name
        self.attack = 3
        self.defend = 4
        self.body = 5
    def talk(self):
        print("I'm a blade-man, I'll cut ya!!!")

lenn = Dwarf("Lenn") 
print(f"Dwarf name = {lenn.name}")
print(f"Lenn's attack strength = {lenn.attack}")
lenn.talk()

class Elf(object):
    def __init__(self, name):
        self.name = name
        self.attack = 4
        self.defend = 4
        self.body = 4

esseden = Elf("Esseden")
print(f"Elf name = {esseden.name}")
print(f"Esseden body value = {esseden.body}")

lenn_attack_roll = random.randrange(1, lenn.attack + 1)
print(f"Lenn attack roll = {lenn_attack_roll}")

esseden_defend_roll = random.randrange(1, esseden.defend + 1)
print(f"Esseden defend roll = {esseden_defend_roll}")

damage = lenn_attack_roll - esseden_defend_roll
if damage > 0:
    esseden.body -= damage
print(f"Esseden body value = {esseden.body}")
    