from random import choice

# [NEW] Keep list behaviour while storing Bard's pending team buff.
class Team(list):
    def __init__(self):
        super().__init__()

        # [NEW] Consumed by one non-Bard action, not by elapsed rounds.
        self.double_next_action = False


# [CHANGED] Pick an alive index without recursion; requires a living member.
def rand_alive(team):
    return choice([i for i, member in enumerate(team) if member.alive])


# [CHANGED] Pick a dead index without recursion; requires a dead member.
def rand_death(team):
    return choice([i for i, member in enumerate(team) if not member.alive])

# All members dead?
def all_dead(team):
    for i in team:
        if i.alive:
            return False
    return True


# All members alive?
def all_alive(team):
    for i in team:
        if not i.alive:
            return False
    return True


# Display column width.
len_longest_name = 11


# Display team stats.
def print_stat(team):
    if team == []:
        print("(Currently no member in the team now)")
        return

    indices = 'Index:     '  # [NEW] Match zero-based attack-log indices.
    names = 'Members:   '
    hp = 'Hitpoints: '
    sth = 'Strength:  '
    maxm = 'Max. Mana: '
    mana = 'Current M: '

    for index, i in enumerate(team):
        indices += '|' + str(index).rjust(len_longest_name)
        nspace = len_longest_name - len(i.name)
        names += '|' + ' '*nspace + i.name
        nspace = len_longest_name - len(str(i.hp))
        hp += '|' + ' '*nspace + str(i.hp)
        if i.str:
            nspace = len_longest_name - len(str(i.str))
            sth += '|' + ' '*nspace + str(i.str)
        else:
            sth += '|' + ' '*len_longest_name
        if i.maxmana:
            nspace = len_longest_name - len(str(i.maxmana))
            maxm += '|' + ' '*nspace + str(i.maxmana)
        else:
            maxm += '|' + ' '*len_longest_name

        if i.mana:
            nspace = len_longest_name - len(str(i.mana))
            mana += '|' + ' '*nspace + str(i.mana)
        else:
            mana += '|' + ' '*len_longest_name

    print(indices)
    print(names)
    print(hp)
    print(sth)
    print(maxm)
    print(mana)
