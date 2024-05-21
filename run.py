"""
Libraries and imports
"""
from random import randint
from math import sqrt
from google.oauth2.service_account import Credentials
from tabulate import tabulate
import os, sys, time
import pyfiglet
import gspread

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
    os.system('cls')

def typingPrint(text):
    """
    Typing effect for text
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)

def welcome_screen():
    """
    Prints title of the game and asks user to choose difficulty level
    """
    title = pyfiglet.figlet_format('Escape',font= 'doom')
    typingPrint(title)    

    print('Warning! This game is going to make you face your deepest fears...\n')
    print('How brave are you?')
    print('1. Very brave! I am only scared of x-large, hairy spiders.')
    print('2. Reasonably brave. I am only occasionaly riddled with self doubt and fear of public humilation.')
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
    while True:
        try:
            level = int(input('Enter 1,2 or 3 depending how brave are you feeling.\n'))
            if level == 1:
                game_width  = 20
                game_height  = 20
                global spider_x
                global spider_y
                spider_x = randint(0, game_width)
                spider_y = randint(0, game_height)
                break
            elif level == 2:
                game_width  = 15
                game_height  = 15
                global doubt_x
                global doubt_y
                doubt_x = randint(0, game_width)
                doubt_y = randint(0, game_height)
                break
            elif level == 3:
                game_width  = 10
                game_height  = 10
                break
            else:
                clear()
                raise ValueError()
        except ValueError as e_rr:
            print('You do not stand a chance in this game if you cannot follow simple instructions.')
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
    typingPrint('With horror you realise you have no idea where you are or how you got here...\n')
    time.sleep(1)       
    typingPrint('Suddenly you hear a hushed voice in the dark.\n')
    time.sleep(1)
    print('Who are you? What is your name?\n')
    name = input('Enter your name.\n')
    if not name.isalpha():
        print("Only letters are allowed!")
        name = input('Enter your name.\n')
    print(f'{name.capitalize()} you are our only chance to get out of here alive!\n')
    time.sleep(1)
    print('There is a key somewhere on the ground.\n')
    time.sleep(1)
    print('You must find it to get out!')
    time.sleep(1)
    
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
    key_found  = False 
    before()
    while not key_found:
       
        steps += 1
        move = input('Quick! Where do you want to go?\n')
        match move.lower():
            case 'w':
                player_y += 1
                if player_y > game_height:
                    print('Oops! You have just crashed into the wall!')
                    player_y = game_height
                    continue
            case 's':
                player_y -= 1
                if player_y < 0:
                    print(f'@\u21af\u2737! That hurt! You cannot walk through walls.')
                    player_y = 0

            case 'a':
                player_x -= 1
                if player_x < 0:
                    print('If you are not careful, you are going to end up concussed as well as kidnapped!')
                    player_x = 0

            case 'd':
                player_x += 1
                if player_x > game_width:
                    print('You hit the wall!')
                    player_x = game_width

            case 'q':
                print ('Having just remembered that you are terribly scared of the dark, you wake up and realise it was all just a bad dream!')
                quit()

            case _:
                print ('You can only move using W/S/A/D keys!')
                continue  
        after()

        if level == 1 and player_x == spider_x and player_y == spider_y:
            print('Ew!\U0001F578 You walked into a spider web!')
            print('You recoil in horror and end up back where you started!')
            player_x = 0
            player_y = 0
       
        if level == 2 and player_x == doubt_x and player_y == doubt_y:
            print('Suddenly you feel riddled with self doubt!')
            print('You stagger back to where you started!')
            player_x = 0
            player_y = 0
        
def after():
    """
    Distance from the key and hints
    """
    global before_move
    after_move = sqrt((key_x - player_x) ** 2 + (key_y - player_y) ** 2)
    if before_move > after_move:
       print('You are getting closer!')
    else:
       print('You are moving away from the key!')

    before_move = after_move 
    end_game()

def end_game():
    """
    Displays message when key found and update the step count 
    """
    free = pyfiglet.figlet_format('Free!',font= 'doom')
    if player_x == key_x and player_y == key_y:
        print('You found the \U0001F511 ! You are')
        print(free)
        print(f'It took you {steps} steps to get out.')
        update_score()
        end_game_choice()

def end_game_choice():
    """
    Displays choice of options
    """            
    print('To play againg - type 1.')
    print('To check "Hall of Fame" scores - type 2.')
    print('To quit - type 3.')
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
    print("Top 10 scores\n")
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
        except ValueError as e_rr:
            print(f'You must press 1 to go back.')
    
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
        except ValueError as e_rr:
            print('Try again. Press 1, 2 or 3.')

if __name__ == '__main__':
    welcome_screen()
    difficulty()
    intro()
     
       