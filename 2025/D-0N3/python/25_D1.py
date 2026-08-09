# %% [markdown]
# # Day 1: Secret Entrance

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
# - EACH row represents a *turn of the dial.
# - EACH row consists of a letter (L/R) = direction and a number (x) = turns.
# - E.g. "R24" means: turn the dial 24 times to the right (+), and "L3" means: turn the dial 3 times to the left (-).
# =====================================================================================================================
# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "25_D1-input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read().strip()

# Split by each line and store in an array
file_data = file_data.split("\n")
#print(file_data)

file.close()
# ====================================================================================================================

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: You arrive at the secret entrance to the North Pole base ready to start decorating. Unfortunately, the password seems to have been changed.
# - The safe has a dial with only an arrow on it - around the dial are the numbers 0 -> 99 in order. As you turn the dial, it makes a small click noise as it reaches EACH number.
# - EACH line in the input file describes a turn of the dial. 
# - EACH line consists of a direction (L/R) and a number of turns (x).
# - E.g. "R24" means to turn the dial 24 times to the right (+), and "L3" means to turn the dial 3 times to the left (-).
# - NOTE: The dial starts by pointing @ 50.
# - TODO: The actual password = the number of times the dial points at 0 after EACH rotation in the sequence.
# ---------------------------------------------------------------------------------------------------------------------
# ! Create a deep (independent) copy of the data, such that changes made does not affect the original data used to test/re-run Part 1/2 independently.
# - NOTE: Not using a deep copy will modify the original data after running Part 1/2, therefore incorrect output data will be calculated for the other part.
rot_seq = copy.deepcopy(file_data)

arrDirections = [] # int array var to store directions (L/R) 
arrTurns = [] # int array var to store the number of turns
MIN = 0; MAX = 99; START = 50
currPos = START
numZero = 0
# --------------------------------------------------------------------------------------------------------------------
# TODO: Read through EACH value in 'rotation_seq' and split by direction and number of turns, then store in separate arrays
# - Split each line by L/R and number (E.g. "R24" -> ["R", "24"])
for rot in rot_seq:
    direction = rot[0] # 1st character = the direction (L/R)
    turns = rot[1:] # Remaining characters are the number of turns

    arrDirections.append(direction)
    arrTurns.append(int(turns))

# # ! Output the arrays
# for i in range(len(rot_seq)):
#     print("Direction:", arrDirections[i], " || Turns: ", arrTurns[i])

#TODO: Execute the rotations along the dial and count the number of times the dial points at 0 after EACH rotation in the sequence
for i in range(len(rot_seq)):
    if arrDirections[i] == "L": # Negative (-) direction
        for j in range(arrTurns[i]):
            currPos -= 1

            if currPos == -1: # Overflow *below 0, wrap around to 99
                currPos = MAX
    elif arrDirections[i] == "R": # Positive (+) direction
        for j in range(arrTurns[i]):
            currPos += 1
            
            if currPos == 100: # Overflow *above 99, wrap around to 0
                currPos = MIN

    #print(i, arrDirections[i], arrTurns[i], ": Current Position: ", currPos)

    # ! Count the number of times the dial points at 0 after EACH rotation in the sequence
    if currPos == MIN:
        numZero += 1
# --------------------------------------------------------------------------------------------------------------------
# ! Output final result
print("Number of zeros (PART 1): ", numZero)
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: As you're rolling the snowballs for your snowman, you find another security document that must have fallen into the snow: "Due to newer security protocols, please use password method: '0x434C49434B' until further notice."
# - This means that you're actually supposed to count the *number of times ANY click causes the dial to point at 0, regardless of whether it happens DURING a rotation OR at the END of one.
# - TODO: The actual password = the number of times the dial points at 0 *during AND *after EACH rotation in the sequence.
# ---------------------------------------------------------------------------------------------------------------------
# ! Create a deep (independent) copy of the data, such that changes made does not affect the original data used to test/re-run Part 1/2 independently.
# - NOTE: Not using a deep copy will modify the original data after running Part 1/2, therefore incorrect output data will be calculated for the other part.
rot_seq2 = copy.deepcopy(file_data)

arrDirections2 = [] # int array var to store directions (L/R) 
arrTurns2 = [] # int array var to store the number of turns
MIN = 0; MAX = 99; START = 50
currPos = START
numZero = 0
# --------------------------------------------------------------------------------------------------------------------
# TODO: Read through EACH value in 'rotation_seq' and split by direction and number of turns, then store in separate arrays
# - Split each line by L/R and number (E.g. "R24" -> ["R", "24"])
for rot in rot_seq2:
    direction = rot[0] # 1st character = the direction (L/R)
    turns = rot[1:] # Remaining characters are the number of turns

    arrDirections2.append(direction)
    arrTurns2.append(int(turns))

# # ! Output the arrays
# for i in range(len(rot_seq2)):
#     print("Direction:", arrDirections2[i], " || Turns: ", arrTurns2[i])

#TODO: Execute the rotations along the dial and count the number of times the dial points at 0 after & *during EACH rotation in the sequence
for i in range(len(rot_seq2)):
    if arrDirections2[i] == "L": # Negative (-) direction
        for j in range(arrTurns2[i]):
            currPos -= 1

            if currPos == -1: # Overflow *below 0, wrap around to 99
                currPos = MAX

            if currPos == MIN: # Count the number of times the dial points at 0 *during EACH rotation in the sequence
                numZero += 1
    elif arrDirections2[i] == "R": # Positive (+) direction
        for j in range(arrTurns2[i]):
            currPos += 1

            if currPos == 100: # Overflow *above 99, wrap around to 0
                currPos = MIN

            if currPos == MIN: # Count the number of times the dial points at 0 *during EACH rotation in the sequence
                numZero += 1

    #print(i, arrDirections2[i], arrTurns2[i], ": Current Position: ", currPos, numZero)

    # ! Count the number of times the dial points at 0 after EACH rotation in the sequence -> NOTE: not necessary anymore since we are counting the number of times the dial points at 0 *during(j) EACH rotation (NOT after = i) in the sequence
    # if currPos == MIN:
    #     numZero += 1
# --------------------------------------------------------------------------------------------------------------------
# ! Output final result
print("Number of zeros (PART 2): ", numZero)
# ====================================================================================================================

# %%



