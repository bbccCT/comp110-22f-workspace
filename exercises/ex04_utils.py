"""EX04 - An exercise where some useful functions are created from lower-level functions we have learned so far."""

__author__ = "930605992"


def all(int_list: list[int], num_to_match: int) -> bool:
    """Do all the items in this list match this number?"""
    i: int = 0
    if len(int_list) == 0:
        return False
    while i < len(int_list):
        if int_list[i] == num_to_match:
            i += 1
        else:
            return False
    return True


def max(int_list: list[int]) -> int:
    """What is the maximum number in this list?"""
    if len(int_list) == 0:
        raise ValueError("max() arg is an empty list")
    current_max: int = int_list[0]
    i: int = 0
    while i < len(int_list):
        if int_list[i] > current_max:
            current_max = int_list[i]
        i += 1
    return current_max


def is_equal(int_list_1: list[int], int_list_2: list[int]) -> bool:
    """Checks whether two lists are deeply equal."""
    if len(int_list_1) != len(int_list_2):
        return False
    elif len(int_list_1) == 0:
        return True
    i: int = 0
    while i < len(int_list_1):
        if int_list_1[i] == int_list_2[i]:
            i += 1
        else:
            return False
    return True