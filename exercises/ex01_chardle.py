"""EX01 - A program related to the hit game Wordle using concepts learned in the first week on COMP 110"""

__author__ = "930605992"

input_word: str = "hello"
input_char: chr = "A"
input_raw_str: str = "hello"
word_valid: bool = False
char_valid: bool = False
num_matches: int = 0

while word_valid == False:
    input_raw_str = input("Enter a 5-character word: ")
    if len(input_raw_str) == 5:
        input_word = input_raw_str
        word_valid = True
    else:
        print("Please enter something that is *5* characters in length.")

while char_valid == False:
    input_raw_str = input("Enter a single character to search for in the word: ")
    if len(input_raw_str) == 1:
        input_char = input_raw_str
        char_valid = True
    else:
        print("Please enter a *SINGLE* character.")

print("Searching for '" + input_char + "' in \"" + input_word + "\"")

for index in input_word:
    if index == input_char:
        print(input_char + " was found at index " + index)
        num_matches += 1

if num_matches == 0:
    print("No instances of '" + input_char + "' found in \"" + input_word + "\"")
else:
    print(num_matches + " instances of '" + input_char + "' found in \"" + input_word + "\"")
