"""EX01 - A program related to the hit game Wordle using concepts learned in the first week on COMP 110."""

__author__ = "930605992"

input_word: str = input("Enter a 5-character word: ")
input_char: str = input("Enter a single character to search for in the word: ")
word_valid: bool = False
char_valid: bool = False
num_matches: int = 0

if len(input_word) == 5:
    word_valid = True
else:
    print("ERROR: Word must be *5* characters in length.")
    quit()

if len(input_char) == 1:
    char_valid = True
else:
    print("ERROR: Character must be a *SINGLE* character.")
    quit()

print("Searching for " + input_char + " in " + input_word)

index: int = 0
while index < len(input_word):
    if input_word[index] == input_char:
        print(input_char + " found at index " + str(index))
        num_matches += 1
    index += 1

if num_matches == 0:
    print("No instances of " + input_char + " found in " + input_word)
elif num_matches == 1:
    print(str(num_matches) + " instance of " + input_char + " found in " + input_word)
else:
    print(str(num_matches) + " instances of " + input_char + " found in " + input_word)
