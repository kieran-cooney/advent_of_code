"""
Object oriented to simulate the battle system,
and a functional approach to find the optimal solution.

To-do:
* Accept effect durations as class inputs, and avoid using copy
* Add more information to print statement
* Add a verbose option to player turn
* Implement decorator for spells
* Implement logic for effects
"""
import sys
from copy import copy
from collections import namedtuple

PLAYER_HP = 50
PLAYER_MP = 500

MAGIC_MISSILE_COST = 53
MAGIC_MISSILE_DMG = 4
DRAIN_COST = 73
DRAIN_DMG = 2
DRAIN_HEAL = 2
SHIELD_COST = 113
SHIELD_DURATION = 6
SHIELD_ARMOR = 7
POISON_COST = 173
POISON_DURATION = 6
POISON_DMG = 3
RECHARGE_COST = 229
RECHARGE_DURATION = 5
RECHARGE_MANA = 101

Spell = namedtuple('Spell', ['name', 'func', 'cost'])

def parse_input(filepath):
    # Parse the input of the boss parameters.
    out_dict = dict()
    with open(filepath, 'r') as f:
        for line in f:
            key, value = line.split(': ')
            out_dict[key] = int(value)
    return out_dict


class MagicBattle():
    """
    Class used to simulate battle between boss and magic player.
    
    Example usage:
    
    battle = MagicBattle(55, 8)
    print(battle)
    spells = battle.available_spells
    print(spells)
    battle.turn(spells[0])
    print(battle)
    battle.turn(spells[1])
    """
    def __init__(self, boss_hp, boss_dmg, player_hp=PLAYER_HP,
                 player_mp=PLAYER_MP, player_poison=0):
        self.boss_hp = boss_hp
        self.boss_dmg = boss_dmg
        self.player_hp = player_hp
        self.player_mp = player_mp
        self.player_poison = player_poison

        # Calculate boss dmg when player has armor once as it only
        # ever takes one value
        self.boss_dmg_after_armor = max(self.boss_dmg - SHIELD_ARMOR, 1)

        # Need this variable as well as player_mp due to mana recharge
        self.player_total_mana_spent = 0

        self.player_armor = 0

        # Duration of various magic effects
        self.player_armor_duration = 0
        self.boss_poison_duration = 0
        self.player_recharge_duration = 0

        self.player_wins = False
        self.boss_wins = False

    def get_winner(self):
        # Simple helper function to get a string for the winner
        if self.player_wins:
            return 'Player'
        elif self.boss_wins:
            return 'Boss'
        else:
            return 'No winner yet...'

    def __repr__(self):
        input_tuple = (self.boss_hp, self.boss_dmg, self.player_hp, self.player_mp)
        return "MagicBattle({}, {}, {}, {})".format(*input_tuple)

    def __str__(self):
        s = "Player HP = {}\n".format(self.player_hp)
        s += "Player MP = {}\n".format(self.player_mp)
        s += "Boss HP = {}\n".format(self.boss_hp)
        s += "Boss dmg= {}\n".format(self.boss_dmg)
        spell_names = [s.name for s in self.available_spells]
        s += "Available spells: {}\n".format(spell_names)
        s += "Winner: {}\n".format(self.get_winner())
        
        return s
        
    def magic_missile(self):
        self.boss_hp -= MAGIC_MISSILE_DMG

    def drain(self):
        self.boss_hp -= DRAIN_DMG
        self.player_hp += DRAIN_HEAL

    def shield(self):
        assert self.player_armor_duration == 0

        self.player_armor = SHIELD_ARMOR
        self.player_armor_duration = SHIELD_DURATION

    def poison(self):
        assert self.boss_poison_duration == 0

        self.boss_poison_duration = POISON_DURATION

    def recharge(self):
        assert self.player_recharge_duration == 0

        self.player_recharge_duration = RECHARGE_DURATION

    # List of all spells. Useul for looping over possible player options
    spells = [
        Spell('Shield', shield, SHIELD_COST),
        Spell('Recharge', recharge, RECHARGE_COST),
        Spell('Poison', poison, POISON_COST),
        Spell('Magic Missile', magic_missile, MAGIC_MISSILE_COST),
        Spell('Drain', drain, DRAIN_COST),
    ]

    # List of spells available to player. Will change depending on effects and
    # mana
    available_spells = spells.copy()

    def resolve_shield(self):
        # Resolve the effects of shield spell
        if self.player_armor_duration > 0:
            self.player_armor_duration -= 1
            if self.player_armor_duration == 0:
                self.player_armor = 0

    def resolve_poison(self):
        # Resolve the effects of poison spell
        if self.boss_poison_duration > 0:
            self.boss_hp -= POISON_DMG
            self.boss_poison_duration -= 1

    def resolve_recharge(self):
        # Resolve the effects of recharge spell
        if self.player_recharge_duration > 0:
            self.player_mp += RECHARGE_MANA
            self.player_recharge_duration -= 1

    def resolve_effects(self):
        # Resolve all effects at the start of the turn
        self.resolve_shield()
        self.resolve_poison()
        self.resolve_recharge()

    def is_spell_available(self, spell):
        # Returns a boolean indicating if a spell is available to use
        affordable = spell.cost <= self.player_mp
        name = spell.name
        if name == 'Shield':
            effect_dur = self.player_armor_duration
        elif name == 'Poison':
            effect_dur = self.boss_poison_duration
        elif name == 'Recharge':
            effect_dur = self.player_recharge_duration
        else:
            return affordable

        effect_available = (effect_dur in [0, 1])

        return affordable and effect_available

    def player_turn(self, spell):
        # Take player turn, performing the input spell
        assert spell in self.available_spells
        self.player_hp -= self.player_poison

        if self.player_hp <= 0:
            self.boss_wins = True

        self.resolve_effects()

        spell.func(self)
        self.player_mp -= spell.cost
        self.player_total_mana_spent += spell.cost
        
        self.available_spells = [
            s for s in self.spells
            if self.is_spell_available(s)
        ]

        if self.boss_hp <= 0:
            self.player_wins = True

    def boss_turn(self):
        # Take boss turn
        self.resolve_effects()

        if self.boss_hp <= 0:
            self.player_wins = True

        if self.player_armor_duration > 0:
            self.player_hp -= self.boss_dmg_after_armor
        else:
            self.player_hp -= self.boss_dmg

        if self.player_hp <= 0:
            self.boss_wins = True


    def turn(self, spell):
        # A turn is just a player_turn followed by a boss_turn
        self.player_turn(spell)
        self.boss_turn()


