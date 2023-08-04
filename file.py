import json
from rich import print
from lib import gttef #Unused. #TODO
import time

player_stats = {}
player_names = {}
next_player_id = 1
free_ids = []
global health_default
health_default = 100

def add_player():
    player_name = input("Enter player name: ")
    if player_name in player_names.values():
        print("[red bold]Player already exists.[/red bold]")
        return
    if detect_ID(player_name):
        print("[red bold]Player name must not be an ID.[/red bold]")
        return

    global next_player_id
    if free_ids:
        player_id = free_ids.pop(0)
    else:
        player_id = f"ID{next_player_id}"
        next_player_id += 1

    try:
        atk = int(input("Enter ATK stat: "))
        if atk > 10**30:
            print("[red bold]Error: ATK must be less than 10^30.[/red bold]")
            return
        defense = int(input("Enter DEF stat: "))
        if defense > 10**30:
            print("[red bold]Error: DEF must be less than 10^30.[/red bold]")
            return
        agility = int(input("Enter AGI stat: "))
        if agility > 10**30:
            print("[red bold]Error: AGI must be less than 10^30.[/red bold]")
            return
        magic = int(input("Enter MAG stat: "))
        if magic > 10**30:
            print("[red bold]Error: MAG must be less than 10^30.[/red bold]")
            return
        intelligence = int(input("Enter INT stat: "))
        if intelligence > 10**30:
            print("[red bold]Error: INT must be less than 10^30.[/red bold]")
            return
        resilience = int(input("Enter RUL stat: "))
        if resilience > 10**30:
            print("[red bold]Error: RUL must be less than 10^30.[/red bold]")
            return
        vitality = int(input("Enter VIT stat: "))
        if vitality > 10**30:
            print("[red bold]Error: VIT must be less than 10^30.[/red bold]")
            return
        stamina = int(input("Enter STA stat: "))
        if stamina > 10**30:
            print("[red bold]Error: STA must be less than 10^30.[/red bold]")
            return
        print("1 = Normal, 2 = [cyan]Veteran[/cyan], 3 = [green]Helper[/green], 4 = [blue]Moderator[/blue], 5 = [blue underline]Administrator[/blue underline], 6 = [yellow underline]Owner[/yellow underline]")
        authority = int(input("Enter Authority: "))
        if not 1 <= authority <= 6:
            print("[red bold]Error: Authority must be in between 1 (inclusive) and 6 (also inclusive).")
            return
    except ValueError:
        print("[bold red]Please enter integer values for stats and Authority, do not send empty values.[/bold red]")
        return

    l = calculate_derived_values(atk, defense, agility, magic, intelligence, stamina, vitality)
    damage_dealt_on_physical_hit = l[0]
    damage_dealt_on_magic_hit = l[1]
    damage_taken_on_hit = l[2]
    speed = l[3]
    regeneration_speed = l[4]
    max_health = l[5]
    dmgtakendivisor = l[6]

    player_stats[player_id] = {
        "name": player_name,
        "ATK": atk,
        "DEF": defense,
        "AGI": agility,
        "MAG": magic,
        "INT": intelligence,
        "RUL": resilience,
        "VIT": vitality,
        "STA": stamina,
        "Damage dealt on physical hit": damage_dealt_on_physical_hit,
        "Damage dealt on magic hit": damage_dealt_on_magic_hit,
        "Damage taken from a hit": damage_taken_on_hit,
        "Regeneration speed": regeneration_speed,
        "Max Health": max_health,
        "Speed": speed,
        "Authority": authority,
        "dev_lazy_dmgtakendivisor": dmgtakendivisor
    }
    player_names[player_id] = player_name

    print("Player added successfully. Player ID:", player_id)
    
