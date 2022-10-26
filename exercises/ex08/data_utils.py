"""Dictionary related utility functions."""

__author__ = "930605992"

# Define your functions below
from csv import DictReader


def read_csv_rows(filename: str) -> list[dict[str, str]]:
    """Read the rows of a csv into a 'table'."""
    result: list[dict[str, str]] = []
    
    # Open a handle to the data file
    file_handle = open(filename, "r", encoding="utf8")

    # Prepare to read the data file as a CSV rather than just strings
    csv_reader = DictReader(file_handle)

    # Read each row of the CSV line-by-line
    for row in csv_reader:
        result.append(row)

    # Close the file when we're done, to free its resources.
    file_handle.close()

    return result


def column_values(table: list[dict[str, str]], column: str) -> list[str]:
    """Produce a list[str] of all values in a single column."""
    result: list[str] = []

    for row in table:
        item: str = row[column]
        result.append(item)
    return result


def columnar(row_table: list[dict[str, str]]) -> dict[str, list[str]]:
    """Transform a row-oriented table to a column-oriented table."""
    result: dict[str, list[str]] = {}
    
    first_row: dict[str, str] = row_table[0]
    for column in first_row:
        result[column] = column_values(row_table, column)

    return result


def head(col_table: dict[str, list[str]], rows: int) -> dict[str, list[str]]:
    """Get only the first specified number of rows in a column-based table."""
    result: dict[str, list[str]] = {}

    for col in col_table:
        first_rows: list[str] = []
        if rows > len(col_table[col]):
            rows = len(col_table[col])
        for i in range(0, rows):
            first_rows.append(col_table[col][i])
        result[col] = first_rows
    
    return result


def select(col_table: dict[str, list[str]], subset: list[str]) -> dict[str, list[str]]:
    """Return a subset of a column-based table of only given keys."""
    result: dict[str, list[str]] = {}

    for key in subset:
        result[key] = col_table[key]
    
    return result


def concat(a: dict[str, list[str]], b: dict[str, list[str]]) -> dict[str, list[str]]:
    """Combine 2 [str, list[str]] dictionaries."""
    result: dict[str, list[str]] = {}

    for col in a:
        result[col] = a[col]
    for col in b:
        if col in result:
            result[col] += b[col]
        else:
            result[col] = b[col]
    
    return result


def count(terms: list[str]) -> dict[str, int]:
    """Given a list of strings, returns a dict showing how many times each search term appeared."""
    result: dict[str, int] = {}

    for item in terms:
        if item in result:
            result[item] += 1
        else:
            result[item] = 1

    return result