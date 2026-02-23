import time
import pyfiglet
import json
import os
import random
import sys
from hall_of_fame_security import load_record, save_record
from colorama import Fore, Style, init


# Package initilisation
# colorama
init(autoreset=True)

# Font for game messages
def system(text):
    print(Fore.GREEN + text + Style.RESET_ALL)
def error(text):
    print(Fore.RED + text + Style.RESET_ALL)

# intro - 1 function
def intro():
    # Display title with color animation
    title = pyfiglet.figlet_format("Just a Rock-Paper-Scissors Game", font="small")
    lines = title.split("\n")
    # colors for the animation
    colors = [
        Fore.RED,
        Fore.YELLOW,
        Fore.GREEN,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.BLUE,
        Fore.MAGENTA,
    ]
    # Display title with color animation
    print(Fore.YELLOW + "=" * 60)
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)
        time.sleep(0.05)

    # ask if the user wants to play
    system("\nPress Enter to continue, or type 'q' to chicken out: ")
    user_input = input()
    if user_input.lower() == 'q':
        system("Cow.. Bye!")
        sys.exit()

# hall of fame - 2 functions
# (1) - shows the hall of fame
def show_hall_of_fame():
    # load the current record
    record = load_record()
    # caption for hall of fame
    print(Fore.YELLOW + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "🏆 HALL OF FAME".center(60))
    print("")
    # show champion and record
    print(Fore.WHITE + f"CHAMPION: {Fore.GREEN + Style.BRIGHT}{record['name']}")
    print(Fore.WHITE + f"RECORD:   {Fore.MAGENTA + Style.BRIGHT}{record['streak']} Win Streak")
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)

# (2) update the hall of fame
def update_hall_of_fame(player_name, new_streak):
    # load the current record
    current_record = load_record()
    # if new streak
    if new_streak > current_record['streak']:
        new_record = {
            "name": player_name,
            "streak": new_streak,
        }
        # save new record
        save_record(new_record)
        # celebration
        print(Fore.YELLOW + "=" * 60)
        print(Fore.GREEN + Style.BRIGHT + "🎉 NEW RECORD! 🎉".center(60))
        print(Fore.CYAN + f"{player_name} is the new champion with {new_streak} win streak!".center(60))
        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
        print("")
        # if the update went well
        return True
    # if it doesn't -> record not broken
    return False

# player name - 1 function
def get_player_name():
    # while loop to ensure user provides a name
    while True:
        system("\nHunter, what is your name? (max 20 characters) : ")
        name = input().strip()
        # if name not provided
        if not name:
            error("\nEvery hunter has a name. Tell us your name : ")
        # if too long
        elif len(name) > 20:
            error("\nName too long (max 20 characters). Try again : ")
        # provided -> greet and return the name
        else:
            system(f"\nVery well, {name}. \nLet's go hunt\n")
            return name

# player's status - 1 function
def player_status(player_name, lives, streak):
    name = f"{Fore.MAGENTA + Style.BRIGHT}{player_name}"
    print(Fore.GREEN + Style.BRIGHT + f"[ Player Status ] {name}" + Fore.GREEN + f" – {lives} lives - {streak} win streak" + Style.RESET_ALL)

# decorates weapon
def weapons_decorated(weapon):
    colours = {
        "rock": Fore.BLUE + "🪨 Rock",
        "paper": Fore.WHITE + "📄 Paper",
        "scissors": Fore.RED +   "✂️  Scissors",
    }
    return colours.get(weapon, weapon) + Style.RESET_ALL

# functions tells the result
def judge(player_weapon, computer_weapon):
    # draw
    if player_weapon == computer_weapon:
        return "draw"
    # win condition
    win_conditions = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    }
    # win or loss
    if win_conditions[player_weapon] == computer_weapon:
        return "win"
    else:
        return "loss"

