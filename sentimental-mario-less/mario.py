from cs50 import get_int

# Prompt user for height
while True:
    height = get_int("Waht's the height? ")
    if 1 <= height <= 8:
        break

# Make the pyramid
i = k = j = 1
while i <= height:
    while k <= (height - i):
        print(" ", end="")
        k += 1
    while j <= i:
        print("#", end="")
        j += 1
    print()
    i += 1
    j = k = 1