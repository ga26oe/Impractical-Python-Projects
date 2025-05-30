import time
from itertools import product

start_time = time.time()

""" combo = (9, 9, 7, 6, 5, 4, 3) """
combo = (6, 8, 2, 2, 8, 5, 8, 9, 0, 2)

# use Cartesian product to generate permutations with reptition
for perm in product([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], repeat=len(combo)):
    if perm == combo:
        print(f"Cracked! {combo}, {perm}")

end_time = time.time()
print(f"\nRuntime for this program was {end_time - start_time} seconds.")
