import sys
from string import punctuation
import json
from nltk.corpus import cmudict

# load dictionary of words in haiku corpus but not in cmudict
with open('missing_words.json') as f:
    missing_words = json.load(f)

cmudict = cmudict.dict()

def count_syllables(words):
    """Use corpora to count syllables in English word or phrase."""
    # prep words for cmudict corpus
    words = words.replace('-', ' ')
    words = words.lower().split()
    num_sylls = 0
    for word in words:
        word = word.strip(punctuation)
        if word.endswith("'s") or word.endswith("‘s"):
            word = word[:-2]
        if word in missing_words:
            num_sylls += missing_words[word]
        else:
            for phonemes in cmudict[word][0]: # use first value in case there is multiple pronounciations
                for phoneme in phonemes:
                    if phonemes[-1].isdigit():
                        num_sylls += 1
                        
def main():
    while True:
        print("Syllable Counter")
        word = input("Enter a word or phrase; else press Enter to Exit: ")
        if word == '': # program exits if user presses Enter
            sys.exit()
        try:
            num_syllables = count_syllables(word)
            print(f"number of syllabes in {word} is: {num_syllables}")
            print()
        except KeyError:  # need try and catch so program doesn't crash when word isn't found
            print("Word not found. Try again.\n", file=sys.stderr)

if __name__ == '__main__':
    main()
    