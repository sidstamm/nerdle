#!/bin/python3

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# NERDLE!
#
# an interactive "wordle-like" game
#
# Sid Stamm <sidstamm@gmail.com>
# February 2022

import random
from random import sample
from colors import * # this is from the ansicolors package

with open("/usr/share/dict/words") as f:

    # grab 5-letter words and strip off whitespace, then upcase
    candidates = [x.strip().upper() for x in f.readlines() if len(x.strip()) == 5]
    # remove words with special chars
    candidates = list(filter(lambda x: not any(c in x for c in " -'"), candidates))

    print("loaded %d words" % (len(candidates)))

    # Pick the NERDLE
    ANSWER = sample(candidates,1)[0]

    def anyInRightPlace(c, guess, target):
        return any([x == c and x == y for x,y in zip(guess,target)])

    def printColorWord(word, target):
        for c1, c2 in zip(word, target):
            colors=('dimgrey', 'rgb(0,0,0)') #default: not in target
            if c1 == c2:
                colors=('black', 'green')    #it's in the right place!
            elif c1 in target:
                colors=('black', 'goldenrod') #anywhere in any guessed word
            print(color(c1, fg=colors[0], bg=colors[1]), end='')
        print()

    def printColorAlphabet(guesses, target):
        guessed = set([c for w in guesses for c in w])  #_o/ ALL THE LETTERS

        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            # Default: unguessed letters
            colors = ('black', 'dimgrey')
            if c in guessed and c not in target:
                # Eliminated letters
                colors=('dimgrey', 'rgb(0,0,0)')
            elif c in target:
                if any([c in g for g in guesses]):
                    colors=('black', 'goldenrod') #anywhere in any guessed word
                if any([anyInRightPlace(c, g, target) for g in guesses]):
                    colors=('black', 'green')     #right place in a guessed word
            print(color(c, fg=colors[0], bg=colors[1]), end='')
        print()


    def printGuesses(guesses):
        [printColorWord(x, ANSWER) for x in guesses]
        for i in range(6-len(guesses)):
            print("-----")

    # Uncomment this line to cheat.
    #print(f'Answer: {ANSWER}\n')

    NERDLE = []   # This is where guesses go

    printGuesses(NERDLE)
    while len(NERDLE) < 6:

        print()
        printColorAlphabet(NERDLE, ANSWER)

        print()
        guess = input("Guess > ").upper()
        if len(guess) != 5:
            print("Guess needs to be five letters.\n")
            continue
        if guess not in candidates:
            print("That's not an acceptable word.\n")
            continue

        NERDLE.append(guess)
        print("\n\n===============================\n")
        printGuesses(NERDLE)

        if guess == ANSWER:
            print(f'You got it in {len(NERDLE)}!')
            break

        if len(NERDLE) > 5:
            print(f'The nerdle was {ANSWER}!')
            print("Too many tries, game over.  :( :( :( :(\n")
            break

        print("\n")
