from cs50 import SQL
from sys import argv, exit

# Check command-line arguments
if len(argv) != 2:
    print("Usage: python roster.py [House]")
    exit(1)

house = argv[1]

# Query database for all students in house
db = SQL("sqlite:///students.db")
students = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

for student in students:
    first = student['first']
    middle = student['middle']
    last = student['last']
    birth = student['birth']
    if middle == None:
        print(f"{first} {last}, born {birth}")
    else:
        print(f"{first} {middle} {last}, born {birth}")