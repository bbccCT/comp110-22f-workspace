"""Some function skeletons and implementations being written for EX05."""

__author__ = "930605992"


def only_evens(int_list: list[int]) -> list[int]:
    """Returns only the even elements of the input list."""
    evens: list[int] = []
    i: int = 0
    while i < len(int_list):
        if int_list[i] % 2 == 0:
            evens.append(int_list[i])
    return evens

def concat(list_1: list[int], list_2: list[int]) -> list[int]:
    """Returns a single list with all elements of the first list followed by all elements of the second list."""
    combined: list[int] = []
    i: int = 0
    while i < len(list_1):
        combined.append(list_1[i])
    i = 0
    while i < len(list_2):
        combined.append(list_2[i])
    return combined

def sub(int_list: list[int], start_idx: int, end_idx: int) -> list[int]:
    """Returns a subset of a list between given indices (including starting index)."""
    subset: list[int] = []
    if start_idx < 0:
        start_idx = 0
    if end_idx > len(int_list):
        end_idx = len(int_list)
    if len(int_list) == 0 or start_idx > len(int_list) or end_idx <= 0 or start_idx <= end_idx:
        return subset
    i: int = start_idx
    while i < end_idx:
        subset.append(int_list[i])
    return subset