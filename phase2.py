import bsddb3

# Dunno if we'll need this but I had the idea and wanted to make it just incase
from time import sleep
from os import system
def boolInput(string, clear=True):
    while True:
        if clear:
            system('cls||clear')
        sel = input(string + '[y/n]\n\r').lower()
        if sel == y:
            return True
        elif sel == n:
            return False
        else:
            print("Invalid selection, try again.")
            sleep(0.75)

