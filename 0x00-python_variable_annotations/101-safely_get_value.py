#!/usr/bin/env python3
""" Augment the following code with the correct duck-typed annotations:
    The types of the elements of the input are not know """
from typing import Mapping, Any, Union, TypeVar


T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """ Augment the following code with the correct duck-typed annotations:
        The types of the elements of the input are not know """
    if key in dct:
        return dct[key]
    else:
        return default
