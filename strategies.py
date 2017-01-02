#!/usr/bin/env python3

import random
from statistics import mean
from game import Game, Combo


def choice(i):
    # random.choice from iterator i, because random.choice 
    # doesn't work on sets
    if not isinstance(i, list):
        i = list(i)
    return random.choice(i) 



class Strategy:
    
    def __init__(self, game=None):
        # print("Strategy {} starting".format(type(self).__name__))
        self.game = game or Game()

    def fullgame(self, turn_cb=None):
        i = 0
        while not self.game.finished:
            i += 1
            combo = self.next_guess()
            red, white = self.game.guess(combo)
            self.parse_turn(combo, red, white)
            if turn_cb:
                turn_cb(i, combo, red, white)

        return i

    @classmethod
    def benchmark(cls, runs=100):
        results = list()
        for x in range(runs):
            tries = cls().fullgame()
            # print("Game finished after {} tries".format(tries))
            results.append(tries)

        avg = mean(results)
        print("Benchmark results for {}: {:.1f}".format(cls.__name__, avg))
        return avg

    def parse_turn(self, combo, red, white):
        # to refine stats, implement state etc
        pass

    def next_guess(self):
        raise RuntimeError('not implemented here')

class RandomStrategy(Strategy):

    def next_guess(self):
        return Combo()

class BasicExclusionStrategy(Strategy):


    """
    1. Play random combos
    1. red+white = 0? don't play these colors again
    1. 0 red? remove these colors per position 
    1. Keep history. Don't play combo's that conflict with history. How can it conflict?
        1. If zero red, same position (we already have that)
        1. Per historical move, compare next combo, should have at least as many red/white for each combo


    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = dict()
        self.choices_per_pin = {p:set(self.game.coloridx) for p in self.game.pinidx}
        self.known_colors = []

    def parse_turn(self, combo, red, white):

        self.history[combo.seq] = (red, white)


        if red == self.game.width:
            pass

        elif red + white == 0:
            for color in set(combo.seq):
                for choices in self.choices_per_pin.values():
                    if color in choices:
                        choices.remove(color)

        elif white + red == self.game.width:
            self.known_colors = list(combo.seq)

        elif white and not red:
            for i, color in enumerate(combo.seq):
                self.choices_per_pin[i].remove(color)

    def next_guess(self):

        i = 0 
        while True:
            i += 1

            # if i % 10000 == 0:
            #     print("Oops, {} tries for a new guess".format(i))


            if self.known_colors:
                seq = list(self.known_colors)
                random.shuffle(seq)
                seq = tuple(seq)
            else:
                seq = tuple(
                    choice(self.choices_per_pin[p]) 
                    for p in self.game.pinidx
                )

            if seq not in self.history and self.honors_history(seq):
                # if i > 1000:
                #     print("oops, had to try {} times before i found a unique possibility".format(i))
                return Combo(seq)

    def honors_history(self, proposed):
        # does proposed seq comply with all previous turns?
        # print("self hist is", self.history)
        for previous, verdict in self.history.items():
            red, white = verdict
            if not self.valid_turn(previous, red, white, proposed):
                return False

        return True

    def valid_turn(self, previous, red, white, proposed):
        # check whether exactly red+white colors are the same
        # samecolors = red + white
        if self.tuple_intersection(previous, proposed) != red + white:
            return False

        # check whether at least red colors are on the same pin
        if self.tuple_match(previous, proposed) != red:
            return False

        return True

    @staticmethod
    def tuple_intersection(t1, t2):
        i = 0        
        t2 = list(t2)
        for x in t1:
            if x in t2:
                t2.remove(x)
                i += 1

        return i 

    @staticmethod
    def tuple_match(t1, t2):
        assert len(t1) == len(t2)

        found = 0
        for i, v in enumerate(t1):
            if t2[i] == v:
                found += 1

        return found


def main():

    # RandomStrategy.benchmark(100)
    BasicExclusionStrategy.benchmark(1000)

if __name__ == '__main__':
    main()