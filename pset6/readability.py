def readability():
    """
    Asks user for a text and returns the grade level for the text.
    """
    text = input("Test: ")
    
    letters = 0
    words = 1
    sentences = 0
    
    for char in text:
        if char.isalpha():
            letters += 1 
        if char is " ":
            words += 1
        if char in ".!?":
            sentences += 1
            
    avg_letters = per100words(letters, words)
    avg_sentences = per100words(sentences, words)
    index = cl_index(avg_letters, avg_sentences)
    
    if index > 16:
        print("Grade 16+")

    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


def cl_index(L, S):
    """
    L: Average number of letters per 100 words in the text.
    S : Average number of sentences per 100 words in the text.
    Returns a number indicating the Coleman-Liau index.
    """
    return round(0.0588 * L - 0.296 * S - 15.8)

    
def per100words(num, den):
    """
    num = numerator.
    den = denominator.
    Returns average per 100.
    """
    return (num * 100) / den

    
readability()
