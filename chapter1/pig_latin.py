'''Input a word then turn it into pig latin'''
def main():
    '''Convert a word to Pig Latin.'''
    vowels = "aeiou"
    while True:
        word = input("Enter a word to convert to Pig Latin (or 'exit' to quit\n")
        if word.lower() == 'exit':
            break
        first_letter = word[0]
        if first_letter in vowels:
            pig_latin = word + "yay"
        else:  
            pig_latin = word[1:] + first_letter + "ay" # remove first letter from word + add first letter + add ay
        print(f"The Pig Latin version of '{word}' is '{pig_latin}'")
        

if __name__ == "__main__":
    main()