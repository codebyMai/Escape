"""
Libraries and imports
"""
from random import randint
from math import sqrt
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from colorama import Fore, init, Back, Style
import os
import sys
import time
import pyfiglet
import gspread
init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("hall_of_fame")

leaders = SHEET.worksheet('leaderboard')


def clear():
    """
    Cleans terminal
    """
    os.system("cls" if os.name == "nt" else "clear")


def typingPrint(text):
    """
    Typing effect for text
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)


def quit():
    welcome_screen()
    difficulty()
    intro()


def welcome_screen():
    """
    Prints title of the game and asks user to choose difficulty level
    """
    title = pyfiglet.figlet_format('Escape', font='doom')
    typingPrint(title)

    print(Back.RED + 'Warning!')
    print(Back.RED + 'You are going to face your deepest fears...')
    print(Fore.YELLOW + Style.BRIGHT + 'How brave are you?')
    print('1. Very brave! I am only scared of x-large, hairy spiders.')
    print('2. Reasonably brave. Occasionaly troubled by bad dreams.')
    print('3. I am already scared...')


def difficulty():
    """
    Sets board size and adds obstacle depending on the chosen level
    """
    global game_width
    global game_height
    global player_x
    player_x = 0
    global player_y
    player_y = 0
    global level
    global spider_x
    global spider_y
    global fear_x
    global fear_y
    while True:
        try:
            level = int(input('Enter 1,2 or 3.\n'))
            if level == 1:
                game_width = 20
                game_height = 20
                spider_x = randint(0, game_width)
                spider_y = randint(0, game_height)
                break
            elif level == 2:
                game_width = 15
                game_height = 15
                fear_x = randint(0, game_width)
                fear_y = randint(0, game_height)
                break
            elif level == 3:
                game_width = 10
                game_height = 10
                break
            else:
                clear()
                raise ValueError()
        except ValueError:
            print(Back.RED + 'To survive you need to follow instructions!')
    clear()


def before():
    """
    Measures distance to the key before move to enable hints
    """
    global key_x
    key_x = randint(0, game_width)
    global key_y
    key_y = randint(0, game_height)
    global before_move
    before_move = sqrt((key_x - player_x) ** 2 + (key_y - player_y) ** 2)


def intro():
    """
    Prints introduction and asks user for their name.
    """
    global name
    typingPrint('It is cold, pitch black and very, very quiet.\n')
    time.sleep(1)
    typingPrint('With horror you realise you have no idea where you are...\n')
    time.sleep(1)
    typingPrint('Or how you got here...\n')
    time.sleep(1)
    typingPrint('Suddenly you hear a hushed voice in the dark.\n')
    time.sleep(1)
    print(Fore.YELLOW + Style.BRIGHT + 'Who are you? What is your name?')
    name = input('Enter your name.\n')
    if not name.isalpha():
        print(Back.RED + 'Only letters are allowed!')
        name = input('Enter your name.\n')
    print(Fore.YELLOW + f'{name.capitalize()} only you can save us!\n')
    time.sleep(1)
    print(Fore.YELLOW + 'There is a key somewhere on the ground.\n')
    time.sleep(1)
    print(Fore.YELLOW + 'You must find it to get out!')
    time.sleep(2)
    clear()
    moves()
    return name


def moves():
    """
    Player movements, steps addition and obstacle encounters"
    """
    global player_x
    player_x = 0
    global player_y
    player_y = 0
    global steps
    steps = 0
    key_found = False
    before()
    print('You are in a square, pitch black room.')
    print('To get out you need to find the key.')
    print(Fore.YELLOW + Style.BRIGHT + 'Use W/S/D/A keys to move.')
    print(Fore.YELLOW + Style.BRIGHT + 'W- up, S- down, D- right, A- left.')
    print('Follow the helpful hints.')
    print('If you chicken out press Q to quit.\n')
    while not key_found:
        steps += 1
        move = input('\nQuick! Where do you want to go?\n')
        match move.lower():
            case 'w':
                player_y += 1
                if player_y > game_height:
                    print(Back.RED + '\nOops! You crashed into the wall!')
                    player_y = game_height
                    continue
            case 's':
                player_y -= 1
                if player_y < 0:
                    print(Back.RED + '\nYou cannot walk through walls!')
                    player_y = 0

            case 'a':
                player_x -= 1
                if player_x < 0:
                    print(Back.RED + '\nOops! You crashed into the wall!')
                    player_x = 0

            case 'd':
                player_x += 1
                if player_x > game_width:
                    print(Back.RED + '\nYou cannot walk through walls!')
                    player_x = game_width

            case 'q':
                print('Suddenly you realise it was all just a bad dream!')
                quit()

            case _:
                print(Back.RED + 'You can only move using W/S/A/D keys!')
                continue
        after()

        if level == 1 and player_x == spider_x and player_y == spider_y:
            print(Back.RED + 'Ew!\U0001F578 You walked into a spider web!')
            print(Back.RED + 'You recoil in horror to back where you started!')
            player_x = 0
            player_y = 0
        if level == 2 and player_x == fear_x and player_y == fear_y:
            print(Back.RED + 'Suddenly you feel a wave of panic!')
            print(Back.RED + 'You stagger back to where you started!')
            player_x = 0
            player_y = 0


def after():
    """
    Distance from the key and hints
    """
    global before_move
    after_move = sqrt((key_x - player_x) ** 2 + (key_y - player_y) ** 2)
    if before_move > after_move:
        print(Fore.GREEN + Style.BRIGHT + 'You are getting closer!')
    else:
        print(Fore.RED + Style.BRIGHT + 'You are moving away from the key!')
    before_move = after_move
    end_game()


def end_game():
    """
    Displays message when key found and update the step count
    """
    free = pyfiglet.figlet_format('Free!', font='doom')
    if player_x == key_x and player_y == key_y:
        print('\n')
        print(Fore.YELLOW + Style.BRIGHT + 'You found the key! You are')
        print(free)
        print(Fore.RED + Style.BRIGHT + f'You took {steps} steps to get out.')
        update_score()
        end_game_choice()


def end_game_choice():
    """
    Displays choice of options
    """
    print(Fore.YELLOW + 'To play againg - type 1.')
    print(Fore.YELLOW + 'To check "Hall of Fame" scores - type 2.')
    print(Fore.YELLOW + 'To quit - type 3.')
    options()


def update_score():
    """
    Updates data on google sheets
    """
    user = name.capitalize()
    update = [user, steps]
    leaders.insert_row(update, 2)


def results():
    """
    Displays scores on user request
    """
    clear()
    leaders.sort((2, 'asc'))
    data = leaders.get("A2:B11")
    print(Back.YELLOW + 'Top 10 scores\n')
    print(tabulate(data, headers=['name', 'score']))
    while True:
        back = int(input('\nPress 1 to get back to menu.\n'))
        try:
            if back == 1:
                clear()
                end_game_choice()
                break
            else:
                clear()
                raise ValueError()
        except ValueError:
            print(Back.RED + f'You must press 1 to go back.')


def options():
    """
    Options offered to user at the end of game
    """
    while True:
        try:
            choice = int(input('\n'))
            if choice == 1:
                clear()
                welcome_screen()
                difficulty()
                intro()
            elif choice == 2:
                results()
                break
            elif choice == 3:
                quit()
            else:
                clear()
                raise ValueError()
        except ValueError:
            print(Back.RED + 'Try again. Press 1, 2 or 3.')


if __name__ == '__main__':
    welcome_screen()
    difficulty()
    intro()
