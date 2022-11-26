"""Tests for linked list utils."""

import pytest
from exercises.ex11.linked_list import Node, last, value_at

__author__ = "730605992"


def test_last_empty() -> None:
    """Last of an empty Linked List should raise a ValueError."""
    with pytest.raises(ValueError):
        last(None)


def test_last_non_empty() -> None:
    """Last of a non-empty list should return its last data value."""
    linked_list = Node(1, Node(2, Node(3, None)))
    assert last(linked_list) == 3


def test_value_at_empty() -> None:
    """Requesting value at index in an empty linked list."""
    with pytest.raises(IndexError):
        value_at(None, 1)


def test_value_at_index_zero() -> None:
    """Requesting value at index 0 in a linked list."""
    linked_list = Node(1, Node(2, Node(3, None)))
    assert value_at(linked_list, 0) == 1


def test_value_at_index_nonzero() -> None:
    """Requesting value at normal index in a linked list."""
    linked_list = Node(1, Node(2, Node(3, None)))
    assert value_at(linked_list, 2) == 3


def test_value_at_index_out_of_bounds() -> None:
    """Requesting value at out of bounds index in a linked list."""
    linked_list = Node(1, Node(2, Node(3, None)))
    with pytest.raises(IndexError):
        value_at(linked_list, 3)