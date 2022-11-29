"""Tests for linked list utils."""

import pytest
from exercises.ex11.linked_list import Node, last, value_at, max, linkify, is_equal, scale

__author__ = "730605992"


def test_last_empty() -> None:
    """Last of an empty Linked List should raise a ValueError."""
    with pytest.raises(ValueError):
        last(None)


def test_last_non_empty() -> None:
    """Last of a non-empty list should return its last data value."""
    linked_list: Node = Node(1, Node(2, Node(3, None)))
    assert last(linked_list) == 3


def test_value_at_empty() -> None:
    """Requesting value at index in an empty linked list."""
    with pytest.raises(IndexError):
        value_at(None, 1)


def test_value_at_index_zero() -> None:
    """Requesting value at index 0 in a linked list."""
    linked_list: Node = Node(1, Node(2, Node(3, None)))
    assert value_at(linked_list, 0) == 1


def test_value_at_index_nonzero() -> None:
    """Requesting value at normal index in a linked list."""
    linked_list: Node = Node(1, Node(2, Node(3, None)))
    assert value_at(linked_list, 2) == 3


def test_value_at_index_out_of_bounds() -> None:
    """Requesting value at out of bounds index in a linked list."""
    linked_list: Node = Node(1, Node(2, Node(3, None)))
    with pytest.raises(IndexError):
        value_at(linked_list, 3)


def test_max_asc() -> None:
    """Requesting maximum value of linked list with values in ascending order."""
    linked_list: Node = Node(10, Node(20, Node(30, None)))
    assert max(linked_list) == 30


def test_max_desc() -> None:
    """Requesting maximum value of linked list with values in descending order."""
    linked_list: Node = Node(30, Node(20, Node(10, None)))
    assert max(linked_list) == 30


def test_max_unordered() -> None:
    """Requesting maximum value of linked list with values in neither ascending nor descending order."""
    linked_list: Node = Node(10, Node(30, Node(20, None)))
    assert max(linked_list) == 30


def test_max_empty() -> None:
    """Requesting maximum value of empty linked list."""
    with pytest.raises(ValueError):
        max(None)


def test_linkify_empty() -> None:
    """Requesting conversion of empty list to linked list of Nodes."""
    assert linkify([]) is None


def test_linkify_ordered() -> None:
    """Requesting conversion of ordered list of ints to linked list of Nodes."""
    int_list: list[int] = [0, 1, 2, 3]
    assert is_equal(linkify(int_list), Node(0, Node(1, Node(2, Node(3, None)))))


def test_scale_empty() -> None:
    """Requesting scaling of empty list."""
    assert scale(None, 3) is None


def test_scale_ordered() -> None:
    """Requesting scaling of ordered list."""
    linked_list: Node = Node(1, Node(2, Node(3, None)))
    scaled_list: Node = scale(linked_list, 5)
    assert is_equal(scaled_list, Node(5, Node(10, Node(15, None))))