# player chooses a weapon
def get_player_weapon():
    # weapon option
    weapons = ["rock", "paper", "scissors"]
    # while loop to ensure user chooses a weapon
    while True:
        print("\nWeapon Code")
        for i in range(0,3,1):
            print(f"{i+1} : {weapons_decorated(weapons[i])}")
        system("\nChoose your weapon (Enter the weapon code number) : ")
        choice = input("")

        if choice in ["1","2","3"]:
            player_weapon = weapons[int(choice) - 1]
            system(f"\nYou chose {weapons_decorated(player_weapon)}")
            return player_weapon
        # if option not provided
        else:
            error("\nThat doesn't sound right. Try again")

# player weapon vs computer weapon
def challenge(player_weapon, player_name, lives, streak):
    # Computer chooses a weapon
    weapons = ["rock", "paper", "scissors"]
    computer_weapon = random.choice(weapons)
    # Countdown for some suspense
    time.sleep(1)
    system("\nHere we go.")
    time.sleep(1.5)
    for i in range(0,3,1):
        system(f"\n{weapons[i]}..")
        time.sleep(0.8)
    system(f"\nShoot!\n"+" "*20+f"⛹(YOU) {weapons_decorated(player_weapon)} VS {weapons_decorated(computer_weapon)} (SYSTEM)👽")

    result = judge(player_weapon, computer_weapon)

    if result == "draw":
        lives, streak, status = draw(player_name, lives, streak)
    elif result == "win":
        lives, streak, status = win(player_name, lives, streak)
    else:
        lives, streak, status = lost(player_name, lives, streak)

    return lives, streak, status

# check if the player's lives are more than 0
def life_check(lives):
    return lives > 0

# check if the current record is broken
def record_check(new_streak, player_name):
    # Load current record using security module
    current_record = load_record()
    # if new record and return True to signify it worked
    if new_streak > current_record["streak"]:
        update_hall_of_fame(player_name, new_streak)
        return True
    # return false otherwise
    return False

# ending
def ending():
    time.sleep(3)
    print("")
    error(f"This is as far as you go".center(60))
    time.sleep(3)
    error("No more,".center(60))
    time.sleep(3)
    error("This is it.".center(60))
    time.sleep(3)
    print("")
    system(f"by Taabe & Naru (Prey, 2022)".center(60))

# if the result is a draw
def draw(player_name, lives, streak):
    time.sleep(1)
    system(f"\nDraw.")
    time.sleep(1)
    system(f"Let's try again\n")
    time.sleep(1)
    return lives, streak, "continue"

# when won
def win(player_name, lives, streak):
    # winning message
    time.sleep(1)
    system(f"\nWon!\n")
    # streak update
    streak += 1
    # if streak % 3, update player_lives
    if streak % 2 ==0:
        lives +=1
        print(Fore.YELLOW + "=" * 60)
        print(Fore.GREEN + Style.BRIGHT + "🎉 2 Win Streak = 1 Life! 🎉".center(60))
        print(Fore.CYAN + f"You've earned one more life!".center(60))
        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    # check for new record
    record_check(streak, player_name)
    system(f"Let's keep going\n")
    time.sleep(1)
    return lives, streak, "continue"

# when lost
def lost(player_name, lives, streak):
    # loss message
    time.sleep(4)
    system(f"\nwell..")
    # update stats
    lives -= 1
    streak = 0
    # life check
    if life_check(lives):
        time.sleep(1)
        system(f"Let's try again\n")
        time.sleep(1)
        return lives, streak, "continue"
    else:
        ending()
        return lives, streak, "game over"


def main():
    intro()
    show_hall_of_fame()
    player_name = get_player_name()
    lives = 2
    streak = 0
    status = "continue"

    while status == "continue":
        player_status(player_name, lives, streak)
        player_weapon = get_player_weapon()
        lives, streak, status = challenge(player_weapon, player_name, lives, streak)


if __name__ == "__main__":
    main()
