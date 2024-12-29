# %% [markdown]
# # Day 1: Historian Hysteria

# %% [markdown]
# ## Import data

# %%
# *** [IMPORT DATA] ***
# =====================================================================================================================
import re

lColumn = [] # int array var to store list of numbers in left column of text file
rColumn = [] # int array var to store list of numbers in right column of text file

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open("../data/day-1-input.txt", "r")

# ! Read through EACH line in the text file
for line in file:
    line = line.strip()
    # Split each line (by space separation) into two values
    num1, num2 = line.split()
    lColumn.append(int(num1))  # Convert to integers and store in column1
    rColumn.append(int(num2))  # Convert to integers and store in column2

file.close()

# Sort the arrays
lColumn.sort()
rColumn.sort()

# Output the sorted arrays
print("Column 1 (L):", lColumn)
print("Column 2 (R):", rColumn)


# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: Lists of 2 historian groups are NOT similar
# - Maybe the lists are only off by a small amount - to find out, we need to pair up the numbers & measure how far apart they are.
# - TASK: Pair the {1st, 2nd, 3rd, ...} SMALLEST number in the L list with the {1st, 2nd, 3rd, ...} SMALLEST number in the R list.
#   - Within EACH pair, figure out *how far apart* the 2 numbers are from one another.
#     - E.g. If pair #3 (L) with #7 (R), then the distance apart between them = 4 (vice versa).
#   - Then add up all the distances between EACH pair to get the *total distance*.
# ---------------------------------------------------------------------------------------------------------------------
totalDistance = 0 # int var to store the total distance between all pairings
pairDistances = [] # int array var to store the distances between EACH pairing of numbers between the 2 columns
counter = 0

# Calculate distance between each pairings
for lNum in lColumn:
    distance = 0
    rNum = rColumn[counter]

    if lNum < rNum:
        distance = rNum - lNum
    else:
        distance = lNum - rNum
    
    pairDistances.append(distance)

    counter += 1

# Calculate total distance between all pairings
totalDistance = sum(pairDistances)

print(pairDistances)
print("Total distance:", totalDistance)

# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: This time, you'll need to figure out exactly *how often* EACH number from the LEFT list appears in the RIGHT list.
# - Calculate a *total similarity score* by adding up EACH number in the LEFT list after multiplying EACH number by the *number of times* that it appears in the RIGHT list.
# ---------------------------------------------------------------------------------------------------------------------
from collections import Counter

totalSimilarityScore = 0
lColumnSimilarityScores = [] # int array var to store similarity scores of EACH number in the LEFT column

# ! Calculate similarity scores of EACH number in the LEFT column
# Count the number of times that EACH number in the RIGHT column appears in the same RIGHT column
counter = Counter(rColumn)

for num in lColumn:
    # func 'counter.get(x)' returns the number of occurrences of the number 'x'; 0 = default return value
    similarityScore = num * counter.get(num, 0)
    #print(num, '\t', similarityScore)
    lColumnSimilarityScores.append(similarityScore)

totalSimilarityScore = sum(lColumnSimilarityScores)

print(lColumnSimilarityScores)
print(totalSimilarityScore)


