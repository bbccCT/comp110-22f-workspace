"""EX03 - A program replicating the hit game Wordle using python basics."""

__author__ = "930605992"


def main() -> None:
    """The entrypoint of the program and main game loop."""
    secret: str = "codes"

    turn: int = 1
    turns: int = 6

    guess: str = ""

    while turn <= turns:
        print(f"=== Turn {turn}/{turns} ===")
        guess = input_guess(len(secret))
        print(emojified(guess, secret))
        if guess == secret:
            print(f"You won in {turn}/{turns} turns!")
            return
        else:
            turn += 1
    print(f"X/{turns} - Sorry, try again tomorrow!")


def input_guess(expected_length: int) -> str:
    """Allows the user to make a guess."""
    in_guess: str = input(f"Enter a {expected_length} character word: ")
    while len(in_guess) != expected_length:
        in_guess = input(f"That wasn't {expected_length} chars! Try again: ")
    return in_guess


def emojified(this_guess: str, secret_word: str) -> str:
    """Checks the status of each character in the guess and returns emoji squares with colors depending on the status of the characters."""
    assert len(this_guess) == len(secret_word)
    WHITE_BOX: str = "\U00002B1C"
    GREEN_BOX: str = "\U0001F7E9"
    YELLOW_BOX: str = "\U0001F7E8"
    colored_boxes: str = ""
    i: int = 0
    while i < len(this_guess):
        if this_guess[i] == secret_word[i]:
            colored_boxes += GREEN_BOX
        elif contains_char(secret_word, this_guess[i]):
            colored_boxes += YELLOW_BOX
        else:
            colored_boxes += WHITE_BOX
        i += 1
    return colored_boxes


def contains_char(secret_word: str, guess_char: str) -> bool:
    """Checks to see if a guessed character is contained within the first word."""
    assert len(guess_char) == 1
    alt_check_index: int = 0
    while alt_check_index < len(secret_word):
        if secret_word[alt_check_index] == guess_char:
            return True
        alt_check_index += 1
    return False


if __name__ == "__main__":
    main()