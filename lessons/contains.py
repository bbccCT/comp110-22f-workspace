"""An example of a list utility algorithm."""

# Name: contains
# Function with 2 parameters:
#  needle = what we're searching for
#  haystack - what we're searching through
# Return Type: bool
def contains(needle: str, haystack: list[str]) -> bool:
    # Start from first index
    i: int = 0
    # Loop through each index of list
    while i < len(haystack):
    #   Test if equal to needle
        if haystack[i] == needle:
    #       Yes! Return True
            return True
        i += 1
    # Return False
    return False