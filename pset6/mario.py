while True:
    n = input("Height: ")
    try:
        i = int(n)
        if i > 0 and i < 9:
            break
    except ValueError:
        pass
blocks = 1
spaces = i - 1
while blocks <= i:
    print(" " *  spaces + "#" * blocks + "  " + "#" * blocks)
    blocks += 1
    spaces -= 1
