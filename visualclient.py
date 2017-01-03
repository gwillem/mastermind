#!/usr/bin/env python3

from strategies import BasicExclusionStrategy
from game import Game, WIDTH


LEFTPADDED = 10 

class Colors:

    @staticmethod
    def Red(s):
        return "\033[1;31;1m{}\033[0m".format(s)

    @staticmethod
    def White(s):
        return "\033[1;37;1m{}\033[0m".format(s)


def show_turn(i, combo, red, white):

    r = Colors.Red("{} red".format(red)) if red else "     "
    a = ", " if (red and white) else "  "
    w = Colors.White("{} white".format(white)) if white else "     "
    score = r+a+w


    print(("{:2d}."+" "*(LEFTPADDED-3)+"{}        {:<80}\n").format(
        i, combo, score
    ))


if __name__ == '__main__':
    game = Game()
    print("Game started!\n")
    print(game.truth)
    print("\n\t" + "=" * (WIDTH * 2 + 4 + WIDTH - 1))

    s = BasicExclusionStrategy(game=game)



    s.fullgame(turn_cb=show_turn)
