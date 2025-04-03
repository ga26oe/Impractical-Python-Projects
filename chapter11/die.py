"""Probabilit that when rolling a die six times you get a different face with each roll"""
from random import randint

trials = 10000
success = 0
for trial in range(trials):
    faces = set()
    for rolls in range(6):
        roll = randint(1, 6)
        faces.add(roll)
    if len(faces) == 6:
        success += 1
print(f"probabilty of success = {success / trial}")