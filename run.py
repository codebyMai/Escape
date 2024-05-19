"""
Libraries and imports
"""
from random import randint
from math import sqrt
import os, sys, time
import pyfiglet

class Board:
    def __init__(self, width, height): 
        self.width = width
        self.height = height

def clear():
    """
    Cleans terminal.
    """
    os.system('cls')

def typingPrint(text):
    """
    Typing effect for text.
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)

def welcome_screen():
    """
    Prints title of the game and asks user to choose difficulty level.
    """

    title = pyfiglet.figlet_format('Escape',font= 'doom')
    typingPrint(title)    

    print('Warning! This game is going to make you face your deepest fears...')
    print('How brave are you?')
    print('1. Very brave! I am only scared of x-large, hairy spiders.')
    print('2. Reasonably brave. I am only occasionaly riddled with self doubt and fear of public humilation.')
    print('3. I am already scared...') 
            
def difficulty():
    """
    This function will ask player to choose dificulty level for the game.

    """
    while True:
        try:
         
            level = int(input('Enter 1,2 or 3 depending how brave are you feeling.\n'))
            if level == 1:
                Board.width  = 20
                Board.height  = 20
                key_x = randint(0, Board.width)
                key_y = randint(0, Board.height)
                break
            elif level == 2:
                Board.width  = 15
                Board.height  = 15
                break
            elif level == 3:
                Board.width  = 10
                Board.height  = 10
                break
            else:
                clear()
                raise ValueError()
        except ValueError as e_rr:
            print('You do not stand a chance in this game if you cannot follow simple instructions.')
    clear()
    return Board.height, Board.width

        

def intro():
    """
    Prints introduction and asks user for their name.
    """
    typingPrint('It is cold, pitch black and very, very quiet.\n')
    time.sleep(1)
    typingPrint('With horror you realise you have no idea where you are or how you got here...\n')
    time.sleep(3)       
    typingPrint('Suddenly you hear a hushed voice in the dark.\n')
    time.sleep(1)
    print('Who are you? What is your name?\n')
    name = input('Enter your name.\n')
    if not name.isalpha():
        print("Only letters are allowed!")
        name = input('Enter your name.\n')
    print(f'{name.capitalize()} you are our only chance to get out of here alive!\n')
    time.sleep(2)
    print('There is a key somewhere on the ground.\n')
    time.sleep(2)
    print('You must find it to get out!')
    time.sleep(2)
    clear() 

"""def game():

    Sets game variables.
    
    player_x  = 0
    player_y  = 0
    steps = 0
    key_x = randint(0, Board.width)
    key_y = randint(0, Board.height)
    key_found  = False"""

def before():
    """
    Measuring distance to key before move for the hints
    """
    #before_move = sqrt((key_x - player_x) ** 2 + (key_y - player_y) ** 2)

def moves():
    
    """
    Player movements and steps addition"
    """
    player_x  = 0
    player_y  = 0
    steps = 0
    key_x = randint(0, Board.width)
    key_y = randint(0, Board.height)
    key_found  = False
    while not key_found:
        before()
        steps += 1
        move = input('Quick! Where do you want to go?')
        match move.lower():
            case 'w':
                player_y += 1
                if player_y > Board.height:
                    print('Oops! You have just crashed into the wall!')
                    player_y = Board.game_height

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
                if player_x > Board.width:
                    print('You hit the wall!')
                    player_x = Board.game_width

            case 'q':
                print ('Having just remembered that you are terribly scared of the dark, you wake up and realise it was all just a bad dream!')
                quit()

            case _:
                print ('You can only move using W/S/A/D keys!')
                continue   

if __name__ == '__main__':
    welcome_screen()
    difficulty()
    intro()    