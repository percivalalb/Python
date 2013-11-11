'''
Created on 9 Nov 2013
@author: Alex
'''

import random

print "Welcome to the Guessing Game!"


number = random.randrange(100)
print "I have chosen a number between 1-100, Guess!!!"

lastGuess = -1

while lastGuess != number:
    lastGuessStr = raw_input("  Please input a number: ")
    try:
        lastGuess = int(lastGuessStr)
    except ValueError:
        print "Hummm, please enter a integer not a string"
        continue
    
    if lastGuess == number:
        print "Well done you guessed my number correctly!"
    elif lastGuess < number:
        print "Number to small try again"
    elif lastGuess > number:
        print "Number to big try again"
    