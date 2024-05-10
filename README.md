# wordle-solver

A very simple python script to solve (bruteforce) wordle. 

![screenshot](screenshot.png)

* [Wordle - Original game](https://www.powerlanguage.co.uk/wordle/)
* [Hello Wordl - clone that allows infinate plays per day](http://foldr.moe/hello-wordl/)

## Installation (docker container)

	docker create --name wordle-solver -p 8080:8080 ghcr.io/jamesread/wordle-solver

## Installation (local)

Pip install the dependencies;

    pip install enwords
    pip install wordfreq

## Run

    ./wordle-solver.py
