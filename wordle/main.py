#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 15:20:10 2024

@author: anthony
"""
import time
import asyncio
from wordle.words_dictionary import get_dictionary
from wordle.agents import SmartAgent


async def main():
    print('Downloading the dictionary...')
    dictionary = await get_dictionary()
    print('Download completed')

    agent = SmartAgent(dictionary=dictionary)

    start = time.time()
    word, times = agent.guess()
    stop = time.time()

    print(
        f"The word is {word}. \nGuessed for {times} times. \nSpent {stop - start:.2f} seconds.")


if __name__ == '__main__':
    asyncio.run(main())
