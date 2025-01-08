# %% [markdown]
# # Day 7: Bridge Repair

# %% [markdown]
# ## Import libraries

# %%
import os
import copy
from itertools import product

# %% [markdown]
# ## Import data

# %%
# *** [IMPORT DATA] ***
# NOTE: In the given puzzle input:
# - EACH line represents a SINGLE equation.
# - Test values appear BEFORE the colon on EACH line.
# =====================================================================================================================
# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-7_input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read()

# Separate data line by line
file_data = file_data.split("\n")

# For EACH line, separate test values from equations
# - E.g. '190: 10 19' => ['190', '10 19']
for i in range(len(file_data)):
    file_data[i] = file_data[i].split(":")

# For EACH line, separate equation numbers
for i in range(len(file_data)):
    file_data[i][1] = file_data[i][1].strip().split(" ")

# print(file_data)
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%
def evaluate_expression(numbers, operators):
    """Evaluate the expression with the given numbers and operators."""
    result = numbers[0] # First number in list of equation numbers

    for i in range(len(operators)): # E.g. operators = ['+','*','+']
        if operators[i] == "+":
            result += numbers[i + 1]
        elif operators[i] == "*":
            result *= numbers[i + 1]

    return result

# %%
def evaluate_expression_concat(numbers, operators):
    """Evaluate the expression with the given numbers and operators."""
    result = numbers[0] # First number in list of equation numbers

    for i in range(len(operators)): # E.g. operators = ['+','*','||']
        if operators[i] == "+":
            result += numbers[i + 1]
        elif operators[i] == "*":
            result *= numbers[i + 1]
        elif operators[i] == "|":
            concatenatedNum = str(result) + str(numbers[i + 1]) # E.g. '6 * 8 || 6 * 15' = '48||6*15' = '486*15' = 7290
            result = int(concatenatedNum)
            # # Reverse previous calculation (using previous number) - E.g. '3+2*[7||6]': '7||6' needs to become '76' -> INCORRECT because need to build from LEFT to RIGHT (See correct impl. above)
            # if operators[i - 1] == '+': # E.g. '3+2[+7]||6'
            #     result -= numbers[i - 1] # Opposite of '+' = '-': E.g. '3+2[-7]'
            #     concatenatedNum = str(numbers[i - 1]) + str(numbers[i + 1])
            #     result += int(concatenatedNum) # E.g. '3+2[+76]'
            # elif operators[i - 1] == '*': # E.g. '3+2[*7]||6'
            #     result /= numbers[i - 1] # Opposite of '*' = '/': E.g. '3+2[/7]'
            #     concatenatedNum = str(numbers[i - 1]) + str(numbers[i + 1])
            #     result *= int(concatenatedNum) # E.g. '3+2[*76]'

    return result
# ====================================================================================================================

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: Some young elephants were playing nearby and stole all the operators from their calibration equations!
# - TODO: Determine which set of remaining numbers (RHS of colon) can be combined with operators to produce the test value (LHS of colon) and then calculate the total calibration result (sum of test values) of the valid equations.
# - Operators are always evaluated *left-to-right*, NOTE according to *precedence rules*.
# - Numbers in the equations cannot be rearranged.
# - NOTE: Only 2 different types of operators can be used ('+' and/or '*').
# - E.g. '190: 10 19' = True IF '*' is inserted between 10 and 19 to produce 190.
# - E.g. '21037: 9 7 18 13' != True for any combination of inserting '+' or '*' inbetween the numbers.
#  --====================================================================================================================
# ! Create a deep (independent) copy of the data, such that changes made to the copy do not affect the original data to still test/re-run Part 1/2 with the correct INITIAL (and not modified) data
# - NOTE: Not using a deep copy will modify the original data after running Part 1, therefore no correct output will be calculated anymore.
equations = copy.deepcopy(file_data)
arrValidTargets = []

"""Find and print the equations that match the target value."""
for equation in equations:
    # Generate all operator combinations
    target = int(equation[0])
    numbers = equation[1]

    for i in range(len(numbers)):
        numbers[i] = int(numbers[i])

    # 2^n possible combinations
    num_operators = len(numbers) - 1
    operator_combinations = product("+*", repeat=num_operators)
    #print(operator_combinations)

    # Check each operator combination
    for operators in operator_combinations:
        #print(operators)
        if evaluate_expression(numbers, operators) == target:
            arrValidTargets.append(target)
            # NOTE: Since there could be multiple expressions (using the same set of numbers in the CURRENT equation line) that could give the same target result, store ONLY the target of the FIRST equation that gives the correct result, otherwise will end up saving unecessary duplicate target values
            # - E.g. For '3267': Both epressions '81 + 40 * 27' & '81 * 40 + 27' are valid BUT only store the target of the FIRST valid expression, otherwise will store the target twice
            # - Therefore, break out of this loop that checks through each evaluated expression AFTER storing the first valid target
            break
    #print("===========================")

totalCalibrationValue = sum(arrValidTargets)

print("Total calibration result (PART 1):", totalCalibrationValue)
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator = the concatenation operator (||).
# - TODO: Find the total value of the targets of equations that can be made valid with '+' AND '+,*,||' operators.
#====================================================================================================================
# ! Create a deep (independent) copy of the data, such that changes made to the copy do not affect the original data to still test/re-run Part 1/2 with the correct INITIAL (and not modified) data
# - NOTE: Not using a deep copy will modify the original data after running Part 1, therefore no correct output will be calculated anymore.
part2_equations = copy.deepcopy(file_data)
part2_arrValidTargets = []

"""Find and print the equations that match the target value."""
for equation in part2_equations:
    # Generate all operator combinations
    target = int(equation[0])
    numbers = equation[1]

    for i in range(len(numbers)):
        numbers[i] = int(numbers[i])

    # 2^n possible combinations
    num_operators = len(numbers) - 1
    operator_combinations = product("+|*", repeat=num_operators)
    #print(operator_combinations)

    # Check each operator combination
    for operators in operator_combinations:
        #print(operators)
        if evaluate_expression_concat(numbers, operators) == target:
            part2_arrValidTargets.append(target)
            # NOTE: Since there could be multiple expressions (using the same set of numbers in the CURRENT equation line) that could give the same target result, store ONLY the target of the FIRST equation that gives the correct result, otherwise will end up saving unecessary duplicate target values
            # - E.g. For '3267': Both epressions '81 + 40 * 27' & '81 * 40 + 27' are valid BUT only store the target of the FIRST valid expression, otherwise will store the target twice
            # - Therefore, break out of this loop that checks through each evaluated expression AFTER storing the first valid target
            break
    #print("===========================")

part2_totalCalibrationValue = sum(part2_arrValidTargets)

print("Total calibration result (PART 2):", part2_totalCalibrationValue)


