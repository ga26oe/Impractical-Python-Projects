import time
from random import randint, randrange

def fitness(combo, attempt):
    """Compare items in two lists and count number of matches."""
    grade = 0
    for i, j in zip(combo, attempt):
        if i == j:
            grade += 1
    return grade # don't record the index, just that the function has found a match, to emulate output from sound detection device

def main():
    """Use hill-climbing algorithm to solve lock combination"""
    combination = '6822858902' # 
    print(f"Combination = {combination}")
    # convert combination to list:
    combo = [int(i) for i in combination]

    # generate guess & grade fitness:
    best_attempt = [0] * len(combo) # generates a list of 0s equal in length to combination
    best_attempt_grade = fitness(combo, best_attempt)

    count = 0 # count how many attempts to crack the code
    
    # evolve guess
    while best_attempt != combo:
        # crossover 
        next_try = best_attempt[:] # a copy of the best attempt variable
        
        #mutate
        lock_wheel = randrange(0, len(combo)) # each digit in combo turns a lock wheel
        next_try[lock_wheel] = randint(0,9) # randomly set lock wheel equal to an index location in combination -- this represents location of the single element to change in this iteration

        #grade and select
        next_try_grade = fitness(combo, next_try)
        if next_try_grade > best_attempt_grade:
            best_attempt = next_try[:]
            best_attempt_grade = next_try_grade
        print(next_try, best_attempt)
        count += 1

    print()
    print("Cracked! {}".format(best_attempt), end=' ')
    print("in {} tries!".format(count))

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print("\nRuntime for this program was {:.5f} seconds.".format(duration))
