#!/bin/usr/env python3
""" Complex types - string and int/float to tuple """
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Takes a string k and an int OR float v as arguments and
    returns a tuple.
    The first element of the tuple is the string k.
    The second element is the square of the int/float v and is annotated
    as a float.
    """
    return (k, v**2)
