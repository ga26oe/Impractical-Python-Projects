"""Calculate probability of shared birthday per x number of people"""
import random

max_people = 50
num_runs = 2000

print("\nProbability of at least 2 people having the same birthday:\n")

for people in range(2, max_people + 1):
    found_shared = 0
    for run in range(num_runs):
        bdays = []
        for i in range(0, people):
            bday = random.randrange(0, 364) # ignore leap years
            bdays.append(bday)
        set_of_bdays = set(bdays)
        if len(set_of_bdays) < len(bdays):
            found_shared += 1
    prob = found_shared / num_runs
    print(f"Number people = {people} Prob = {prob}")

print("""
      According to the Birthday paradox, if there are 23 people in a room,
      there's a 50% chance that two of them will share the same birthday.
      """)