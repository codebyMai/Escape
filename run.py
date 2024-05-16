"""
Libraries and imports
"""
import os, sys, time
import pyfiglet

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
