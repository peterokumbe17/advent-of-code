# %% [markdown]
# # Day 2: Red-Nosed Reports

# %% [markdown]
# ## Import data

# %%
# *** [IMPORT DATA] ***
# =====================================================================================================================
import os

# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-2_input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read()

# Split the data read from the file by every new line encountered and store in an array list
file_data = file_data.split('\n')

# print(file_data)
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%
def check_safe_report(arrLevels):
    # ! Check if current report == safe
    # - func 'all':
    #   - Returns a boolean
    #   - Checks if the given param condition holds for all adjacent pairs in an array list

    # Check if the list of level numbers are strictly INCREASING with a difference of at least 1 and at most 3
    validIncrease = all(arrLevels[i] < arrLevels[i + 1] and (1 <= (arrLevels[i + 1] - arrLevels[i]) <= 3) for i in range(len(arrLevels) - 1))
    # Check if the list of level numbers are strictly DECREASING with a difference of at least 1 and at most 3
    validDecrease = all(arrLevels[i] > arrLevels[i + 1] and (1 <= (arrLevels[i] - arrLevels[i + 1]) <= 3) for i in range(len(arrLevels) - 1))

    # Safe report = all level numbers either strictly increasing OR decreasing
    # - Should return 'True': True OR False; False OR True; True OR True
    return validIncrease or validDecrease

# %%
def problem_dampener(arrLevels):
    # Check IF the current report = safe IF it's array list of number levels passes the safe check conditions IFF any 1 number is removed from the list
    for i in range(len(arrLevels)):
        # Remove the i-th element in the array list
        # - '[:x]': Returns a new list of the original list excluding everything AFTER the xth element
        # - '[x:]': Returns a new list of the original list excluding everything BEFORE the xth element
        modifiedArrLevels = arrLevels[:i] + arrLevels[i + 1:]  # Remove the i-th element in the array list
        
        if check_safe_report(modifiedArrLevels) == True:
            return True
    
    return False
# ====================================================================================================================

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: The unusual data (your puzzle input) consists of many reports with levels. The engineers are trying to figure out which reports are safe.
# - EACH line represents a report. 
# - EACH report contains a list of numbers called *levels* that are separated by spaces.
# - The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing.
# - TODO: Count how many reports are considered safe.
#   - A report only counts as safe IFF:
#     - The levels (column numbers) in the report (row) are ALL either increasing or decreasing.
#     - Any 2 adjacent levels (column numbers) differ by at least 1 (NOT = 0) and at most 3 (NOT > 3). 
# ---------------------------------------------------------------------------------------------------------------------
totalSafeReports = 0
arrSafeReportsCheck = []

for report in file_data:
    # Split the report string line of numbers (levels) into a string array list of numbers (levels)
    arrLevels = report.split()
    # Convert each string value in the array into an integer
    arrLevels = [int(num) for num in arrLevels]

    # Check if current report == safe
    isSafeReport = check_safe_report(arrLevels)

    if isSafeReport == True:
        arrSafeReportsCheck.append(True)
    else:
        arrSafeReportsCheck.append(False)

totalSafeReports = arrSafeReportsCheck.count(True)

print("Total safe reports (PART 1):", totalSafeReports)
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the *Problem Dampener*.
# - The Problem Dampener is a reactor-mounted module that lets the reactor safety systems *tolerate a single bad level* in what would otherwise be a safe report.
# - TODO: The same rules apply as before, except if *removing a single level* from an UNSAFE report would make it SAFE, then the report would now count as SAFE.
# ---------------------------------------------------------------------------------------------------------------------
totalSafeReports = 0
arrSafeReportsCheck = []

for report in file_data:
    # Split the report string line of numbers (levels) into a string array list of numbers (levels)
    arrLevels = report.split()
    # Convert each string value in the array into an integer
    arrLevels = [int(num) for num in arrLevels]

    # Check if current report == safe after applying the *Problem Dampener*
    isSafeReport = problem_dampener(arrLevels)

    if isSafeReport == True:
        arrSafeReportsCheck.append(True)
    else:
        arrSafeReportsCheck.append(False)

totalSafeReports = arrSafeReportsCheck.count(True)

print("Total safe reports (PART 2):", totalSafeReports)
