#!/usr/bin/env python

from english_words import english_words_lower_set as enwords

letterFrequency = {'e': 12000, 't': 9000, 'a': 8000, 'i': 8000, 'n': 8000, 'o': 8000, 's': 8000, 'h': 6400, 'r': 6200, 'd': 4400, 'l': 4000, 'u': 3400, 'c': 3000, 'm': 3000, 'f': 2500, 'w': 2000, 'y': 2000, 'g': 1700, 'p': 1700, 'b': 1600, 'v': 1200, 'k': 800, 'q': 500, 'j': 400, 'x': 400, 'z': 200, "'": 0, '.': 0}

candidates = list()

for word in enwords:
    if len(word) != 5: continue

    score = 0

    for c in word:
        score += letterFrequency[c]

    candidates.append({
        "word": word,
        "score": score,
    })

sorted_candidates = sorted(candidates, key=lambda v: len(set(v['word'])) * v['score'])

for candidate in sorted_candidates:
    print(candidate['score'], candidate['word'])
    
