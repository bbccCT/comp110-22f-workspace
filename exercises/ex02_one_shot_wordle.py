"""EX02 - A A program like the hit game Wordle, but you get one chance to match the secret word, using concepts learned in the first 2 weeks of COMP 110."""

__author__ = "930605992"

secret: str = "python"
input_str: str
word_valid: bool = False
colored_boxes: str = ""
char_elsewhere: bool = False
alt_check_index: int = 0

WHITE_BOX: str = "\U00002B1C"
GREEN_BOX: str = "\U0001F7E9"
YELLOW_BOX: str = "\U0001F7E8"

#Input Guess
while word_valid == False:
    input_str = input(f"What is your {len(secret)}-letter guess? ")
    if len(input_str) == len(secret):
        word_valid = True
    else:
        print(f"That was not {len(secret)} letters. Try again: ")

i: int = 0
while i < len(secret):
    if input_str[i] == secret[i]:
        colored_boxes = colored_boxes + GREEN_BOX
    else:
        #Check for other instances of the character
        alt_check_index = 0
        char_elsewhere = False
        while (char_elsewhere == False) and (alt_check_index < len(secret)):
            if secret[alt_check_index] == input_str[i]:
                char_elsewhere = True
            else:
                alt_check_index = alt_check_index + 1
        if char_elsewhere == True:
            colored_boxes = colored_boxes + YELLOW_BOX
        else:
            colored_boxes = colored_boxes + WHITE_BOX
    i = i + 1
print(colored_boxes)

if input_str == secret:
    print("Woo! You got it!")
else:
    print("Not quite. Play again soon!")