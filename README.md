# Wordle

A demo program for the Wordle game of Votee.

## Agents

There are 2 agents available for this game:
1. `DullAgent`, constructs words from the present list after checking all the charactors.
2. `SmartAgent`, filters words from a given dictionary while guessing. It will also guess from the present list if the correct word is out of the dictionary.

You can call `agent.guess()` to guess the daily word after instantition.

## Run

Install this project.
```
poetry install
```

Guess the daily word with SmartAgent.
```
python wordle/main.py
```
