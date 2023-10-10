#!/usr/bin/env python3
"""This module contains the function for task 3"""
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """[summary] Async basics in Python task 3"""
    return asyncio.create_task(wait_random(max_delay))
