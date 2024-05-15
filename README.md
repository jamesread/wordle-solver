# wordle-solver

A very simple python script to solve (bruteforce) wordle. 

![screenshot](screenshot.png)

This app has a solve rate within the very high 90% - probably 98%, and most of the time loss is simply down to human input error or occasionally words not existing in the dictionary, otherwise, it generally destroys, I mean, solves, wordle, very nicely :)

* [Wordle - Original game](https://www.nytimes.com/games/wordle/index.html) 
* [Wordly - allows infinate plays](https://wordly.org/)

## Interesting game variations 

* [Octordle - Paralell 8 way](https://www.britannica.com/games/octordle/)
* [Victordle - Multipler supposedly, but feels like bots](https://www.britannica.com/games/victordle/), this app scores on average 81% win over 50 games (the 20% "loss" is that sometimes the opponent guesses correctly first!)

## Installation (docker container)

	docker create --name wordle-solver -p 8080:8080 ghcr.io/jamesread/wordle-solver

## Installation (local)

Pip install the dependencies;

    pip install enwords
    pip install wordfreq

## Run

    ./wordle-solver.py
