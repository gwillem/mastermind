#!/usr/bin/env python3

import tty
import sys
import termios
import time
from game import Combo, Game, COLORS
from visualclient import show_turn, LEFTPADDED
import subprocess



def getchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    if ord(ch) == 3:  # control-c
        sys.exit(1)

    return ch


def write(c):
    sys.stdout.write(c)
    sys.stdout.flush()

def read_guess():

    guess = []

    while True:

        available_colors = ' '.join([COLORS[i] for i in sorted(COLORS)])
        statusline = " " * LEFTPADDED + "{}" + "     (kies: {})\r".format(available_colors)
        
        alreadyguessed = ''.join([COLORS[i] + ' ' for i in guess])

        # need manual padding because the string contains
        # non-displayed control characters
        padding = ' ' * (Game.width * 3 - len(guess) * 3)
        # print("padding lngth:", len(padding)) 
        alreadyguessed += padding
        write(statusline.format(alreadyguessed))


        ch = getchar()
        # write('char {}\n'.format(ord(ch)))

        if ord(ch) == 127 and guess:  # backspace
            # write('backspace!\n')
            guess.pop()
        elif ord(ch) == 13 and len(guess) == Game.width:  # enter
            break
        elif ch.isnumeric():
            n = int(ch)
            if len(guess) == Game.width:
                guess[-1] = n
            else:
                guess.append(n)


    return tuple(guess)

if __name__ == '__main__':

    combo = Combo()


    while True:
        game = Game(combo)

        print("We gaan beginnen!\n")
        print(' ' * LEFTPADDED  + ''.join(['?? ' for _ in game.truth.seq]))
        print("\n\t" + "=" * (game.width * 2 + 4 + game.width - 1))

        for i in range(12):
            myguess = Combo(read_guess())
            red, white = game.guess(myguess)
            show_turn(i+1, myguess, red, white)
            if game.finished: 
                break

        if game.finished:
            print("Je hebt gewonnen na {} pogingen".format(i+1))
        else:
            print("Helaas.. geen MasterMind Kampioen van Val Godard dit keer.")
            print("Het was: ", game.truth)

        print('\n\n\n(druk op enter om opnieuw te beginnen)')
        input()
        subprocess.call(['clear'])



    # while True:
    #     ch = getchar()
    #     print("\rGot char {} == chr({})".format(ch, ord(ch)), end='')
    #     if ord(ch) == 3:
    #         print("Control C")
    #         break

