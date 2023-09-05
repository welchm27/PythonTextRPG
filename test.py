#!/usr/bin/env python3
import os
import time
from character_classes import character_classes  # import the dict of character classes
from character_classes import skills  # import the dict of skills
from main_level_map import main_floor  # import the dict for the main_floor
from item_list import items  # import items dict
from command_list import command_list  # import the command list
from combat import *
from monsters import monsters

def clear_screen():
    """Eric
    Clear the screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def characterCreation():
    """Eric
    Prompts the player to create their character by entering their name and choosing a class.
    Returns the character's name, class choice, and class attributes.
    """
    print("Let's begin by creating your character.")
    name = input("Enter your character's name: ")

    print("\nNow, choose your character class:")
    for class_key, class_data in character_classes.items():
        print(class_key + ". " + class_data["name"] + ": " + class_data["description"])

    class_choice = input("Enter the number corresponding to your desired class: ")

    # Retrieve the selected character class and its attributes
    selected_class = character_classes.get(class_choice)

    # Return the character's name, class choice, and class attributes
    return name, selected_class["name"], selected_class["description"], selected_class["health"], selected_class["armor"], selected_class["damage"]

def displayIntroduction():
    """Eric
    Displays the introduction and premise of the game to the player.
    """
    print(f"\nWelcome, {character_name} the {character_class}!")
    print("You have received a quest about an evil priest being controlled by an Illithid.")
    print("Your mission is to venture into the Unholy temple and put an end to their dark alliance.")
    print("Prepare yourself for a treacherous journey filled with danger and secrets!\n")

def displayCommandList():
    """Eric
    Display the available commands to the player."""
    print("\nAvailable commands:")
    for command in command_list:
        print("-", command)

def displayCharacterInfo():
    # --Eric--Display character information
    print("\n\nCharacter Name:", character_name)
    print("Character Class:", character_class)
    print("Class Description:", class_description)
    print("Health:", health)
    print("Armor:", armor)
    print("Damage:", damage)

def search_room(current_room):
    # Eric -- Function to search the current room for items
    items_in_room = main_floor[current_room]["items"]
    if items_in_room:
        print(f"You search the {main_floor[current_room]['name']} and find the following items:")
        for item in items_in_room:
            print(f"- {item}")
    else:
        print("You search the room but find no items.")

def get_item(current_room, item_name):
    # Eric -- Function to get an item from the room and add it to the player's inventory
    items_in_room = main_floor[current_room]["items"]
    if item_name in items_in_room:
        player_inventory["items"].append(item_name)
        items_in_room.remove(item_name)
        print(f"You pick up the {item_name} and add it to your inventory.")
    else:
        print("The item is not in this room.")

def inspect_item(item_name):
    # Eric -- Function to inspect an item in the player's inventory
    if item_name in player_inventory["items"]:
        item_description = items[item_name]["description"]
        print(f"You inspect the {item_name}: {item_description}")
    else:
        print("You don't have that item in your inventory.")

def use_item(item_name):
    # Eric -- Function to use a consumable item from the player's inventory
    if item_name in player_inventory["items"]:
        if items[item_name]["consumable"]:
            player_inventory["items"].remove(item_name)
            print(f"You use the {item_name}.")
        else:
            print("You can't use that item.")
    else:
        print("You don't have that item in your inventory.")

def displayInventory():
    # Eric -- Function to display the player's current inventory
    if player_inventory["items"]:
        print("Your Inventory:")
        for item in player_inventory["items"]:
            print("- " + item)
    else:
        print("Your inventory is empty.")

def check_for_monster(current_room, player_class, player_health):
    # --Michael: check if a monster is in the room:
    if "monster" in main_floor[current_room]:
        monster_name = main_floor[current_room]["monster"]
        combat(monster_name, player_class, player_health)
        del main_floor[current_room]["monster"]
        # else:
        #     print("Invalid character class.")
    else:
        print("No monster in this room")

# --Eric--Game start
# Initialize the character
character_name, character_class, class_description, health, armor, damage = characterCreation()
# Initialize the inventory
player_inventory = {
    "items": []
}


displayCharacterInfo()
displayIntroduction()

# --Eric--Initialize the current_location to "entrance" where the character starts
current_location = "entrance"

# Game loop --WonderTwins
first_time_in_entrance = True

while True:
    # Display the current location's name and description
    location = main_floor[current_location]
    print(f"\n{location['name']}")
    print(location['description'])

    # Set the flag to False after leaving the entrance for the first time
    if current_location != "entrance":
        first_time_in_entrance = False

    # Get available directions to move from the current location
    available_directions = [direction for direction in location if direction not in ["name", "description"]]

    # Ask the player for their next move
    print("enter 'help' to show command list.")
    next_move = input("Enter your command: ")
    if next_move.lower() == "help":
         # Display the available commands and inventory if the player asks for help
        displayCommandList()
        displayInventory()

    # Check if the player wants to exit the game
    if next_move.lower() == "exit":
        print("Thank you for playing! Goodbye.")
        break

    # Check if the player wants to look at available directions
    elif next_move.lower() == "look":
        print("Available directions:", ", ".join(available_directions))

    # Handle the inventory commands
    elif next_move.lower() == "search":
        search_room(current_location)
    elif next_move.lower().startswith("get "):
        item_name = next_move.split(" ", 1)[1]
        get_item(current_location, item_name)
    elif next_move.lower().startswith("inspect "):
        item_name = next_move.split(" ", 1)[1]
        inspect_item(item_name)
    elif next_move.lower().startswith("use "):
        item_name = next_move.split(" ", 1)[1]
        use_item(item_name)

    # Check if the player wants to move to another location
    elif next_move.startswith("go "):
        # Extract the direction from the command
        direction = next_move.split(" ", 1)[1]
        # Check if the chosen direction is valid
        if direction in available_directions:
            # Move the player to the next location
            current_location = location[direction]
            # Michael -- check for monster which if present, will begin combat()
            player_health = None
            for class_data in character_classes.values():
                if class_data["name"] == character_class:
                    player_health = [class_data["health"]]  # Wrap player_health in a list
                    break
            if player_health is None:
                print("Invalid character class")
            check_for_monster(current_location, character_class, player_health)
            # Clear the screen after moving to a new location
            if not first_time_in_entrance:
                time.sleep(1)  # Add a 1-second delay
                clear_screen()
        else:
            print("Invalid direction. Please choose a valid direction.")

    # Handle other invalid commands
    else:
        print("Invalid command. Please enter a valid command.")