#!/usr/bin/env python

from english_words import english_words_lower_set as enwords

badLetters = set() 
lettersInWrongPlace = set()
solved = "_____"

def enterGuessResult(): 
    global solved
    global badLetters
    global lettersInWrongPlace

    i = -1

    print("HELP: Green letters: Uppercase")
    print("HELP: Orange letters: Lowercase")
    print("HELP: Gray letters: spacebar")
    print("")

    for c in input("Guess result: "):
        i = i + 1

        if c == " ":
            continue 

        if c.isupper(): 
            solved = solved[:i] + c + solved[i+1:]
            continue

        if c.islower(): 
            lettersInWrongPlace.add(c)

def enterUnusedLetters():
    for c in input("Enter unused: "):
        if c in solved.lower(): continue

        badLetters.add(c)

def isCandidate(word):
    global badLetters
    global solved
    global lettersInWrongPlace


    if len(word) != 5: return False

    for bl in badLetters: 
        if bl in word: 
            print (word, "contains bad letter", bl)
            return False

    for c in lettersInWrongPlace:
        if c not in word:
            print(word, "does not container needed letter", c)
            return False

    for i in range(5): 
        solvedCharacter = solved[i]
        print(i, solvedCharacter, solved, word)

        if solvedCharacter != "_":
            print(i, solvedCharacter)

            if word[i].upper() != solvedCharacter:
                print(word, "word does not have a", solvedCharacter, "at position", i)
                return False

    return True

def findCandidates():
    global enwords

    candidates = set()

    for word in enwords:
        if isCandidate(word):
            candidates.add(word)

    return candidates
        

while "_" in solved: 
    print("")
    print("Turn status: ")
    print("  Solved:", solved)
    print("  badLetters:", badLetters)
    print("  lettersInWrongPlace:", lettersInWrongPlace)
    print("")
    print("Type in a guess, and enter the result!:")
    print("")

    enterGuessResult()
    enterUnusedLetters()

    candidates = findCandidates()

    print("")
    print("-------------")
    print("")

    if len(candidates) == 0:
        print("Cannot solve")
        break

    if len(candidates) == 1:
        print("Hopefully that is the answer!")
        print("Answer =", next(iter(candidates)))
        break

    else: 
        print ("Candidates....")

        for candidate in candidates:
            print("-", candidate)