def edit_player():
    identifier = input("Enter player ID or name: ")
    if identifier in player_stats:
        player_id = identifier
        player_name = player_names[player_id]
    elif identifier in player_names.values():
        player_name = identifier
        player_id = next(key for key, value in player_names.items() if value == player_name)
    else:
        print("[bold red]Invalid[/bold red] player ID or name.")
        return
    
    print("Applicable stats: ATK, VIT, DEF, MAG, INT, RUL, STA, AGI, Name, Authority")
    stat = input("Enter the stat to change(Case sensitive, ALL CAPS!): ")
    
    list_of_stats = ['ATK', 'VIT', 'DEF', 'MAG', 'INT', 'RUL', 'STA', 'AGI', 'Name', 'Authority']
    
    if stat in list_of_stats and stat != 'Name':
        try:
            value = int(input("Enter the new value: "))
        except:
            print("[bold red]Invalid[/bold red] value, please enter an integer.")
            return
        if stat in ['ATK', 'DEF', 'MAG', 'VIT', 'INT', 'RUL', 'STA', 'AGI', 'Authority']:
            if stat == 'Authority' and (value < 1 or value > 6):
                print("[bold red]Invalid[/bold red] Authority value, please enter a number 1-6 (inclusive).")
                return
            player = player_stats[player_id]
            player[stat] = int(value)
    elif stat == 'Name':
        new_name = input("Enter the new name of the player: ")
        player_names[player_id[stat]] = new_name
    else:
        print("[bold red]Invalid[/bold red] Stat.")
        return
def remove_player():
    identifier = input("Enter player ID or name to remove: ")
    if identifier in player_stats:
        player_id = identifier
    elif identifier in player_names.values():
        player_id = next(key for key, value in player_names.items() if value == identifier)
    else:
        print("[bold red]Invalid[/bold red] player ID or name.")
        return

    player_name = player_names[player_id]
    del player_stats[player_id]
    del player_names[player_id]
    free_ids.append(player_id)
    print(f"Player {player_name} ({player_id}) removed successfully.")

def calculate_derived_values(ATK, DEF, AGI, MAG, INT, STA, VIT):
    DMG = ATK * (AGI + STA) + (INT ** 2)
    MAGDMG = ATK * (MAG + AGI + (STA / 2)) + (INT ** 2)
    DMGTAKEN_1 = DEF * AGI
    DMGTAKEN_FULL = "damage taken / " + str(DMGTAKEN_1)
    SPEED = str(AGI * INT) + " km/h"
    REGEN_SPEED = f"{round(VIT * (INT/(3*(ATK/5))))} HP/s"
    MAX_HEALTH = f"{health_default + VIT * INT}"
    return [DMG, MAGDMG, DMGTAKEN_FULL, SPEED, REGEN_SPEED, MAX_HEALTH, DMGTAKEN_1]

def detect_ID(string):
    if string[0] == 'I' and string[1] == 'D':
        return True
    return False

def get_IDofPlayer(name):
    for player_id, player_name in player_names.items():
        if player_name == name:
            return player_id
    print("[bold red]Invalid[/bold red] Name.")

def calculate_damage_taken():
    name = input("Name or ID of player:")
    if detect_ID(name):
        if name not in player_names.keys():
            print("[bold red]Invalid[/bold red] ID.")
        else:
            damage = input("Enter Damage:")
            try:
                damage = float(damage)
            except:
                print("[bold red]Error: Damage is either too large, not a number or a string.[/bold red]")
            player_info = player_stats[name]
            print(f"Player {player_info['name']} will take {damage/player_info['dev_lazy_dmgtakendivisor']} on hit from an attack dealing {damage} damage.")
    else:
        ID = get_IDofPlayer(name)
        if ID:
            try:
                damage = float(input("Enter Damage:"))
            except:
                print("[bold red]Error: The value you have entered is invalid.[/bold red]")
            player_info = player_stats[ID]
            print(f"Player {player_info['name']} will take {damage/player_info['dev_lazy_dmgtakendivisor']} on hit from an attack dealing {damage} damage.")

def save_data():
    data = {
        "player_stats": player_stats,
        "player_names": player_names,
        "next_player_id": next_player_id,
        "free_ids": free_ids
    }
    with open("data.json", "w") as file:
        json.dump(data, file)
    print("Data saved successfully.")

