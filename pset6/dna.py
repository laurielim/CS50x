import csv
from sys import argv, exit

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

# Opening the files

database = argv[1]  # CSV file

csvfile = open(database, "r")
data = csv.DictReader(csvfile)
key = data.fieldnames

sequence = argv[2]  # Text file
textfile = open(sequence, "r")
seq = textfile.read()
seqlength = len(seq)

STRcount = {}


def dna():
    """
    Identifies to whom a sequence of DNA belongs.
    Returns a name or 'No Match' if the STR counts do not match exactly with any of the individuals in the CSV file.
    """
    # Compute longest run of consecutive repeats in the DNA sequence for each STR
    for STR in key:
        if STR != "name":
            count = 0
            longest = 0
            STRlength = len(STR)
            i = 0
            # Loops until the end of the string
            while i != (seqlength - 1):
                # Find 1st STR match
                if seq[i:(i + STRlength)] == STR:
                    # Track consecutive repeats
                    while seq[i:(i + STRlength)] == STR:
                        count += 1
                        # Check if end of sequence has been reached
                        if i + STRlength > seqlength:
                            break
                        else:
                            i += STRlength
                    longest = compare(count, longest)
                    count = 0
                
                if i + 1 > seqlength:
                    break
                else:
                    i += 1
            STRcount[STR] = str(longest)
    
        else:
            STRcount[STR] = ""
    
    # Compare STR counts.
    for row in data:
        STRcount["name"] = row["name"]
        if STRcount == row:
            print(STRcount["name"])
            exit(0)
    print("No Match")
    exit(1)


def compare(x, y):
    """
    Takes in 2 integer and returns the greater integer.
    """
    if x > y:
        return x
    else:
        return y

        
dna()
