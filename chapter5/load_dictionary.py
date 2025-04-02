'''Load a text file as a list.
    Arguments:
    - Text file name (and directory path, if needed)
    Exceptions:
    - IOError if filename is not fond
    Returns:
    - List of all words in a text file in lowercase
'''
import sys

def load(file):
    '''Open a text file and return a list of lowercase strings'''
    try:
        with open(file) as in_file:
            loaded_txt = in_file.read().strip().split('\n')
            loaded_txt = [x.lower() for x in loaded_txt]
            return loaded_txt
    except IOError as e:
        print("{}\nError opening {}. Terminating program.".format(e, file), file=sys.stderr)
    sys.exit(1)