def load_data():
    global player_stats, player_names, next_player_id, free_ids
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        player_stats = data["player_stats"]
        player_names = data["player_names"]
        next_player_id = data["next_player_id"]
        free_ids = data.get("free_ids", [])
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("No data file found.")

def print_player_stats():
    identifier = input("Enter player ID or name: ")
    if identifier in player_stats:
        player_id = identifier
        player_name = player_names[player_id]
    elif identifier in player_names.values():
        player_name = identifier
        player_id = next(key for key, value in player_names.items() if value == player_name)
    else:
        print("[bold red]Invalid[/bold red] player ID or name.")
        return

    player_info = player_stats[player_id]
    authority = player_info['Authority']
    rank = {
        1: "None",
        2: "[cyan]Veteran[/cyan]",
        3: "[green]Helper[/green]",
        4: "[blue]Moderator[/blue]",
        5: "[blue underline]Administrator[/blue underline]",
        6: "[yellow underline]Owner[/yellow underline]",
    }.get(authority, "Unknown Rank")

    print(f"Stats for player: [blue bold]{player_name}[/blue bold] ([blue bold]{player_id}[/blue bold])")
    print(f"Rank: {rank}")
    print(f"ATK: {player_info['ATK']}")
    print(f"DEF: {player_info['DEF']}")
    print(f"AGI: {player_info['AGI']}")
    print(f"MAG: {player_info['MAG']}")
    print(f"INT: {player_info['INT']}")
    print(f"RUL: {player_info['RUL']}")
    print(f"VIT: {player_info['VIT']}")
    print(f"STA: {player_info['STA']}")
    print(f"Damage dealt on physical hit: {player_info['Damage dealt on physical hit']}")
    print(f"Damage dealt on magic hit: {player_info['Damage dealt on magic hit']}")
    print(f"Damage taken from a hit: {player_info['Damage taken from a hit']}")
    print(f"Regeneration speed: {player_info['Regeneration speed']}")
    print(f"Max Health: {player_info['Max Health']}")
    print(f"Speed: {player_info['Speed']}")
    print(f"Authority: {authority}")

def get_all_players():
    names = list(player_names.values())
    ids = list(player_names.keys())
    return names, ids

def return_all_players():
    names, ids = get_all_players()

    if not names:
        print("No players found.")
    else:
        for name, player_id in zip(names, ids):
            print(f"Name: [bold green]{name}[/bold green], ID: [bold green]{player_id}[/bold green]")

def list_ids():
    print("[bold red]Dev command:[/bold red] [bold yellow]dev.getids[/bold yellow]")
    ids = list(player_stats.keys())
    if ids:
        print("List of all IDs:")
        for player_id in ids:
            print(player_id)
    else:
        print("No players found.")

def list_names():
    print("[bold red]Dev command:[/bold red] [bold yellow]dev.getnames[/bold yellow]")
    names = list(player_names.values())
    if names:
        print("List of all names:")
        for name in names:
            print(name)
    else:
        print("No players found.")

def raw_stats():
    print("[bold red]Dev command:[/bold red] [bold yellow]dev.rawstats[/bold yellow]")
    identifier = input("Enter player ID or name: ")
    if identifier in player_stats:
        player_id = identifier
        player_name = player_names[player_id]
    elif identifier in player_names.values():
        player_name = identifier
        player_id = next(key for key, value in player_names.items() if value == player_name)
    else:
        print("[bold red]Invalid[/bold red] player ID or name.")
        return

    print(f"Raw stats for player: {player_name} ({player_id})")
    print(player_stats[player_id])

def playerstats():
    print("[bold red]Dev command:[/bold red] [bold yellow]dev.fulldict[/bold yellow]")
    print("Player Names Dictionary:")
    print(player_names)

def stat_dict():
    print("[bold red]Dev command:[/bold red] [bold yellow]dev.statdict[/bold yellow]")
    print("[bold blue]Stat Dictionary:[/bold blue]")
    print(player_stats)

