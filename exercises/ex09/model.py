"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from random import random
from exercises.ex09 import constants
from math import sin, cos, pi, sqrt


__author__ = "730605992"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, other: Point) -> float:
        """Checks distance between two points."""
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.
    def tick(self) -> None:
        """Update cell every tick."""
        self.location = self.location.add(self.direction)
        
    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_infected():
            return "red"
        elif self.is_vulnerable():
            return "gray"
        else:
            return "black"

    def contract_disease(self) -> None:
        """Change sickness state to infected."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Returns bool of if this cell is vulnerable."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False
    
    def is_infected(self) -> bool:
        """Returns bool of if this cell is infected."""
        if self.sickness == constants.INFECTED:
            return True
        else:
            return False

    def contact_with(self, other: Cell) -> None:
        """Upon contact with a cell, spread infection if possible."""
        if self.is_vulnerable() and other.is_infected():
            self.contract_disease()
        elif self.is_infected() and other.is_vulnerable():
            other.contract_disease()


class Model:
    """The state of the simulation."""

    population: list[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, infected: int):
        """Initialize the cells with random locations and directions."""
        if infected <= 0 or infected >= cells:
            raise ValueError("Some number of the cells must begin infected, but also not all.")
        self.population = []
        for _ in range(cells):
            start_location: Point = self.random_location()
            start_direction: Point = self.random_direction(speed)
            cell: Cell = Cell(start_location, start_direction)
            self.population.append(cell)
            if infected > 0:
                cell.contract_disease()
                infected -= 1
    
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x: float = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y: float = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle: float = 2.0 * pi * random()
        direction_x: float = cos(random_angle) * speed
        direction_y: float = cos(random_angle) * speed
        return Point(direction_x, direction_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1.0
        elif cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1.0
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1.0
        elif cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1.0

    def check_contacts(self) -> None:
        """Check whether any cells come in contact with each other."""
        i: int = 0
        while i < len(self.population):
            for cell_num in range(i + 1, len(self.population)):
                if self.population[i].location.distance(self.population[cell_num].location) < constants.CELL_RADIUS:
                    self.population[i].contact_with(self.population[cell_num])
            i += 1

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        return False