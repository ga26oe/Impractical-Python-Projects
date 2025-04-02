import load_dictionary

def main():
    word_list = load_dictionary.load('words.txt')
    pali_list = []
    for word in word_list:
        if len(word) > 1 and word == word[::-1]:
            pali_list.append(word)
    print("\nNumber of palindromes found = {}n".format(len(pali_list)))
    print(*pali_list, sep='\n') #print elements on a new line * unpacks it -- very elegant

if __name__ == "__main__":
    main()