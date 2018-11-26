from Database import Database
from os import system
import sys

def main():
    db = Database()
    system('cls||clear')
    print("Welcome to sqlite3 clone!\n\rFeel free to query the database of ads. Type !help for assistance at any time.\n")
    while True:
        query = input('>>> ').lower()
        if query == 'output=brief':
            db.setOutput(False)
            print("Changed output mode to brief.")
            continue
        elif query == 'output=full':
            db.setOutput(True)
            print("Changed output mode to full.")
            continue
        elif query == '!help':
            helpmess = '!help -- Prints this message.\n!quit -- Exits the terminal program.\n!clear -- Clears the terminal window of results\noutput=[full|brief] -- Sets the output to display all info, or just the Ad ID and Title.'
            print(helpmess)
            continue
        elif query == '!clear':
            system('cls||clear')
            print("Welcome to sqlite3 clone!\n\rFeel free to query the database of ads. Type !help for assistance at anytime.\n")
            continue
        elif query == '!quit':
            sys.exit()

        try:
            db.get(query)
        except ValueError:
            print('Invalid query, try again.')
            continue

main()

    


