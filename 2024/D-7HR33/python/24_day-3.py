# %% [markdown]
# # Day 3: Mull It Over

# %% [markdown]
# ## Import data

# %%
# *** [IMPORT DATA] ***
# =====================================================================================================================
import os
import re # regex

# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-3_input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
arrFileData = file.read()

#print(arrFileData)
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%
def mul(X,Y):
    return X * Y 
# ====================================================================================================================

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!
# - Goal of the program = to multiply some numbers. It does this with instructions like 'mul(X,Y)', where 'X' and 'Y' are each *1-3 digit numbers*. 
# - E.g. 'mul(44,46)' multiplies 44 by 46 to get a result of 2024. Similarly, 'mul(123,4)' would multiply 123 by 4 = 492.
# - TODO: Scan the corrupted memory for uncorrupted mul instructions.
#   - What do you get if you add up all of the results of the multiplications?
# ---------------------------------------------------------------------------------------------------------------------
# Regular expression to match 'mul(X,Y)'
#regex_mul = r"mul\(\d{1,3},\d{1,3}\)"  # Matches 'mul(' > followed by 1-3 digits > ',' > and 1-3 digits > then ')'
regex_mul = r"mul\((\d{1,3}),(\d{1,3})\)"  # Captures X and Y in 'mul(X,Y)' as groups: E.g. '(X, Y)'
sumResults = 0

# Find all matches in the string
arrMatches = re.findall(regex_mul, arrFileData)

# Call func 'mul(X,Y)' for each match and store the results
arrResults = [mul(int(x), int(y)) for x, y in arrMatches]

sumResults += sum(arrResults)

print("Multiplication result (PART 1):", sumResults)

# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact.
# - If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.
# - TODO: There are two new instructions you'll need to handle:
#   - 'do()': Enables future 'mul()' instructions.
#   - 'don't()': Disables future 'mul()' instructions.
#   - NOTE: Only the most recent 'do()' or 'don't()' instruction applies. At the beginning of the program, all valid 'mul()' instructions are enabled.
# ---------------------------------------------------------------------------------------------------------------------
# Regular expression to match occurrences of ALL 'mul(X,Y)' in a string
regex_mul = r"mul\(\d{1,3},\d{1,3}\)"  # Matches 'mul(' > followed by 1-3 digits > ',' > and 1-3 digits > then ')'
regex_xy_group = r"mul\((\d{1,3}),(\d{1,3})\)"  # Captures X and Y as groups: E.g. '(X, Y)'
regex_controls = r"don't\(\)|do\(\)"  # Matches "don't()" or "do()"
flag = True
pos = 0 # int var to store the index position of the current character of the string
arrMatches = [] # string array var to store all valid captured 'mul(X,Y)' occurrences

# ! Find all matches in the string
# While the end of the string has NOT been reached
while pos < len(arrFileData):
    # Search for the next occurrence of "don't()", "do()", or 'mul(X,Y)'
    match = re.search(f"{regex_controls}|{regex_mul}", arrFileData[pos:])
    
    # IF no matches found, then exit the loop
    if not match:
        break  

    # Get the matched text and its position
    matchedText = match.group()
    # Move the position to after the current match
    pos += match.end() 

    # Update flag based on control patterns
    if matchedText == "don't()":
        flag = False
    elif matchedText == "do()":
        flag = True
    elif (flag == True) and (re.match(regex_mul, matchedText)):
        # Capture 'mul(X,Y)' IFF flag == True
        arrMatches.append(matchedText)

#print(arrMatches)
arrMatches = [re.findall(regex_xy_group, item) for item in arrMatches]

# Call func 'mul(X,Y)' for each match and store the results
arrResults = [mul(int(x), int(y)) for [(x, y)] in arrMatches]

sumResults = sum(arrResults)

print("Multiplication result (PART 2):", sumResults)
# %%