def todo():
    print("[bold red]Dev command:[/bold red] [bold yellow]dev.todo[/bold yellow]")
    print("[bold blue]Current list of TODO tasks:[/bold blue]")
    print("[bold green]1. Fix dev.timesession[/bold green]")
    print("[bold blue]2. Add new options such as events, battle variables etc and create categorical functions and set exit to 0")
    print("[bold blue]3. [bold red]WILL DO IN 5 YEARS OR MORE[/bold red] Create a real game using Pygame and intergrate this system into it[/bold blue]")


def main():
    while True:
        print("[bold green]Player Management System[/bold green]")
        print("1. Add Player")
        print("2. Remove Player")
        print("3. Calculate Damage Taken")
        print("4. Save Data")
        print("5. Load Data")
        print("6. Get All Players")
        print("7. Print Player Stats")
        print("8. Edit Player Stats")
        print("9. Exit") #TODO: Set exit to 0 and add 9 which will create an in-game event.

        choice = input("Enter your choice (1-9): ")
        print()

        if choice == "1":
            add_player()
        elif choice == "2":
            remove_player()
        elif choice == "3":
            calculate_damage_taken()
        elif choice == "4":
            save_data()
        elif choice == "5":
            try:
                load_data()
            except json.decoder.JSONDecodeError:
                print("[bold green]The JSON file seems to be empty, please add some data, then try loading again.[/bold green]")
        elif choice == "6":
            return_all_players()
        elif choice == "7":
            print_player_stats()
        elif choice == "8":
            edit_player()
        # elif choice == "dev.timesession":
        #     t1, t2 = ['n', 'N', 'No', 'nO', 'no', 'NO'], ['y', 'Y', 'ye', 'Ye', 'yE', 'YE', 'yes', 'Yes', 'yEs', 'yeS', 'YEs', 'yES', 'YES']
        #     confirmation = input("Are you sure you want to record session time? This will close the current session, make sure your data is saved:")
        #     if confirmation in t2:
        #         global time_taken_for_execution
        #         time_taken_for_execution = gttef(main, [], 1)
                
        #     elif confirmation in t1:
        #         pass
        #     else:
        #         print("[bold red]Invalid[/bold red] confirmation, please enter yes or no.")
        elif choice == "9":
            # print(time_taken_for_execution)
            print("Exiting program...")
            time.sleep(1)
            print("[bold green]Exited.[/bold green]")
            exit()
        elif choice == "dev.getids":
            list_ids()
        elif choice == "dev.getnames":
            list_names()
        elif choice == "dev.rawstats":
            raw_stats()
        elif choice == "dev.fulldict":
            playerstats()
        elif choice == "dev.todo":
            todo()
        elif choice == "dev":
            print("[bold blue]List of [red bold]Developer[/red bold] Commands:[/bold blue]")
            print("[bold green][bold yellow]dev.getids: [/bold yellow]Print a list of all IDs in the current database.[/bold green]")
            print("[bold green][bold yellow]dev.getnames: [/bold yellow]Print a list of all names in the current database.[/bold green]")
            print("[bold green][bold yellow]dev.rawstats: [/bold yellow]Print a list of all stats of a player, showing all stats, including hidden ones. Unrefined display.[/bold green]")
            print("[bold green][bold yellow]dev.fulldict: [/bold yellow]Print the entire name database stored in memory. Unrefined display.[/bold green]")
            print("[bold green][bold yellow]dev.statdict: [/bold yellow]Print the enter player stat data list. Unrefined display.[/bold green]")
            print("[bold green][bold yellow]dev.todo: [/bold yellow]Print the list of all TODO tasks.[/bold green]")
            print("[bold green][bold yellow]dev.timesession: [/bold yellow]Close the current session and open a new session which will be timed, requires confirmation before executing. [bold red]Not bugproofed, is currently completely broken and has been commented out. If you un-comment it, it WILL cause an error when run. Will develop it further down the line.[/bold red][/bold green]")

        else:
            print("[bold red]Invalid[/bold red] choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()