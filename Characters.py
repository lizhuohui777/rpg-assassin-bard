from random import randint
from Team import *
from Actions import *  # [NEW] Shared action types.

print_action_description = True

def dprint(s):
    if print_action_description:
        print(s)


# Constants for Mage Type
mana_cost = 20
mana_recovery = 30


class Character(object):
    def __init__(self):
        self.name = ''
        self.max_hp = 1000
        self.hp = 1000
        self.str = 0
        self.maxmana = 0
        self.mana = 0
        self.cost = 9999999999
        self.alive = True
        self.effects = []  # [NEW] Status effects belong to this character.

    # [NEW] Return an Action so Battle can boost it before execution.
    def create_action(self, my_team, enemy):
        raise NotImplementedError

    def act(self, my_team, enemy):
        # [CHANGED] Legacy direct call; Battle handles poison and Bard separately.
        action = self.create_action(my_team, enemy)
        action.execute()

    # [NEW] Tick statuses on this character's turn; remove expired effects.
    def begin_turn(self):
        active_effects = []

        for effect in self.effects[:]:  # [CHANGED] Death may clear the original list.
            if effect.on_before_act(self):
                active_effects.append(effect)
            if not self.alive:
                self.effects.clear()
                return

        self.effects = active_effects

    def got_hurt(self, damage):
        if damage >= self.hp:
            self.hp = 0
            self.alive = False
            self.effects.clear()  # [NEW] Death ends poison, even if revived later.
            dprint(self.name + ' died!')
        else:
            self.hp -= damage
            dprint(self.name +
                   f' hurt with remaining hp {self.hp}.')


class Fighter(Character):
    def __init__(self):
        super().__init__()
        self.name = 'Fighter'
        self.max_hp = 1200
        self.hp = 1200
        self.str = 100
        self.cost = 100

    def create_action(self, my_team, enemy):
        # [CHANGED] Return damage instead of applying it; retain enemy index.
        index = rand_alive(enemy)
        return DamageAction(self, enemy[index], self.str, dprint, index)


class Mage(Character):
    def __init__(self):
        super().__init__()
        self.name = 'Mage'
        self.maxmana = 50
        self.mana = 50
        self.max_hp = 800
        self.hp = 800
        self.cost = 200
        self.int = 400

    def create_spell_action(self, my_team, enemy):
        # [CHANGED] Spell selection returns an Action for Bard to boost.
        index = rand_alive(enemy)
        return DamageAction(self, enemy[index], self.int, dprint, index)

    def create_action(self, my_team, enemy):
        if self.mana < mana_cost:
            # [CHANGED] Recovery is also a boostable Action.
            return ManaRecoveryAction(self, mana_recovery, dprint)
        self.mana -= mana_cost  # Cost is paid once, even when boosted.
        return self.create_spell_action(my_team, enemy)



class Berserker(Fighter):
    def __init__(self):
        super().__init__()
        self.name = 'Berserker'
        self.cost = 200
    
    def create_action(self, my_team, enemy):
        if self.hp <= self.max_hp / 2:
            self.str = 200
            dprint('Berserk mode! Attack double!')
        else:
            self.str = 100
        # [CHANGED] Keep berserk rules; return Fighter's boostable Action.
        return super().create_action(my_team, enemy)
    

class ArchMage(Mage):
    def __init__(self):
        super().__init__()
        self.name = 'ArchMage'
        self.cost = 600
        self.int = 400

    def create_spell_action(self, my_team, enemy):
        if sum(member.alive for member in my_team) > 1:
            return super().create_spell_action(my_team, enemy)
        # [CHANGED] Return area Action; full team keeps original enemy indices.
        return MultiDamageAction(self, enemy, self.int * 2, dprint)

class Necromancer(Mage):
    def __init__(self):
        super().__init__()
        self.name = 'Necromancer'
        self.cost = 400

    def create_spell_action(self, my_team, enemy):
        if not all_alive(my_team):
            # [CHANGED] Revival is an Action; Bard can increase its target count.
            return ReviveAction(my_team, count=1, hp_ratio=0.5, dprint=dprint)
        return super().create_spell_action(my_team, enemy)


# [NEW] Assassin: 900 HP, 300 gold; poison one enemy for 3 of its actions.
class Assassin(Character):
    def __init__(self):
        super().__init__()
        self.name = 'Assassin'
        self.max_hp = 900
        self.hp = 900
        self.cost = 300

    def create_action(self, my_team, enemy):
        index = rand_alive(enemy)
        return PoisonAction(self, enemy[index], turns=3, damage_ratio=0.20,
                            dprint=dprint, target_index=index)


# [NEW] Bard: 800 HP, 300 gold; boost the next non-Bard teammate's action.
class Bard(Character):
    def __init__(self):
        super().__init__()
        self.name = 'Bard'
        self.max_hp = 800
        self.hp = 800
        self.cost = 300

    def create_action(self, my_team, enemy):
        return SongAction(my_team, dprint)
