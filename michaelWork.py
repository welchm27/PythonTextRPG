#!/usr/bin/env python3
""" Text-based RPG game
    Made by the WonderTwins
    Michael and Eric"""

from random import randint
from monsters import *
from mw_rooms import *
from item_list import *
import sys
import os

def roll_damage(damage_dice):
    num_dice, dice_sides = map(int, damage_dice.split('d'))
    total = sum(randint(1, dice_sides) for _ in range(num_dice))
    print("Rolled a " + str(total) + " damage.")
    return total

def roll_for_monster(monster_name):
    if monster_name in monsters:
        monster_info = monsters[monster_name]
        damage_dice = monster_info["damage"]
        roll_damage(damage_dice)
    else:
        print("Monster not found")

# roll_for_monster("Zombie")

# show instructions to player
def showInstructions():
    """Show instructions when called"""
    print('''
        RPG Game
        ========
        Commands:
          look ...
          go [direction]  
          get [item]
          inspect [item]
          search
        ''')
def showStatus():
    """Determine the current status of the player"""
    # print players current location
    print('-----------------------')
    print('You are in the ' + currentRoom)
    # print what the player is carrying
    print('Inventory:', inventory)
    # check if there's an item in teh room, if so print it
    if "item" in mw_rooms[currentRoom]:
        print('You see a ' + mw_rooms[currentRoom]['item'])
    print('-----------------------')

# an inventory, which is initially empty
inventory = []

# The rooms are from mw_rooms.py
currentRoom = 'Entrance'    # player starts in 'Entrance'
os.system('clear')      # start the player with a fresh screen
showInstructions()      # show instructions to the player

# breaking this while loop will result in game over
while True:
    showStatus()

    # the player Must type something
    # otherwise input will keep asking
    move = ''
    while move == '':
        move = input('>')

    # normalizing input:
    # .lower() makes it lower case, .split() turns it to a list
    # therefore, "get golden key" becomes ["get", "golden key"]
    move = move.lower().split(" ", 1)
    os.system('clear')  # clear the screen

    # if they type 'go' first
    if move[0] == 'go':
        # check that they are allowed wherever they want to go
        if move[1] in mw_rooms[currentRoom]:
            # check if they're trying to enter the 'Locked_RM'
            if currentRoom == 'Entrance' and move[1] == 'east' and 'key' not in inventory:
                print('The door is locked. You cannot enter without the key!')
            else:
                # set the current room to the new room
                currentRoom = mw_rooms[currentRoom][move[1]]
        # if they aren't allowed to go that way:
        else:
            print('You can\'t go that way!')

    # if they type 'get' first
    if move[0] == 'get':
        # make two checks:
        # 1. if the current room contains an item
        # 2. if the item in the room matches the item the player wishes to get
        if "item" in mw_rooms[currentRoom] and move[1] in mw_rooms[currentRoom]['item']:
            # add the item to their inventory
            inventory.append(move[1])
            # display a helpful message
            print(move[1] + ' got!')
            # delete the item key:value pair from the rooms dict
            del mw_rooms[currentRoom]['item']
        # if there's no item in the room or it doesn't match
        else:
            # tell them they can't get it
            print('Can\'t get ' + move[1] + '!')
    
    # if they type 'search' first
    if move[0] == 'search':
        # retrieve teh current room dict
        room_dict = mw_rooms[currentRoom]
        # check if 'search' key exists in the room dict
        if 'search' in room_dict:
            print(room_dict['search'])  # print the value of 'search'
            if 'item' in room_dict:     # if the item is in the room dict
                item_name = room_dict['item']   # set the item name to the room dict's item
                if item_name in items:      # if the room's item is in the item dict
                    item_info = items[item_name]    # set item_info to search item dict and return the item matched
                    description = item_info['description']  # set description to the item dict description of item
                    property = item_info['property']    # set property to item dict property of item
                    print('Item:', item_name)   # print the item name
                    print('Description:', description)  # print the item description
                    print('Property:', property)    # print the item's property
        else:
            print('Nothing of interest to search in this room.')