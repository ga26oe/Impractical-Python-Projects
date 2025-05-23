import sys
from itertools import permutations
from collections import Counter
import load_dictionary


def main():
    """Load files, run filters, allow users to view anagrams by 1st letter"""
    name = "tmvoordle"  # remaining letters "voldemort" from "I am Lord Voldemort"
    name = name.lower()

    word_list_ini = load_dictionary.load("words.txt")
    trigrams_filtered = load_dictionary.load("least_likely_trigrams.txt")

    word_list = prep_words(name, word_list_ini)
    filtered_cv_map = cv_map_words(word_list)
    filter_1 = cv_map_filter(name, filtered_cv_map)
    filter_2 = trigram_filter(filter_1, trigrams_filtered)
    filter_3 = letter_pair_filter(filter_2)
    view_by_letter(name, filter_3)


def prep_words(name, word_list_ini):
    """prep words list for dining anagrams"""
    print("Length of initial word_list= {}".format(len(word_list_ini)))
    len_name = len(name)
    word_list = [word.lower() for word in word_list_ini if len(word) == len_name]
    print("length of new word_list = {}".format(len(word_list)))
    return word_list


def cv_map_words(word_list):
    """Map letters in words to consonants and vowels"""
    vowels = "aeiouy"
    cv_mapped_words = []
    for word in word_list:
        temp = ""
        for letter in word:
            if letter in vowels:
                temp += "v"
            else:
                temp += "c"
        cv_mapped_words.append(temp)

    # determine number of UNIQUE c-v patters
    total = len(set(cv_mapped_words))
    # target fraction to eliminate
    target = 0.05
    n = int(total * target)
    count_pruned = Counter(cv_mapped_words).most_common(total - n)  # remove the least likely by 5 percent
    filtered_cv_map = (set())  # all we need are the final c-v maps, not the frequency counts, which since Counter returns a dictionary we should change it to set
    for pattern, count in count_pruned:
        filtered_cv_map.add(pattern)  # only get the key, not the value (for key, value)
    print("Length filtered_cv_map = {}".format(len(filtered_cv_map)))
    return filtered_cv_map


def cv_map_filter(name, filtered_cv_map):
    """Remove permutations of words based on unlikely consonants-vowel combos"""
    perms = {
        "".join(i) for i in permutations(name)
    }  # generate permuations while removing duplicated due to use of sets
    print("length of initial permutations set ={}".format(len(perms)))
    vowels = "aeiouy"
    filter_1 = set()  # holds contents of first filter
    for candidate in perms:
        temp = ""
        for letter in candidate:
            if letter in vowels:
                temp += "v"
            else:
                temp += "c"
        if temp in filtered_cv_map:
            filter_1.add(candidate)
    print("# choices after filter_1 = {}".format(len(filter_1)))
    return filter_1


def trigram_filter(filter_1, trigrams_filtered):
    """Remove unlikely trigrams from permutations"""
    filtered = set()
    for candidate in filter_1:
        for triplet in trigrams_filtered:
            triplet = triplet.lower()
            if triplet in candidate:
                filtered.add(candidate)
    filter_2 = filter_1 - filtered
    print("# of choices after filter_2 = {}".format(len(filter_2)))
    return filter_2


def letter_pair_filter(filter_2):
    """Remove unlikely letter-pairs from permutations"""
    filtered = set()
    rejects = [
        "dt",
        "lr",
        "md",
        "ml",
        "mr",
        "mt",
        "mv",
        "td",
        "tv",
        "vd",
        "vl",
        "vm",
        "vt",
    ]
    first_pair_rejects = [
        "ld",
        "lm",
        "lt",
        "lv",
        "rd",
        "rl",
        "rm",
        "rt",
        "rv",
        "tl",
        "tm",
    ]

    for candidate in filter_2:
        for r in rejects:
            if r in candidate:
                filtered.add(candidate)
        for fp in first_pair_rejects:
            if candidate.startswith(fp):
                filtered.add(candidate)
    filter_3 = filter_2 - filtered
    print("# of choices after filter_3 = {}".format(len(filter_3)))
    if "voldemort" in filter_3:
        print("Voldemoert found!", file=sys.stderr)
    return filter_3


def view_by_letter(name, filter_3):
    """Filter to anagrams starting with input letter."""
    print("Remaining letters = {}".format(name))
    first = input("select a starting letter or press Enter to see all:")
    subset = []
    for candidate in filter_3:
        if candidate.startswith(first):
            subset.append(candidate)
    print(*sorted(subset), sep="\n")
    print("Number of choices starting with {} = {}".format(first, len(subset)))
    try_again = input("Try again? (Press Enter else any other key to Exit):")
    if try_again.lower() == "":
        view_by_letter(name, filter_3)
    else:
        sys.exit()


if __name__ == "__main__":
    main()
