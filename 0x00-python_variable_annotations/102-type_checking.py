#!/usr/bin/env python3
""" Augment the following code with the correct duck-typed annotations:
    The types of the elements of the input are not know """
from typing import Tuple, List


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """ Augment the following code with the correct duck-typed annotations:
        The types of the elements of the input are not know """
    zoomed_in: List[int] = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)
zoom_2x = zoom_array(array)
zoom_3x = zoom_array(array, 3)
