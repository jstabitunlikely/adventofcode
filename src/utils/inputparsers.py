# Parsers for the most common puzzle input formats

from typing import Callable


# REVISIT: how to type hint a dinamically changing type
def parse_matrix2d(data: str,
                   type: Callable = int) -> list[list]:
    """
    Parses a string representation of a 2D matrix and converts it into a nested list of values.

    Args:
        data: A string representing the 2D matrix. Each row in the matrix should be
              separated by whitespace (e.g., spaces, tabs, newlines).
        type: An optional callable (e.g., int, float, str) that specifies the
              desired data type for the matrix elements. Defaults to int.

    Returns:
        A nested list representing the 2D matrix, where each inner list corresponds
        to a row in the matrix, and each element within the inner lists is of the
        specified type.
    """
    matrix = [list(line) for line in data.split()]
    matrix = [list(map(type, line)) for line in matrix]
    return matrix
