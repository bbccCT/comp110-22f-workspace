"""An example of a while loop statement."""

counter: int = 0
maximum: int = int(input("Count up to, but not including, what? "))

while(counter < maximum):
    print("The square of " + str(counter) + " is " + str(counter ** 2))
    counter = counter + 1

print("Done!")