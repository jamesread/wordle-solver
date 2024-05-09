#!/usr/bin/env python

from wordfreq import word_frequency
from english_words import get_english_words_set
import argparse

enwords = get_english_words_set(['web2'], lower = True)
enwords = sorted(enwords)

class Solver():
    unusedLetters = set()
    lettersInWrongPlace = dict()
    solved = dict()
    length = 0

    def __init__(self, length):
        self.reset()

    def reset(self):
        self.index = -1
        self.unusedLetters = set()
        self.lettersInWrongPlace = dict()
        self.solved = dict()
        self.length = 5

    def addResultLetter(self, resultCharacter, resultType):
        resultCharacter = resultCharacter.upper()

        if self.index + 1 == self.length:
            self.index = -1

        self.index += 1

        match resultType:
            case "solved":
                self.solved[self.index] = resultCharacter
                return "solved-letter"

            case "wrong-position":
                if resultCharacter not in self.lettersInWrongPlace:
                    self.lettersInWrongPlace[resultCharacter] = []

                self.lettersInWrongPlace[resultCharacter].append(self.index)
                return

            case "unused":
               if resultCharacter in self.solved.values(): return "error-unused-in-solved"
               if resultCharacter in self.lettersInWrongPlace: return "error-unused-in-wrong-place"

               self.unusedLetters.add(resultCharacter)
               return

            case _:
               raise Error("Unknown type: " + resultType)


    def wordExists(self, word):
        return word.lower() in enwords

    def isCandidate(self, word):
        word = word.upper()

        if len(word) != self.length: return False

        for bl in self.unusedLetters:
            if bl in word:
                print(word, "contains bad letter", bl)
                return False

        for c in self.lettersInWrongPlace:
            if c not in word:
                print(word, "does not contain needed letter", c)
                return False

            for i in self.lettersInWrongPlace[c]:
                print(c, i, word, self.lettersInWrongPlace)
                if word[i] == c:
                    print(word, "cannot have a", c, "at position", i)
                    return False

        for i in self.solved:
            solvedCharacter = self.solved[i]

            if word[i].upper() != self.solved[i]:
                print(word, "word does not have a", solvedCharacter, "at position", i)
                return False

        return True

    def getCandidateRanking(self, entry):
        word = entry['word']

        uniqueChars = set(word)

        newCharCount = 0

        for c in uniqueChars:
            if c not in self.solved:
                newCharCount = newCharCount + 1


        entry['ranking'] = len(uniqueChars) + (newCharCount * len(uniqueChars)) * word_frequency(word, 'en')

        return entry['ranking']

    def findCandidates(self):
        global enwords

        candidates = list()

        for word in enwords:
            if self.isCandidate(word):
                candidates.append({
                    "word": word,
                    "ranking": 0,
                    })

        return sorted(candidates, key=self.getCandidateRanking)

    def isSolved(self):
        if "_" in self.solved:
            return False
        else:
            return True
