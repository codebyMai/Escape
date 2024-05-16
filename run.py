"""
Libraries and imports
"""
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
    Sets size of the board depending on the user choice of difficulty.
    """
    level = int(input('Enter 1,2 or 3 depending how brave are you feeling.'))
    if level := 1:
        Board.width  = 20
        Board.height  = 20 

    elif level := 2:
        Board.width  = 15
        Board.height  = 15

    elif level := 3:
        Board.width  = 10
        Board.height  = 10

    else :
        print('You do not stand a chance in this game if you cannot follow simple instructions.')          
        level = int(input('Enter 1, 2 or 3:\n'))             

def intro():
    """
    Prints introduction and asks user for their name.
    """
    typingPrint('It is cold, pitch black and very, very quiet.\n ')
    time.sleep(1)
    typingPrint('With horror you realise you have no idea where you are or how you got here...\n')
    time.sleep(3)       
    typingPrint('Suddenly you hear a hushed voice in the dark.\n')
    time.sleep(1)
    print('Who are you? What is your name?\n')
    name = input('Enter your name.')
    if not name.isalpha():
        print("Only letters are allowed!")
    print(f'{name.capitalize()} you are our only chance to get out of here alive!\n')
    time.sleep(2)
    print('There is a key somewhere on the ground.\n')
    time.sleep(2)
    print('You must find it to get out!')
    time.sleep(2)
    clear() 