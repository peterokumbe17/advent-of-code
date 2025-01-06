# %% [markdown]
# # Day 5: Print Queue

# %% [markdown]
# ## Import libraries

# %%
import os
from itertools import permutations
# from concurrent.futures import ProcessPoolExecutor

# %% [markdown]
# ## Import data

# %%
# *** [IMPORT DATA] ***
# NOTE: In the given puzzle input:
# - The *first section* specifies the *page ordering rules* (one per line).
# - The notation 'X|Y' means that if BOTH page number 'X' and page number 'Y' are to be produced as part of an *update*, then page number 'X' must be printed at ANY point BEFORE page number 'Y'.
# - E.g. The first rule ('47|53'), means that IF an *update* includes BOTH page number '47' AND page number '53', then page number '47' must be printed at ANY point BEFORE page number '53'. (47 doesn't necessarily need to be IMMEDIATELY before 53; other pages are allowed to be between them.)
# - The *second section* (separated from the first part by an empty line) specifies the *page numbers (separated by ',') of each update (one per line)*. Because most safety manuals are different, the pages needed in the updates are different too.
# =====================================================================================================================
# ! Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-5_input-test.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read().strip()

# Split the data read from the file by the empty line encountered and store in an array list
file_data = file_data.split('\n\n')

rules = file_data[0].split("\n")

for i in range (len(rules)):
    rules[i] = rules[i].split("|")

updates = file_data[1].split("\n")

for j in range(len(updates)):
    updates[j] = updates[j].split(",")

print(rules)
# print(len(rules))
print(updates)
# print(len(updates))
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%
def is_correct_update(rules, update):
    arrCheckUpdates = []
    
    for rule in rules:
        leftPN = rule[0]
        rightPN = rule[1]

        # Check IF the left page number (PN) of the CURRENT rule exists in the CURRENT update
        if leftPN in update:
            leftPN_idx = update.index(leftPN)
        else:
            leftPN_idx = -1 # Not found

        if rightPN in update:
            rightPN_idx = update.index(rightPN)
        else:
            rightPN_idx = -1 # Not found

        # Check IF the LHS page number comes BEFORE the RHS page number in the CURRENT update
        if leftPN_idx == -1 or rightPN_idx == -1:
            arrCheckUpdates.append(True)
        else:
            if leftPN_idx < rightPN_idx:
                arrCheckUpdates.append(True)
        
            if leftPN_idx > rightPN_idx:
                arrCheckUpdates.append(False)
    
    # Check IF ALL rule checks pass for the list of page numbers in the CURRENT update
    if False not in arrCheckUpdates:
        return True

    return False

# %%
def is_incorrect_update(rules, update):
    arrCheckUpdates = []
    
    for rule in rules:
        leftPN = rule[0]
        rightPN = rule[1]

        # Check IF the left page number (PN) of the CURRENT rule exists in the CURRENT update
        if leftPN in update:
            leftPN_idx = update.index(leftPN)
        else:
            leftPN_idx = -1 # Not found

        if rightPN in update:
            rightPN_idx = update.index(rightPN)
        else:
            rightPN_idx = -1 # Not found

        # Check IF the LHS page number comes BEFORE the RHS page number in the CURRENT update
        if leftPN_idx == -1 or rightPN_idx == -1:
            arrCheckUpdates.append(True)
        else:
            if leftPN_idx < rightPN_idx:
                arrCheckUpdates.append(True)
        
            if leftPN_idx > rightPN_idx:
                arrCheckUpdates.append(False)
    
    # ! Get list of INCORRECT updates
    # - NOTE: Check IF NOT all rule checks pass for the list of page numbers in the CURRENT update
    if False in arrCheckUpdates:
        return True

    return False

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services. Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order.
# - The Elf has given you both the page ordering rules and the pages to produce in EACH *update* (your puzzle input), but can't figure out whether each update has the pages in the right order.
# - TODO: Determine which updates are already in the correct order. What do you get if you add up all the middle page numbers from all the correctly-ordered updates?
#   - E.g. The first update ('75,47,61,53,29'), means that the update consists of page numbers 75, 47, 61, 53, and 29.
# - NOTE: In the above example, the first update (75,47,61,53,29) is in the right order for the following reasons:
#   - 75 is correctly [first] because there are rules that put each other page AFTER it: (75|47), (75|61), (75|53), and (75|29).
#   - 47 is correctly [second] because 75 must be BEFORE it (75|47) AND every other page must be AFTER it according to 47|61, 47|53, and 47|29.
#   - 61 is correctly in the [middle] because 75 and 47 are BEFORE it (75|61 and 47|61) AND 53 and 29 are AFTER it (61|53 and 61|29).
#   - 53 is correctly [fourth] because it is BEFORE page number 29 (53|29).
#   - 29 is the only page left and so is correctly [last].
# ====================================================================================================================
arrValidUpdates = []
sumMiddlePNs = 0

for update in updates:
    #print(update, is_correct_update(rules, update))
    if is_correct_update(rules, update) == True:
        arrValidUpdates.append(update)

# Get sum of all middle page numbers in the list of valid updates
for update in arrValidUpdates:
    middlePN_idx = len(update) // 2
    middlePN = update[middlePN_idx]

    sumMiddlePNs += int(middlePN)

print("Sum of all correct middle page numbers (PART 1):", sumMiddlePNs)
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.
# - TODO: For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order.
#   - E.g. '75,97,47,61,53' becomes '[97,75],47,61,53'
#====================================================================================================================
arrInvalidUpdates = []
arrValidUpdates = []
sumMiddlePNs = 0

for update in updates:
    if is_incorrect_update(rules, update) == True:
        arrInvalidUpdates.append(update)
    
# ! Correctly order the invalid updates
for update in arrInvalidUpdates:
    #print(update)
    #print("-----------------------------")

    # """Check if the condition can be met by any permutation of the array."""
    # # Generate permutations lazily
    all_perms = permutations(update)
    # #print(all_perms)

    for perm in all_perms:
        if is_correct_update(rules, perm) == True:
            # func 'list(tuple)'
            # - Convert tuple back to list
            validUpdate = list(perm)
            #print(validUpdate)
            arrValidUpdates.append(validUpdate)

    #print("=============================")

#print(arrValidUpdates)

# TODO: Get sum of all middle page numbers in the new list of correctly ordered & now valid updates
for update in arrValidUpdates:
    middlePN_idx = len(update) // 2
    middlePN = update[middlePN_idx]

    sumMiddlePNs += int(middlePN)

print("Sum of all correct middle page numbers (PART 2):", sumMiddlePNs)

# %%



