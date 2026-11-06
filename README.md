# RPG: Assassin and Bard

## Run

Requires Python 3. No external packages are needed.

```sh
python3 battle.py
```

Choose characters by entering their menu numbers. Enemy indices start at 0.

## Goal

I added Assassin and Bard to practise managing status-effect lifecycles.

## New characters

- **Assassin:** 900 HP, 300 gold. Poison deals 20% max HP before each of the enemy's next three actions. It ends after three triggers or death.
- **Bard:** 800 HP, 300 gold. No direct damage; doubles the next non-Bard teammate's action.

## Three types of classes

1. **Character:** stores attributes and chooses actions. `self.effects` holds status objects. `begin_turn()` triggers all current effects.
2. **Action:** represents one action. `create_action()` creates it, `amplify()` boosts it, and `execute()` performs it.
3. **Status effect:** stays on a character across turns. `PoisonEffect` stores damage ratio and remaining triggers. `on_before_act()` defines what the effect does before the character acts.

I separated actions from effects because poisoning happens once, but the poison needs to stay on the enemy for later turns.

## Team state

`Team(list)` works like a list and also stores `self.double_next_action`. Poison stays on the enemy; Bard's buff stays on the team until used. Reapplying poison replaces the old poison; songs do not stack.

## Bard's boost

- Fighter/Berserker: damage ×2.
- Mage/ArchMage: spell damage ×2, including area damage.
- Mana recovery: recovery ×2, capped at max mana.
- Necromancer: revive up to 2 teammates instead of 1.
- Assassin: poison damage 20% → 40%; still three triggers.

## Cost

I chose 300 gold as a starting point because both effects are useful, but poison takes time and Bard needs teammates. Balance needs more testing.

## Files

- `Characters.py`: character decisions and status management.
- `Actions.py`: action execution, boosts, and poison effects.
- `Team.py`: team state and helpers.
- `battle.py`: recruitment and turn processing; a 1000-round limit prevents endless battles.

`[NEW]` and `[CHANGED]` comments mark additions and modifications to the assignment code.
