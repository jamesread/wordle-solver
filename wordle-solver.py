#!/usr/bin/env python

from wordfreq import word_frequency
from english_words import english_words_lower_set as enwords
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--length", type = int, default = 5)
parser.add_argument("--lookup", type = str, default = "")
args = parser.parse_args()

badLetters = set() 
lettersInWrongPlace = dict()
solved = "_" * args.length

def enterGuessResult(): 
    global solved
    global badLetters
    global lettersInWrongPlace

    i = -1

    print("Green letters:\tUppercase")
    print("Orange letters:\tLowercase")
    print("Gray letters:\tspacebar")
    print("")

    for c in input("Guess result: "):
        i = i + 1

        if c == " ":
            continue 

        if c.isupper(): 
            solved = solved[:i] + c + solved[i+1:]
            continue

        if c.islower(): 
            if c not in lettersInWrongPlace:
                lettersInWrongPlace[c] = [i]
            else:
                lettersInWrongPlace[c].append(i)


def enterUnusedLetters():
    for c in input("Enter unused: "):
        if c in solved.lower(): continue
        if c in lettersInWrongPlace: continue

        badLetters.add(c)

def isCandidate(word):
    global badLetters
    global solved
    global lettersInWrongPlace
    global args

    if len(word) != args.length: return False

    for bl in badLetters: 
        if bl in word: 
            print (word, "contains bad letter", bl)
            return False

    for c in lettersInWrongPlace:
        if c not in word:
            print(word, "does not container needed letter", c)
            return False

        for i in lettersInWrongPlace[c]:
            if word[i] == c:
                print(word, "cannot have a", c, "at position", i)
                return False

    for i in range(args.length): 
        solvedCharacter = solved[i]
        print(i, solvedCharacter, solved, word)

        if solvedCharacter != "_":
            print(i, solvedCharacter)

            if word[i].upper() != solvedCharacter:
                print(word, "word does not have a", solvedCharacter, "at position", i)
                return False

    return True

def getCandidateRanking(entry):
    word = entry['word']

    uniqueChars = set(word)

    newCharCount = 0

    for c in uniqueChars:
        if c not in solved.lower():
            newCharCount = newCharCount + 1


    entry['ranking'] = len(uniqueChars) + (newCharCount * len(uniqueChars)) * word_frequency(word, 'en')

    return entry['ranking']

def findCandidates():
    global enwords

    candidates = list()

    for word in enwords:
        if isCandidate(word):
            candidates.append({
                "word": word,
                "ranking": 0,
            })

    return sorted(candidates, key=getCandidateRanking)
        
def printTurnStatus():
    global solved
    global badLetters
    global lettersInWrongPlace

    print("")
    print("Turn status: ")
    print("\tSolved:", solved)
    print("\tbadLetters:", badLetters)
    print("\tlettersInWrongPlace:", lettersInWrongPlace)
    print("")

def printSeparator():
    print("")
    print("-------------")
    print("")


print("wordle-solver")
print("")

if args.lookup != "":
    print(args.lookup in enwords)
    exit()

print("Hint: ATONE is a good first guess - high frequency EN letters")
printSeparator()

while "_" in solved: 
    print("Type in a guess, and enter the result!")
    print("")

    enterGuessResult()
    enterUnusedLetters()

    candidates = findCandidates()

    printSeparator()
    printTurnStatus()
    printSeparator()
 
    if len(candidates) == 0:
        print("Cannot solve")
        break

    if len(candidates) == 1:
        print("Hopefully that is the answer!")
        print("Answer =", next(iter(candidates))['word'])
        break

    else: 
        print ("Candidates....")

        for candidate in candidates:
            print("-", candidate['ranking'], candidate['word'])

