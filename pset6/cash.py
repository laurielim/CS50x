from cs50 import get_float 

while True:
    dollars = get_float("Change owed: ")
    if dollars >= 0:
        break
coins = round(dollars * 100)
total = 0

while coins > 24:
    total += 1
    coins -= 25

while coins > 9:
    total += 1
    coins -= 10

while coins > 4:
    total += 1
    coins -= 5

while coins > 0:
    total += 1
    coins -= 1
    
print(total)

