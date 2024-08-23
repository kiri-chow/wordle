#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 13:07:03 2024

@author: anthony
"""
import asyncio
import requests


URL = "https://fly.wordfinderapi.com/api/search"


async def get_dictionary(length: int = 5) -> list[str]:
    # load the first page
    words, total_pages = await _download_words(length, 1)

    # load the rest pages
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_download_words(length, p))
                 for p in range(2, total_pages + 1)]

    for task in tasks:
        words_ext, _ = task.result()
        words.extend(words_ext)
    return words


async def _download_words(length: int, page: int) -> (list[str], int):
    "download words from Wordtips"
    response = requests.get(
        URL, params={"length": length, "page_token": page,
                     "page_size": 100, 'dictionary': 'all_en'}
    )
    data = response.json().get("word_pages", [])[0]
    words = [x['word'] for x in data.get("word_list", [])]
    total_pages = data.get("num_pages", 0)
    return words, total_pages
