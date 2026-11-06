from Characters import *
from random import randint
from Team import *


n_char_type = 7  # [CHANGED] Five original classes + Assassin + Bard.
gold = 2000    # Gold for you to recruit characters
min_cost = 100  # A hack for user_choose_team()

'''
Type:
1: Fighter (Given)
2: Mage (Given)
3: Berserker 
4: ArchMage
5: Necromancer
6: Assassin
7: Bard
'''


def create_char(i):
    if i == 1:
        return Fighter()
    elif i == 2:
        return Mage()
    elif i == 3:
        return Berserker()
    elif i == 4:
        return ArchMage()
    elif i == 5:
        return Necromancer()
    # [NEW] Register Assassin and Bard.
    elif i == 6:
        return Assassin()
    elif i == 7:
        return Bard()



def create_rand_team(gold):
    team = Team()  # [CHANGED] Store Bard's buff alongside members.
    while gold >= min_cost:  # [CHANGED] Stop when no class is affordable.
        temp_char = create_char(randint(1, n_char_type))
        if gold >= temp_char.cost:
            gold -= temp_char.cost
            team.append(temp_char)
    return team


def user_choose_team(gold):
    team = Team()  # [CHANGED] Store Bard's buff alongside members.
    choice = -1
    while (gold >= min_cost) and (gold != 0):
        print("\nYour current team:")
        print_stat(team)
        print(f'\nYou have {gold} gold currently')
        choice = -1
        while choice < 1 or choice > n_char_type:
            print("Choices:")
            print(f"1: Fighter (cost: {Fighter().cost})")
            print(f"2: Mage (cost: {Mage().cost})")
            print(f"3: Berserker (cost: {Berserker().cost})")
            print(f"4: ArchMage (cost: {ArchMage().cost})")
            print(f"5: Necromancer (cost: {Necromancer().cost})")
            # [NEW] Show both new classes in the recruitment menu.
            print(f"6: Assassin (cost: {Assassin().cost})")
            print(f"7: Bard (cost: {Bard().cost})")
            try:  # [CHANGED] Retry non-integer input.
                choice = int(input(f'Input a choice from 1 to {n_char_type}:'))
            except ValueError:
                print('Please enter an integer.')
                continue
            if choice < 1 or choice > n_char_type:
                print(
                    f"Your choice {choice} is not valid. Please choose again")
        if choice > 0 and choice <= n_char_type:
            temp_char = create_char(choice)
            if gold >= temp_char.cost:
                gold -= temp_char.cost
                team.append(temp_char)
            else:
                print('Not enough gold for this character.')  # [NEW] Explain failed purchase.
    return team


def run_battle(team_a, team_b, pause=True, max_rounds=1000):
    # [CHANGED] 0 = A wins, 1 = B wins, -1 = draw (e.g. Bard-only teams).

    rd = 0
    ATurn = True
    dprint("")
    dprint("THE BATTLE STARTS!!!!!")

    while (not all_dead(team_a)) and not all_dead(team_b):
        if ATurn and rd >= max_rounds:
            dprint('Round limit reached: draw.')
            return -1
        dprint('')

        if ATurn:
            my_team = team_a
            enemy = team_b
            rd += 1
            dprint(f'Round {rd}')
        else:
            my_team = team_b
            enemy = team_a

        if print_action_description:
            print("Team A:")
            print_stat(team_a)
            print()
            print("Team B:")
            print_stat(team_b)

        dprint('')
        
        # [CHANGED] Turn flow: status -> choose Action -> boost -> execute.
        attacker = rand_alive(my_team)
        team_s = 'Team A' if ATurn else 'Team B'
        actor = my_team[attacker] 

        dprint(team_s + f' member {attacker} {actor.name} acts')

        # [NEW] 1. Tick the selected actor's poison.
        actor.begin_turn()

        # [CHANGED] Poison death skips BOTH boosting and execution.
        if actor.alive:
            # [CHANGED] 2. Create the action without executing its effect.
            action = actor.create_action(my_team, enemy)

            # [NEW] 3. Consume song once; Bard actions keep it pending.
            if my_team.double_next_action and not isinstance(actor, Bard):
                action.amplify()
                my_team.double_next_action = False
                dprint("Bard's song doubles this action!")

            # [CHANGED] 4. Execute the final, possibly boosted action.
            action.execute()
        

        ATurn = not ATurn
        if pause:
            input("Press Enter to continue....")

    if all_dead(team_b):
        dprint("Frist team won!")
        return 0
    else:
        dprint("Second team won!")
        return 1


def game_start(gold, pause=True):
    enemy = create_rand_team(gold)
    print("Your enemy will be:")
    print_stat(enemy)
    my_team = user_choose_team(gold)
    result = run_battle(my_team, enemy, pause)
    if result == 0:
        print("Congrats! You won!")
    elif result == -1:  # [NEW] Report the round-limit draw.
        print('Draw: round limit reached.')
    else:
        print("Sorry, you lose")

if __name__ == "__main__":
    game_start(gold, False)  # False = no pause between turns.