def find_cheapest_spells(battle):
    """
    Take a magic battle, and compute the lowest amount of mana required for
    the player to win.
    
    Also compute the spells used and the number of battles searched.

    Tree based recursive solution.
    """
    # Initialize variables
    lowest_mana = float('inf')
    winning_spells = list()
    num_battles = 0

    def find_cheapest_helper(battle, spell_history=list()):
        """
        Helper function. This is the actual recursive function. We use this
        so that we don't need to declare any global variables (like
        lowest_mana) when calling find_cheapest_spells
        """
        # Set these variables to be nonlocal so the variables defined in
        # find_cheapest_spells are used. Otherwise, python treats them as
        # completely different variables!
        nonlocal lowest_mana
        nonlocal winning_spells
        nonlocal num_battles

        if battle.player_wins:
            # If the player wins, just update the results
            lowest_mana = min(lowest_mana, battle.player_total_mana_spent)
            winning_spells = spell_history
            num_battles += 1
        elif (not battle.available_spells) or battle.boss_wins or (battle.player_total_mana_spent >= lowest_mana):
            # If the player loses due to one of three conditions, just
            # just increment the number of battles searched
            num_battles += 1
        else:
            # Otherwise, to battle! Find all the spells that can be cast...
            for spell in battle.available_spells:
                # Create a new battle... (deepcopy isn't needed, and is slower)
                new_battle = copy(battle)
                # Take the next turn...
                new_battle.turn(spell)
                # And now repeat the search for the battle after that turn
                find_cheapest_helper(new_battle, spell_history + [spell.name])

    # Calculate results, and return
    find_cheapest_helper(battle)

    return (lowest_mana, winning_spells, num_battles)


def main(filepath):
    boss_dict = parse_input(filepath)
    battle = MagicBattle(boss_dict['Hit Points'], boss_dict['Damage'])

    lowest_mana, winning_spells, num_battles = find_cheapest_spells(battle)
    print("The player can win using the least amount of mana ({}) with the spells {}".format(lowest_mana, winning_spells))
    print("{} battles were simulated to find this solution".format(num_battles))

    battle = MagicBattle(boss_dict['Hit Points'], boss_dict['Damage'], player_poison=1)

    lowest_mana, winning_spells, num_battles = find_cheapest_spells(battle)
    print("The player can win using the least amount of mana ({}) with the spells {}".format(lowest_mana, winning_spells))
    print("{} battles were simulated to find this solution".format(num_battles))

if __name__=='__main__':
    if len(sys.argv) > 1:
          filepath = sys.argv[1]
    else:
          filepath = "input.txt"
    main(filepath)
