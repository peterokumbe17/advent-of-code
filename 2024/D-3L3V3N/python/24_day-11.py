# %% [markdown]
# # Day 11: Plutonian Pebbles

# %% [markdown]
# ## Import libraries

# %%
import os
import copy

# %% [markdown]
# ## Import data

# %%
# *** [IMPORT DATA] ***
# NOTE: In the given puzzle input:
# - A string list of stones (represented by numbers) in a straight line.
# =====================================================================================================================
# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-11_input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read().strip()

file_data = file_data.split(" ")

print(file_data)
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%
def change_numbers(numbers):
    """
    Process a list of string numbers according to the following rules:
    1. If the value is '0', replace it with '1'.
    2. If the value has an even number of digits, split it into two numbers.
    3. If the value does not meet the above conditions, multiply it by 2024.

    Args:
    - numbers (list): A list of string numbers.

    Returns:
    - list: The processed list of numbers.
    """
    arrChangedNumbers = []

    for num in numbers:
        # Rule 1: Replace '0' with '1'
        if num == '0':
            arrChangedNumbers.append('1')
        else:
            # Rule 2: Split even-length numbers into two
            if len(num) % 2 == 0:
                half = len(num) // 2
                num1, num2 = num[:half], num[half:]
                # Remove leading zeros
                num1, num2 = num1.lstrip('0') or '0', num2.lstrip('0') or '0'
                arrChangedNumbers.extend([num1, num2])
            else:
                # Rule 3: Multiply by 2024
                arrChangedNumbers.append(str(int(num) * 2024))
    
    return arrChangedNumbers
# =====================================================================================================================

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: The ancient civilization on Pluto was known for its ability to manipulate spacetime, and while The Historians explore their infinite corridors, you've noticed a strange set of physics-defying stones. At first glance, they seem like normal stones: they're arranged in a perfectly *straight line*, and EACH stone has a *number* engraved on it. The strange part is that every time you BLINK, the stones CHANGE:
# - If the stone is engraved with the number '0', it is replaced by a stone engraved with the number '1'.
# - If the stone is engraved with a number that has an EVEN number of *digits*, it is REPLCAED by TWO stones. The LEFT half of the CURRENT stone's digits are engraved on the new left stone, and the RIGHT half of the digits are engraved on the new right stone. (NOTE: The new numbers don't keep extra leading zeroes: E.g. '1000' would become stones '10'(L) and '0'(R).)
# - If none of the above rules apply, then the stone is REPLACED by a new stone = the old stone's number * 2024.
# - NOTE: No matter how the stones CHANGE, their order is PRESERVED, and they stay on their perfectly straight line.
# ! TODO: Consider the arrangement of stones in front of you (puzzle input). How many stones will you have after blinking 25 times?
# ====================================================================================================================
# ! Create a deep (independent) copy of the data, such that changes made to the copy do not affect the original data to still test/re-run Part 1/2 with the correct INITIAL (and not modified) data
# - NOTE: Not using a deep copy will modify the original data after running Part 1/2, therefore no correct output will be calculated anymore.
stones = copy.deepcopy(file_data)
blink = 25

# Change stones every time you blink
for i in range(blink):
    stones = change_numbers(stones)

# Calculate the number of stones after x blinks
sumStones = len(stones)

# print(stones)

print("Total number of stones after 25 blinks (PART 1):", sumStones)
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: Same as Part 1.
# ! TODO: Consider the arrangement of stones in front of you (puzzle input). How many stones will you have after blinking 75 times?
#====================================================================================================================
# ! Create a deep (independent) copy of the data, such that changes made to the copy do not affect the original data to still test/re-run Part 1/2 with the correct INITIAL (and not modified) data
# - NOTE: Not using a deep copy will modify the original data after running Part 1/2, therefore no correct output will be calculated anymore.
stones = copy.deepcopy(file_data)
blink = 75

# Change stones every time you blink
for i in range(blink):
    stones = change_numbers(stones)

# Calculate the number of stones after x blinks
sumStones = len(stones)

# print(stones)

print("Total number of stones after 75 blinks (PART 2):", sumStones)

# %%



