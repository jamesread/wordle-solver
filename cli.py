#!/usr/bin/env python

from wordfreq import word_frequency
from solver import Solver
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--length", type = int, default = 5)
parser.add_argument("--lookup", type = str, default = "")
args = parser.parse_args()

def printTurnStatus(solver):
    print("")
    print("Turn status: ")
    print("\tSolved:", solver.solved)
    print("\tUnused Letters:", solver.unusedLetters)
    print("\tLetters In Wrong Place:", solver.lettersInWrongPlace)
    print("")

def printSeparator():
    print("")
    print("-------------")
    print("")

def main():
    solver = Solver(args.length)

    print("wordle-solver")
    print("")

    if args.lookup != "":
        print(solver.wordExists(args.lookup))
        exit()

    print("Hint: ATONE is a good first guess - high frequency EN letters")
    printSeparator()

    while not solver.isSolved():
        print("Type in a guess, and enter the result!")
        print("")

        print("Green letters:\tUppercase")
        print("Orange letters:\tLowercase")
        print("Gray letters:\tspacebar")
        print("")

        guess = input("Guess result: ")

        solver.addResult(guess)

        unused = input("Enter unused: ")
        solver.addUnusedLetters(unused)

        candidates = solver.findCandidates()

        printSeparator()
        printTurnStatus(solver)
        printSeparator()

        if len(candidates) == 0:
            print("Cannot solve")
            break

        if len(candidates) == 1:
            print("There is only one possible answer left - hopefully that is the answer!")
            print("Answer =", next(iter(candidates))['word'])
            break
        else:
            print ("Candidates....")

            for candidate in candidates:
                print("-", candidate['ranking'], "\t", candidate['word'])


if __name__ == "__main__":
    main()
