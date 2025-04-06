import sys
import random
import matplotlib.pyplot as plt # needed to build the bar chart

def read_to_list(file_name):
    """Open a file of data in percent, convert to decimal & return a list.."""
    with open(file_name) as in_file: # opening file with "with" automatically closes it.
        lines = [float(line.strip()) for line in in_file] # listcomp to build contents
        decimal = [round(line / 100, 5) for line in lines] # rounding to 5 places
        return decimal

def default_input(prompt, default=None):
    """Allow use of default values in input."""
    prompt = f'{prompt} [{default}]'
    response = input(prompt)
    if not response and default:
        return default
    else:
        return response

#! load data files with original data in percent form
print("\nNote: Input data should be in percent, not decimal!\n")
try:
    bonds = read_to_list('10-yr_TBond_returns_1926-2013_pct.txt')
    stocks = read_to_list('SP500_returns_1926-2013_pct.txt')
    blend_40_50_10 = read_to_list('S-B-C_blend_1926-2013_pct.txt')
    blend_50_50 = read_to_list('S-B_blend_1926-2013_pct.txt')
    infl_rate = read_to_list('annual_infl_rate_1926-2013_pct.txt')
except IOError as e:
    print(f"{e}. \nTerminating Program.")
    sys.exit(1)

#! get user input; use dictionary for investment-type arguments
# allows user to type simple names, so use dict to map names to list we just loaded
investment_type_args = {'bonds': bonds, 'stocks': stocks, 'sb_blend': blend_50_50,
                        'sbc_blend': blend_40_50_10}

#before asking for input, print legend to aid user
print("     stocks = SP500")
print("      bonds   = 10-yr Treasury Bond")
print("   sb_blend = 50% SP500/50% TBond")
print("  sbc_blend = 40% SP500/50% TBond/10% Cash\n")
print("Press ENTER to take defauly value shown in [brackets]. \n")

#! get user investment choice using default_input()
invest_type = default_input("Enter investment type: (stocks, bonds, sb_blend,"\
    " sbc_blend): \n", 'bonds').lower()
while invest_type not in investment_type_args:
    invest_type = input("Invalid investment type. Enter investment type "\
        "as listed in promt: ")

start_value = default_input("Enter starting value of investments: \n", '200000')
while not start_value.isdigit():
    start_value = input("Invalid input! Input integer only.")

withdrawal = default_input("Input annual pre-tax withdrawal (today's $):", '80000')
while not withdrawal.isdigit():
    withdrawal = input("Invalid input! Input integer only.")

min_years = default_input("Input minimum years in retirement: \n", '18')
while not min_years.isdigit():
    min_years = input("Invalid input! Enter integer only:")

most_likely_years = default_input("Input most-likely years in retirement: \n", '25')
while not most_likely_years.isdigit():
    most_likely_years = input("Invalid input! Enter integer only:") 
    
max_years = default_input("Input maximum years in retirement: \n", '40')
while not max_years.isdigit():
    max_years = input("Invalid input! Enter integer only:")  

num_cases = default_input("Input number of cases to run: \n", '50000')
while not num_cases.isdigit():
    num_cases = input("Invalid input! Input integer only: ")

# check for additional input errors
if not int(min_years) < int(most_likely_years) < int(max_years) \
    or int(max_years) > 99:
        print("\nProblem with input years.")
        print("Required Min < ML < Max with max <=99.", file=sys.stderr)
        sys.exit(1)

