#!/usr/bin/env python3
"""[summary] Async basics in Python task 0"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """[summary] Async basics in Python task 0"""
    random_float = random.uniform(0, max_delay)
    await asyncio.sleep(random_float)
    return random_float
