#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 13:52:10 2024

@author: anthony
"""
import requests
from itertools import product


class BaseWordleAgent:

    def __init__(self, length: int = 5, seed: int = None):
        self.length = length
        self.times = 0
        self.present = set()
        self.absent = set()
        self.slots = {}
        self.seed = seed

        start = ord('a')
        self.alphabet = {chr(start + i) for i in range(26)}

    @property
    def url(self) -> str:
        if self.seed is None:
            return 'https://wordle.votee.dev:8000/daily'
        return f'https://wordle.votee.dev:8000/random?seed={self.seed}'

    def _clear_memory(self):
        self.times = 0
        self.present.clear()
        self.absent.clear()
        self.slots.clear()

    def guess_once(self, word: str) -> bool:
        "guess once and update memories, return True if the guess is correct"
        response = requests.get(self.url, params={'guess': word})
        data = response.json()

        result = True
        for char in data:
            if char['result'] == 'correct':
                self.slots[char['slot']] = char['guess']
                self.present.add(char['guess'])
            else:
                result = False
                getattr(self, char['result']).add(char['guess'])
        self.times += 1
        return result

    def _guess_from_absent(self):
        # permutate present chars
        for word in product(*[self.present] * self.length):
            word = ''.join(word)
            if self._check_word(word):
                result = self.guess_once(word)
                if result:
                    return word, self.times
        raise RuntimeError("Can not guess the word.")

    def _check_word(self, word) -> bool:
        "check if the word match the memory"
        chars = set(word)

        # check absent
        if self.absent & chars:
            return False

        # check present
        if len(chars | self.present) > self.length:
            return False

        # check correct slots
        for ind, char in enumerate(word):
            target = self.slots.get(ind)
            if target and char != target:
                return False
        return True


class DullAgent(BaseWordleAgent):
    """
    Guess the word after checking all present charactors.

    params
    ------
    length : int,
        The length of the word.
    seed : int or None,
        The seed for random guess. None stands for daily guess.

    """

    def guess(self) -> (str, int):
        "return the correct word and guess times."
        self._clear_memory()
        alphabet = list(self.alphabet)
        dull_list = (''.join(alphabet[i * self.length: (i + 1) * self.length])
                     for i in range(len(alphabet) // self.length + 1))

        # get present chars
        for word in dull_list:
            result = self.guess_once(word)
            if result:
                return word, self.times
            if (len(self.present) >= self.length
                    or len(self.present) + len(self.absent) >= len(self.alphabet)):
                break

        return self._guess_from_absent()


class SmartAgent(BaseWordleAgent):
    """
    Agent with dictionary

    params
    ------
    length : int,
        The length of the word.
    seed : int or None,
        The seed for random guess. None stands for daily guess.
    dictionary : list[str],
        The word list helps to reduce the guess space.

    """

    def __init__(self, *args, dictionary: list[str], **kwargs):
        super().__init__(*args, **kwargs)
        self.dictionary = sorted(dictionary,
                                 key=lambda x: len(set(x)), reverse=True)

    def guess(self) -> (str, int):
        "return the correct word and guess times."
        self._clear_memory()

        for word in self.dictionary:
            if not self._check_word(word):
                continue
            result = self.guess_once(word)
            if result:
                return word, self.times

        # try absent list to catch words not in the dictionary
        return self._guess_from_absent()
