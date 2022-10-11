"""Tests for the sample functions in dictionary.py containing dicts."""

__author__ = "930605992"


from dictionary import invert, favorite_color, count
import pytest


def test_invert_empty() -> None:
    """Tests invert function with empty dictionary input."""
    xs: dict[str, str] = {}
    assert invert(xs) == {}


def test_invert_many_items() -> None:
    """Tests invert function with normal dictionary input with no repeating values."""
    xs: dict[str, str] = dict()
    xs["smile"] = "happy"
    xs["frown"] = "unhappy"
    xs["crying"] = "sad"
    xs["eyes open wide"] = "surprised"
    assert invert(xs) == {
        "happy": "smile",
        "unhappy": "frown",
        "sad": "crying",
        "surprised": "eyes open wide"
    }


def test_invert_many_items_with_duplicate() -> None:
    """Tests invert function with normal dictionary input with a repeating value. Should throw an error."""
    with pytest.raises(KeyError):
        xs: dict[str, str] = dict()
        xs["smile"] = "happy"
        xs["frown"] = "unhappy"
        xs["laughing"] = "happy"
        xs["eyes open wide"] = "surprised"
        invert(xs)


def test_favorite_color_empty() -> None:
    """Tests favorite_color function with empty dictionary input."""
    xs: dict[str, str] = {}
    assert favorite_color(xs) == {}


def test_favorite_color_many_items() -> None:
    """Tests favorite_color function with normal dictionary input with no tie."""
    xs: dict[str, str] = {}
    xs["Kris"] = "blue"
    xs["Marc"] = "yellow"
    xs["Ezri"] = "blue"
    xs["Aristotle"] = "blue"
    xs["Jerry"] = "red"
    xs["David"] = "yellow"
    assert favorite_color(xs) == "blue"


def test_favorite_color_many_items_tie() -> None:
    """Tests favorite_color function with normal dictionary input with a tie."""
    xs: dict[str, str] = {}
    xs["Kris"] = "blue"
    xs["Marc"] = "yellow"
    xs["Ezri"] = "blue"
    xs["Aristotle"] = "blue"
    xs["Jerry"] = "red"
    xs["David"] = "yellow"
    xs["Nova"] = "yellow"
    assert favorite_color(xs) == "blue, yellow"


def test_count_empty() -> None:
    """Tests count function with empty list input."""
    xs: list[str] = []
    assert count(xs) == {}


def test_count_many_items() -> None:
    """Tests count function with normal list input without duplicates."""
    xs: list[str] = ["Aristotle", "Kris", "Susie", "Dani", "Jason", "Jeremy", "Sage", "Kiriko", "Robert"]
    assert count(xs) == {"Aristotle": 1, "Kris": 1, "Susie": 1, "Dani": 1, "Jason": 1, "Jeremy": 1, "Sage": 1, "Kiriko": 1, "Robert": 1}


def test_count_many_items_duplicates() -> None:
    """Tests count function with normal list input with duplicates."""
    xs: list[str] = ["pencil", "pencil", "pen", "pencil", "eraser", "marker", "notebook", "binder", "notebook"]
    assert count(xs) == {"pencil": 3, "pen": 1, "eraser": 1, "marker": 1, "notebook": 2, "binder": 1}