# [NEW] Action system: characters choose; Battle boosts; Actions execute.
from random import choice

# [NEW] Shared interface; each action defines its own doubling rule.
class Action:
    def amplify(self):
        return self

    def execute(self):
        raise NotImplementedError


# [NEW] Fighter/Mage damage; Bard doubles damage. Preserve enemy index.
class DamageAction(Action):
    def __init__(self, actor, target, damage, dprint, target_index):
        self.actor = actor
        self.target = target
        self.damage = damage
        self.target_index = target_index
        self.dprint = dprint

    def amplify(self):
        self.damage *= 2
        return self

    def execute(self):
        self.dprint(f'Hurt enemy {self.target_index} ({self.target.name}) by damage {self.damage}.')
        self.target.got_hurt(self.damage)


# [NEW] ArchMage area damage; Bard doubles damage for each living enemy.
class MultiDamageAction(Action):
    def __init__(self, actor, targets, damage, dprint):
        self.actor = actor
        self.targets = targets
        self.damage = damage
        self.dprint = dprint

    def amplify(self):
        self.damage *= 2
        return self

    def execute(self):
        self.dprint(f'{self.actor.name} attacks every enemy for {self.damage} damage!')
        for index, target in enumerate(self.targets):
            if target.alive:
                self.dprint(f'Hurt enemy {index} ({target.name}) by damage {self.damage}.')
                target.got_hurt(self.damage)


# [NEW] Mage recovery; Bard doubles recovery, capped at max mana.
class ManaRecoveryAction(Action):
    def __init__(self, actor, amount, dprint):
        self.actor = actor
        self.amount = amount
        self.dprint = dprint

    def amplify(self):
        self.amount *= 2
        return self

    def execute(self):
        self.actor.mana = min(self.actor.maxmana, self.actor.mana + self.amount)
        self.dprint(f'{self.actor.name} recovers mana to {self.actor.mana}.')


# [NEW] Necromancer revival; Bard doubles count (1 -> 2), not restored HP.
class ReviveAction(Action):
    def __init__(self, team, count, hp_ratio, dprint):
        self.team = team
        self.count = count
        self.hp_ratio = hp_ratio
        self.dprint = dprint

    def amplify(self):
        self.count *= 2
        return self

    def execute(self):
        dead_members = [member for member in self.team if not member.alive]
        candidates = dead_members.copy()
        for _ in range(min(self.count, len(candidates))):
            member = choice(candidates)
            candidates.remove(member)
            member.hp = int(member.max_hp * self.hp_ratio)
            member.alive = True
            self.dprint(f'Revived member {self.team.index(member)} ({member.name}) with hp {member.hp}.')


# [NEW] Target-owned state: tick only on its actions; expire after 3 or death.
class PoisonEffect:
    def __init__(self, turns, damage_ratio, dprint, target_index):
        self.turns = turns
        self.target_index = target_index
        self.damage_ratio = damage_ratio
        self.dprint = dprint

    def on_before_act(self, character):
        damage = int(character.max_hp * self.damage_ratio)
        self.dprint(f'Member {self.target_index} ({character.name}) takes {damage} poison damage ({self.turns} poison turns remaining).')
        character.got_hurt(damage)
        self.turns -= 1
        return character.alive and self.turns > 0


# [NEW] Apply poison; Bard doubles damage ratio (20% -> 40%), not duration.
class PoisonAction(Action):
    def __init__(self, actor, target, turns, damage_ratio, dprint, target_index):
        self.actor = actor
        self.target = target
        self.turns = turns
        self.target_index = target_index
        self.damage_ratio = damage_ratio
        self.dprint = dprint

    def amplify(self):
        self.damage_ratio *= 2
        return self

    def execute(self):
        # [NEW] Reapplication replaces poison; effects do not stack.
        self.target.effects = [effect for effect in self.target.effects if not isinstance(effect, PoisonEffect)] # Move
        self.target.effects.append(PoisonEffect(self.turns, self.damage_ratio, self.dprint, self.target_index)) # Add new one
        self.dprint(f'{self.actor.name} poisons enemy {self.target_index} ({self.target.name}) for {self.turns} turns.')


# [NEW] Team-owned buff: wait for one non-Bard action; songs do not stack.
class SongAction(Action):
    def __init__(self, team, dprint):
        self.team = team
        self.dprint = dprint

    def execute(self):
        self.team.double_next_action = True
        self.dprint('Bard sings: the next non-Bard action will be doubled!')
