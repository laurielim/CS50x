import csv
from cs50 import SQL
from sys import argv, exit

# Check command-line arguments
if len(argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1)

data = argv[1]

# Open file for SQL
db = SQL("sqlite:///students.db")
# Open csv file
csvfile = open(data, "r")
# Create reader
reader = csv.reader(csvfile)
next(reader)

for row in reader:
    # Parse names
    name = row[0].split()
    if len(name) == 2:
        first = name[0]
        middle = None
        last = name[1]
    elif len(name) == 3:
        first = name[0]
        middle = name[1]
        last = name[2]
    house = row[1]
    birth = row[2]
    # Insert each student into SQL database students.db
    db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", first, middle, last, house, birth)