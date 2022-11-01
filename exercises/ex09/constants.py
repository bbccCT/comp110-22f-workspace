"""Constants used through the simulation."""

CELL_RADIUS: int = 15
CELL_COUNT: int = 10
CELL_SPEED: float = 5.0

BOUNDS_WIDTH: int = 400
MAX_X: float = BOUNDS_WIDTH / 2
MIN_X: float = -MAX_X
VIEW_WIDTH: int = BOUNDS_WIDTH + CELL_RADIUS * 2

BOUNDS_HEIGHT: int = 400
MAX_Y: float = BOUNDS_HEIGHT / 2
MIN_Y: float = -MAX_Y
VIEW_HEIGHT: int = BOUNDS_HEIGHT + CELL_RADIUS * 2