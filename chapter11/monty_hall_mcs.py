import random

def user_prompt(prompt, default=None):
    """User prompted to ent er a number of games or run defailt value."""
    prompt = '{} [{}]: '.format(prompt, default)
    response = input(prompt)
    if not response and default:
        return default # if user presses ENTER without providing input and default value exists, return default value
    else:
        return response  # otherwise return user input

# input number of times to run simulation
num_runs = int(user_prompt("Input number of runs", 20000))

#assign counters for ways to win
first_choice_wins = 0
pick_change_wins = 0
doors = ['a', 'b', 'c']

#run Monte Carlo
for i in range(num_runs):
    winner = random.choice(doors)
    pick = random.choice(doors)

    if pick == winner:
        first_choice_wins += 1
    else:
        pick_change_wins += 1

print(f"Wins with original pick = {first_choice_wins}")
print(f"Wins with changed pick = {pick_change_wins}")
print("Probability of winning with initial guess: {:.2f}".format(first_choice_wins / num_runs))
print("Probability of winning by switching: {:.2f}".format(pick_change_wins / num_runs))

input("\nPress Enter key to exit.")
