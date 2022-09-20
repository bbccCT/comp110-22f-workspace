"""A series of tests meant for each function in utils.py for EX05."""

__author__ = "930605992"


from utils import only_evens, sub, concat

def test_only_evens_empty() -> None:
    xs: list[int] = []
    assert only_evens(xs) == []

def test_only_evens_single_odd() -> None:
    xs: list[int] = [27]
    assert only_evens(xs) == []
    
def test_only_evens_single_even() -> None:
    xs: list[int] = [42]
    assert only_evens(xs) == [42]

def test_only_evens_many_items() -> None:
    xs: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    assert only_evens(xs) == [0, 2, 4, 6, 8 ,10, 12, 14, 16]

def test_only_evens_many_items_unordered_and_negatives() -> None:
    xs: list[int] = [-31, 0, 12, 17, -3, 5, -12, 17, 6, 6, 17]
    assert only_evens(xs) == [0, 12, -12, 6, 6]


def test_concat_both_empty() -> None:
    xs: list[int] = []
    ys: list[int] = []
    assert concat(xs, ys) == []

def test_concat_first_empty() -> None:
    xs: list[int] = []
    ys: list[int] = [10, 20, 30]
    assert concat(xs, ys) == [10, 20, 30]

def test_concat_second_empty() -> None:
    xs: list[int] = [10, 20, 30]
    ys: list[int] = []
    assert concat(xs, ys) == [10, 20, 30]

def test_concat_many_items() -> None:
    xs: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ys: list[int] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    assert concat(xs, ys) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

def test_concat_many_items_unordered_and_negative() -> None:
    xs: list[int] = [-20, 5, 72, -400, 12442666166777543854921011, -2]
    ys: list[int] = [42, 42, 42, 42, -13, 12, -909, 404]
    assert concat(xs, ys) == [-20, 5, 72, -400, 12442666166777543854921011, -2, 42, 42, 42, 42, -13, 12, -909, 404]


def test_sub_empty() -> None:
    xs: list[int] = []
    start: int = 0
    end: int = 10
    assert sub(xs, start, end) == []

def test_sub_negative_start() -> None:
    xs: list[int] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    start: int = -6
    end: int = 3
    assert sub(xs, start, end) == [10, 20, 30]

def test_sub_overshot_end() -> None:
    xs: list[int] = [1, 2, 3, 4, 5]
    start: int = 1
    end: int = 10
    assert sub(xs, start, end) == [2, 3, 4, 5]

def test_sub_overshot_start() -> None:
    xs: list[int] = [1, 2, 3, 4, 5]
    start: int = 10
    end: int = 15
    assert sub(xs, start, end) == []

def test_sub_end_zero() -> None:
    xs: list[int] = [1, 2, 3, 4, 5]
    start: int = 0
    end: int = 0
    assert sub(xs, start, end) == []

def test_sub_swapped_indices() -> None:
    xs: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    start: int = 6
    end: int = 2
    assert sub(xs, start, end) == []

def test_sub_single() -> None:
    xs: list[int] = [1, 2, 3, 4, 5]
    start: int = 2
    end: int = 3
    assert sub(xs, start, end) == [3]

def test_sub_same_index() -> None:
    xs: list[int] = [1, 2, 3, 4, 5]
    start: int = 2
    end: int = 2
    assert sub(xs, start, end) == []

def test_sub_many_items() -> None:
    xs: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    start: int = 4
    end: int = 10
    assert sub(xs, start, end) == [5, 6, 7, 8, 9, 10]

def test_sub_many_items_unordered_and_negative() -> None:
    xs: list[int] = [-9, 5, 30, -22, 0, 558, -1111]
    start: int = 3
    end: int = 6
    assert sub(xs, start, end) == [-22, 0, 558]