#! Monte Carlo Engine
def montecarlo(returns):
    """Run MCS and return investment value at end-of-plan and bankrupt count."""
    case_count = 0 # counter for case being run
    bankrupt_count = 0
    outcome = []
    
    while case_count < int(num_cases):
        investments = int(start_value) # starting investment value that the user specified -- need to \
            # reinitialize each case since investments variable will change constantly
        start_year = random.randrange(0, len(returns)) # pick a value at random from the range of avail. years
        duration = int(random.triangular(int(min_years), int(max_years), int(most_likely_years)))
        end_year = start_year + duration
        lifespan = [i for i in range(start_year, end_year)] # make a list lifespan that captures all \
                                    # the indexes between the starting year and the ending year
        bankrupt = 'no'

        # use two lists to store applicable returns and inflation data for chosen lifespand
        # populate these lists using a for loop that uses each item in lifespan as index and returns
        # inflation lists
        # if lifespan index is out of range compared to other lists, use % operator to wrap indexes
        lifespan_returns = []
        lifespan_infl = []
        for i in lifespan: # use each item in lifespan as index for the returns and inflaiton list
            lifespan_returns.append(returns[i % len(returns)]) # if lifespan index is out of range compared to other list, 
                                                               #use modulo operator to wrap index (list as endless loop)
            lifespan_infl.append(infl_rate[i % len(infl_rate)])
        
        # loop through each year of retirement for each case, increasing/decreasting investment based on returns
        for index, i in enumerate(lifespan_returns): # enumerate produses an index that we will use to get the years avg infl.
            infl = lifespan_infl[index]
            
            # don't adjust for inflation for the first year
            if index == 0:
                withdraw_infl_adj = int(withdrawal)
            else: 
                withdraw_infl_adj = int(withdraw_infl_adj * (1 + infl))
            
            #slowly increase or decrease invesments based on inflationary or deflationary times
            investments -= withdraw_infl_adj
            investments = int(investments * (1 + i))
            
            if investments <= 0:
                bankrupt = 'yes'
                break
            
        if bankrupt == 'yes':
            outcome.append(0)
            bankrupt_count += 1
        else:
            outcome.append(investments)
        case_count += 1
    
    return outcome, bankrupt_count

def bankrupt_prob(outcome, bankrupt_count):
    """Calculate and return chance of running out of money and other stats."""
    total = len(outcome)
    odds = round(100 * bankrupt_count / total, 1)

    print("\nInvestment type: {}".format(invest_type))
    print("Starting Value: ${:,}".format(int(start_value)))
    print("Annual Withdrawal: ${:,}".format(int(withdrawal)))
    print("Years in retirement (min-ml-max): {}-{}-{}".format(min_years, most_likely_years, max_years))
    print("Number of runs: ${:,}\n".format(len(outcome)))
    print("Odds of running out of money: {}%\n".format(odds))
    print("Average outcome: ${:,}".format(int(sum(outcome) / total)))
    print("Minimum outcome: ${:,}".format(min(i for i in outcome)))
    print("Maximum outcome: ${:,}".format(max(i for i in outcome)))
    
    return odds

def main():
    """Call montecarlo() and bankrupt_prob() and draw bar chart of results."""

    outcome, bankrupt_count = montecarlo(investment_type_args[invest_type]) # pass dict name with user input (invest_type) as the key
    odds = bankrupt_prob(outcome, bankrupt_count)
    
    plotdata = outcome[:3000] # only plot first 3000 runs
    
    plt.figure('Outcome by Case (showing first {} runs)'.format(len(plotdata)),
                figsize=(16,5)) # size is width, height in inches
    # use list comprehension to build indexes, starting with 1 for year one, based on length of plotdata
    index = [i + 1 for i in range(len(plotdata))]
    plt.bar(index, plotdata, color='black')
    plt.xlabel('Simulated Lives', fontsize=18)
    plt.ylabel('$ Remaining', fontsize=18)
    plt.ticklabel_format(style='plain', axis='y') # overwrides matplotlib using scientific notation 
    ax = plt.gca() # get the current axis using gca()
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))) # apply Python string-formatting for comma seperators
    plt.title('Probability of running out of money = {}%'.format(odds), fontsize=20, color='red')
    plt.show()
    
if __name__ == '__main__':
    main()

    


    


            

            
        
        

        



    
    