"""
Libraries and imports
"""
from random import randint
from math import sqrt
import os, sys, time
import pyfiglet




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
    global game_width
    global game_height
    while True:
        try:
            level = int(input('Enter 1,2 or 3 depending how brave are you feeling.\n'))
            if level == 1:
                game_width  = 20
                game_height  = 20
                break
            elif level == 2:
                game_width  = 15
                game_height  = 15
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
    #return game_height, game_width
      

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
    moves() 

def before():
   
    """Measuring distance to key before move for the hints"""
    
   
    player_x  = 0
    
    player_y  = 0 
    global key_x
    key_x = randint(0, game_width)
    global key_y
    key_y = randint(0, game_height)
    global before_move
    before_move = sqrt((key_x - player_x) ** 2 + (key_y - player_y) ** 2)
    print(key_x, key_y)

  
def moves():
    """
    Player movements and steps addition"
    """
    
    global player_x
    player_x = 0
    global player_y
    player_y = 0
    
    key_found  = False 
    before()
    while not key_found:
        global steps
        steps = 0  
        
        steps += 1
        move = input('Quick! Where do you want to go?')
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
        print(player_x, player_y)
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
    """Key found and steps total """

    free = pyfiglet.figlet_format('Free!',font= 'doom')
    if player_x == key_x and player_y == key_y:
        print('You found the \U0001F511 ! You are')
        print(free)
        print(f'It took you {steps} steps to get out.')
        print('To play againg press 1')
        print('To check "Hall of Fame" scores press 2')
        print('To quit press 3')
        options() 

#def score():

def options():
    while True:
        try:
            choice = int(input('\n'))
            if choice == 1:
                clear()
                welcome_screen()
                difficulty()
                intro()
            elif choice == 2:
                score()
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
     
       