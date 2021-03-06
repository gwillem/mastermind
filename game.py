#!/usr/bin/env python3

import sys
import random
import unittest

COLORCODES = [
    '7;30;1',
#    '7;31;1',
    '7;31;2',
    '7;32;1',
    '7;33;1',
    '7;34;1',
    '7;35;1',
    '7;36;1',
    '7;37;1',
]

COLORS = {i+1: "\033[{}m{} \033[0m".format(x, i+1) for i, x in enumerate(COLORCODES)}
WIDTH = 4


def allcolors():
    base = '\033[%sm'
    reset = '\033[0m'

    for bold in (1, 2):
        for y in range(1, 8):
            for x in range(30, 38):
                sys.stdout.write('\033[{};{};{}m'.format(y, x, bold) + '{};{};{}'.format(y,x,bold) + reset)
        print()


def tuple_intersection(t1, t2):
    i = 0        
    t2 = list(t2)
    for x in t1:
        if x in t2:
            t2.remove(x)
            i += 1

    return i 


def tuple_match(t1, t2):
    assert len(t1) == len(t2)

    found = 0
    for i, v in enumerate(t1):
        if t2[i] == v:
            found += 1

    return found


def permute(lol):
    # lol = list of lists
    if not isinstance(lol[0], list):
        lol[0] = list(lol[0])
        
    random.shuffle(lol[0])
    for x in lol[0]:
        if lol[1:]:
            for y in permute(lol[1:]):
                yield [x] + y
        else:
            yield [x]


class Game:

    width = WIDTH
    pinidx = tuple(range(WIDTH))
    coloridx = tuple(COLORS)

    def __init__(self, combo=None):
        self.truth = combo or Combo()
        self.finished = False

    def finish(self):
        self.finished = True

    def guess(self, combo):
        assert not self.finished, 'Game already finished'

        red, white = self.verdict(self.truth, combo)
        if red == self.width:
            self.finish()

        return red, white

    @staticmethod
    def verdict(combo1, combo2):
        """ Return number of red (right color, right position) and white (just right color) """

        red = tuple_match(combo1.seq, combo2.seq)
        white = tuple_intersection(combo1.seq, combo2.seq) - red

        return red, white


class Combo:

    def __init__(self, seq=None, **kwargs):
        self.seq = seq or self.create_seq(**kwargs)
        assert isinstance(self.seq, tuple) 

    def __hash__(self):
        return hash(self.seq)

    def create_seq(self, forbidden=None):
        possibles = list(Game.coloridx)

        if forbidden:
            for x in forbidden:
                possibles.remove(x)

        return tuple([random.choice(possibles) for _ in range(WIDTH)])

    def __str__(self):
        return " ".join([COLORS[x] for x in self.seq])
