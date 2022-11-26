"""Utility functions for working with Linked Lists."""

from __future__ import annotations
from typing import Optional

__author__ = "730605992p"


class Node:
    """An item in a singly-linked list."""
    data: int
    next: Optional[Node]

    def __init__(self, data: int, next: Optional[Node]):
        """Construct a singly linked list. Use None for 2nd argument if tail."""
        self.data = data
        self.next = next

    def __str__(self) -> str:
        """Produce a string visualization of the linked list."""
        if self.next is None:
            return f"{self.data} -> None"
        else:
            return f"{self.data} -> {self.next}"


def is_equal(lhs: Optional[Node], rhs: Optional[Node]) -> bool:
    """Test if two linked lists are deeply (values and order) equal to one another."""
    if lhs is None and rhs is None:
        print("1")
        return True
    elif lhs is None or rhs is None or lhs.data != rhs.data:
        print(str(lhs.data) + ", " + str(rhs.data))
        return False
    else:
        return is_equal(lhs.next, rhs.next)


def last(head: Optional[Node]) -> int:
    """Returns the last value of a Linked List, or raises a ValueError if the list is empty."""
    if head is None:
        raise ValueError("last cannot be called with None")
    else:
        if head.next is None:
            return head.data
        else:
            return last(head.next)


def value_at(head: Optional[Node], index: int) -> int:
    """Returns the data value of the Node at a given index in a linked list."""
    if index < 0 or head is None:
        raise IndexError("Index is out of bounds on the list.")
    elif index == 0:
        return head.data
    else:
        return value_at(head.next, index - 1)


def max(head: Optional[Node]) -> int:
    """Returns the maximum data value in a linked list"""
    if head is None:
        raise ValueError("Cannot call max with None")
    if head.next is None:
        return head.data
    elif max(head.next) > head.data:
        return max(head.next)
    else:
        return head.data


def linkify(values: list[int]) -> Optional[Node]:
    """Takes a list of ints and returns a linked list of Nodes with those values."""
    if len(values) > 1:
        return Node(values[0], linkify(values[1:]))
    elif len(values) == 1:
        return Node(values[0], None)
    elif len(values) == 0:
        return None
    

def scale(head: Optional[Node], factor: int) -> Optional[Node]:
    """Takes a linked list of Nodes and scales each Node's value by the given factor."""
    if head is None:
        raise ValueError("scale cannot be called with None")
    else:
        if head.next is None:
            head.data *= factor
            return head
        else:
            return Node(head.data * factor, scale(head.next, factor))