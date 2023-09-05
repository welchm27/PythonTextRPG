#!/usr/bin/env python3
"""Michael
    function to handle combat and import into main file"""

from monsters import monsters
from character_classes import character_classes
from character_classes import skills
import random
import time

# combat function to be imported and used in main file
def combat(monster_name, player_health: int, armor, damage, skill): 
    monster = monsters[monster_name]        # setting local monster to name from monsters dict
    monster_health = monster["health"]      # setting monster health from monsters dict
    
    # show the user a monster appears in the room and ask for their action
    print("=====================")
    print(f"A {monster_name} appears! What do you want to do?")
    
    # loop for the entire encounter
    while True:
        # ask player to choose to fight or run. Only valid input accepted
        choice = input("1. Fight\n2. Run\nEnter your choice: ")
        # if 1(fight) is chosen
        if choice == "1":
            # start the fight function and return player health
            player_health = fight(monster_name, monster_health, player_health, armor, damage, skill)
            break  # if fight function concludes, break out of this while loop, ending the encounter
        # if 2(run) is chosen
        elif choice == "2":
            # begin the run() function
            run(monster_name, monster_health, player_health, armor, damage, skill)
            break # if run function concludes, break out of this while loop, ending the encounter
        # if an invalid input is used, continue asking
        else:
            print("Invalid choice. Please choose a valid option.")
    return player_health   # return player_health to be used and updated in textRPG.py

# simple roll function for use everywhere!!!!!!!!
def roll(dice):     # will input dice as "1d20", "2d4", "2d6", etc...
    # split the dice input using the "d".  The left entry is how many and the right is what number they go up to.
    num_dice, dice_sides = map(int, dice.split('d'))
    # roll and sum up the total amount of dice and each of their individual random rolls
    total = sum(random.randint(1, dice_sides) for _ in range(num_dice))
    return total    # return the total

# player turn fight function inside of combat
def fight(monster_name, monster_health, player_health, armor, damage, skill):
    # while both player and monster are still alive
    while monster_health > 0 and player_health > 0:
        time.sleep(1)           # after a 2 second delay
        # os.system('clear')      # clear the screen
        print("========================")
        print("Your health:", player_health)    # display player's current health
        print(f"{monster_name}'s health: {monster_health}") # display monster's current health
        print("------------------------")
        
        # ask the player if they want to attack or try to run(during combat)
        print("What do you want to do?")
        choice = input("\n1. Attack\n2. Run\n3. Use Skill\nEnter your choice: ")
        if choice == "1":
            monster = monsters[monster_name]
            # if attack, roll 1d20 to see if the player hits
            hit_roll = roll("1d20")
            # display your hit roll
            print("You rolled a: " + str(hit_roll) + " to hit!")
            # compare roll to monster's armor value
            if hit_roll > monster["armor"]: 
                print(f"\nYou hit the {monster_name}!")
                # deal damage based off player damage dice
                damage_roll = roll(damage)
                # display the damage that you dealt, and reduce the monster's health by that amount
                print("You deal", damage_roll, "damage.")
                monster_health -= damage_roll
                time.sleep(1)
            else:
                # if you miss, display it
                print(f"\nYou miss the {monster_name}!")
                time.sleep(1)
            if monster_health <= 0:
                # check if monster is dead and display message
                print(f"You defeated the {monster_name}!")
                time.sleep(1)
            else:
                # if monster is still alive, display it's health
                print(f"The {monster_name}'s health: {monster_health}")
                time.sleep(1)
        # if you choose run, execute run() function
        elif choice == "2":
            run(monster_name, monster_health, player_health, armor, damage, skill)
            break   # if you succeed, break out of loop
        elif choice == "3":
            skill_damage, skill_description = useSkill(skill)
            print(f"{skill_description} doing {skill_damage} points of damage damage!")
            monster_health -= skill_damage
            time.sleep(1)
        else:
            # check for invalid input
            print("Invalid choice. Please choose a valid option.")
        # after a 1 second delay, the monster takes his turn
        time.sleep(1)
        player_health = monsterAttack(monster_name, monster_health, player_health, armor, damage)
    return player_health

# function for if the player chooses run at anytime during combat
def run(monster_name, monster_health, player_health, armor, damage, skill):
    # roll 1d20 to see if you succeed
    run_roll = roll("1d20")
    # gives a 50% chance to run
    if run_roll > 10:
        print("You successfully run away.")
        time.sleep(1)
    else:
        # if you fail to succeed, the monster takes a turn and attacks you
        print("You failed to escape and got attacked!")
        time.sleep(1)
        monsterAttack(monster_name, monster_health, player_health, armor, damage)
        # after the monster attacks, begin the normal fight() function
        player_health = fight(monster_name, monster_health, player_health, armor, damage, skill)
    return player_health

# Use Skill function to check the damage value from the skills dict in character_classes file
def useSkill(skill):
    if skill in skills:
        return skills[skill]["damage"], skills[skill]["description"]
    else:
        return 0

# monster's turn attack function 
def monsterAttack(monster_name, monster_health, player_health, armor, damage):
    if monster_health > 0:
        # roll 1d20 for hit
        hit_roll = roll("1d20")
        # compares hit roll to player armor value
        # if greater, it's a hit
        if hit_roll > armor:
            monster = monsters[monster_name]
            print(f"\nYou got hit hit by the {monster_name}!")
            time.sleep(1)
            # damage roll calculated from monsters damage value in monsters dict
            damage_roll = roll(monster["damage"])
            print("You took", damage_roll, "damage.")
            time.sleep(1)
            # adjust player health by damage dealt
            player_health -= damage_roll
        else:
            # if the monster misses
            print(f"\nThe {monster_name} missed it's attack!")
            time.sleep(1)
        # check if the player is dead, and return message
        if player_health <= 0:
            print("You were defeated, GAME OVER!")
            time.sleep(2)
        else:
            # if the player is still alive, display player health
            print(f"Your health: {player_health}\n")      
            time.sleep(1)
        # return updated player health
    return player_health

# Currently hard coded to test function and ensure this file is working as intented
#------- this will instead pull monster_name from current_room["monster"] once imported in main file
# monster_name = "Skeleton"     
# #----- combat() will instead execute in the main file if there is a monster in the current room
# combat(monster_name, player_health)  