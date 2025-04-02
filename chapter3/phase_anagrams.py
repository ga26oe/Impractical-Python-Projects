import sys
from collections import Counter
import load_dictionary

dict_file = load_dictionary.load('words.txt')
dict_file.append('a')
dict_file.append('i') # Some dict files omit a and I
dict_file = sorted(dict_file)

init_name = input("Enter a name: ")

def find_anagrams(name, word_list):
    '''Read name and dict files and display all anagrams in name'''
    name_letter_map = Counter(name)
    anagrams = []
    for word in word_list:
        test = '' #7: accumulate all variables in word that "fit" in name
        word_letter_map = Counter(word.lower()) #8: counter for the current word
        for letter in word: #9: check that the count of each letter is the same or less than the count in name
            if word_letter_map[letter] <= name_letter_map[letter]:
                test +=letter
        if Counter(test) == word_letter_map:
            anagrams.append(word)
    print(*anagrams, sep='\n')
    print()
    print("Remaining letters = {}".format(name))
    print("Number of remaining letters = {}".format(len(name)))
    print("Number of remaining (real world) anagrams = {}".format(len(anagrams)))

def process_choice(name):
    '''Check user choice for validity, return choice and leftover letters'''
    while True:
        choice = input('\nMake a choice else Enter to start over or # to end:') #2: 
        if choice == '':
            main()
        elif choice == '#':
            sys.exit()
        else:
            candidate = ''.join(choice.lower().split()) #3: remove whitespace and convert to lowercase
        left_over_list = list(name) #4: build a list from the name variable
        for letter in candidate:    #5: loop to subtract the letters used in candidate
            if letter in left_over_list:
                left_over_list.remove(letter) # if a chosen letter is present, it is removed
        if len(name) - len(left_over_list) == len(candidate): #6: if users enters a word that isn't displayed in the list, or entered mulitple wods, a letter may not be present
            break # subtracts left over letters from name -- if result is number of letters in candinate, the input is valid and break out of while loop
        else:
            print("Won't work! Make another choice!", file=sys.stderr)
    name = ''.join(left_over_list) #7: if all user choice letters pass, the list of leftovers is converted back to string and used to update variable
    return choice, name

def main():
    '''Help user build anagram phrase from their name'''
    name = ''.join(init_name.lower().split())
    name = name.replace('-', '')
    limit = len(name)
    phrase = ''
    running = True
    
    while running:
        temp_phrase = phrase.replace(' ', '') # prepare string, strip it of whitespace
        if len(temp_phrase) < limit:
            print("Length of anagram phrase = {}".format(len(temp_phrase)))
            
            find_anagrams(name, dict_file)
            print("Current anagram phrase -", end=" ")
            print(phrase, file=sys.stderr)
            
            choice, name = process_choice(name)
            phrase += choice + ' '
        
        elif len(temp_phrase) == limit:
            print("\n*****FINISHED!!!*****\n")
            print("Anagram of name =", end=" ")
            print(phrase, file=sys.stderr)
            print()
            
            try_again = input('\nTry again? (Press Enter else "n" to quit)\n' )
            if try_again.lower() == 'n':
                running = False
                sys.exit()
            else: 
                main()

if __name__ == '__main__':
    main()