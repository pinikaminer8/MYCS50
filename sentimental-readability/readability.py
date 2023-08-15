from cs50 import get_string


def main():

    # get input
    text = get_string("Text: ")

    # count letters, words and sentences
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # compute Coleman-Liau index
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = (0.0588 * L) - (0.296 * S) - 15.8
    grade = round(index)

    # Checks whether the score is 16 or higher
    if grade >= 16:
        print("Grade 16+")
    # Checks whether the score is 1 or lower
    elif grade < 1:
        print("Before Grade 1")

    else:
        print("Grade", grade)


# A function that measures the number of letters
def count_letters(text):
    count = 0
    for char in text:
        # checks how many letters
        if char.isalpha():
            count += 1
    return count


# A function that measures the number of words
def count_words(text):
    count = 0
    words = text.split()
    count = len(words)
    return count


# A function that measures the number of sentences
def count_sentences(text):
    count = 0
    for char in text:
        # checks how many dots or exclamation mark or question Mark
        if char in ['.', '!', '?']:
            count += 1
    return count


main()