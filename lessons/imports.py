"""Examples of importing Python."""


from lessons import helpers
from lessons import helpers as hp

from lessons.helpers import powerful, THE_ANSWER

def main() -> None:
    """Entrypoint of program."""
    print(helpers.powerful(2, 4))
    print(f"The answer: {hp.THE_ANSWER}")
    print(powerful(2, 4))
    print(THE_ANSWER)


if __name__ == "__main__":
    main()