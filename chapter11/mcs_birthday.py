"""Use MCS to determine how many poeple is required to be in a room 
so that two people share the same birthday."""

"""Agorithim:

    - 1: Start with empy set of birthdays
    - 2: Keep adding people with random birthdays one by one
    - 3: Before adding each birthday to set, check if its already there
    - 4: If there is a match, record how many were needed and move to next trials
    - 5: After all the trials, analyze data
 
 NOTES:
 - Maybe make each person an object, each having a birthday attribute
 """
from random import randint

num_trials = 10000
results = [] # store results from all trials

class Person(object):
    def __init__(self, number):
        self.number = number
        self.birthday = randint(1, 365)

for i in range(num_trials):
    birthdays = set() # create a new set for each trial
    person = Person(0) # add the first person in the room
    birthdays.add(person.birthday)

    # Track the number of poeple (starting at 1 for first position)
    people_count = 1
    
    sameBirthday = False
    while not sameBirthday:
        people_count += 1
        new_person = Person(people_count)
        if new_person.birthday in birthdays:
            sameBirthday = True
            results.append(people_count) # record the room size
            print(f"Two people have the same birthday! There are {people_count} in the room")
            
        else: # no two birthdays were the same -- add person to room
            birthdays.add(new_person.birthday)

# calculate average room size
average_room_size = sum(results) / len(results)
print(f"Average Room Size: {average_room_size}")
        
    
    


    
