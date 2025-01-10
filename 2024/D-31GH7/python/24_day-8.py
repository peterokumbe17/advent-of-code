# %% [markdown]
# # Day 8: Resonant Collinearity

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
# - The grid map represents antennas.
# - EACH antenna is represented by a *letter* or *digit*.
# - The FREQUENCY of EACH antenna is different, based on whether the antenna is a: lowercase letter, uppercase letter or digit.
# - '#': Represents an antinode. 
# =====================================================================================================================
# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-7_input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read()

# Read all the data in the file
file_data = file.read().strip()

# Separate data by line to create rows for grid
grid = file_data.split("\n")

# Separate data in EACH row to represent EACH column
for i in range(len(grid)):
    grid[i] = list(grid[i])

print(grid)
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%


# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas.
# - In particular, an *antinode* occurs at *any point* that is perfectly *in line* with TWO antennas of the SAME frequency - but ONLY when ONE of the antennas is TWICE as far away as the other. This means that for any PAIR of antennas with the SAME frequency, there are TWO antinodes, one on EITHER side of them.
# - Antennas with DIFFERENT frequencies DO NOT create antinodes; however, antinodes CAN occur at the SAME locations that CONTAIN antennas.
# - TODO: Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?
# ====================================================================================================================
# ! Create a deep (independent) copy of the grid data, such that changes made to the copy do not affect the original grid to still test/re-run Part 1 with the correct INITIAL (and not modified) grid
# - NOTE: Not using a deep copy will modify the original grid after running Part 1, therefore no correct output will be calculated anymore
part1_grid = copy.deepcopy(grid)


# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: xxx
# - TODO: xxx
#====================================================================================================================
# ! Create a deep (independent) copy of the grid data, such that changes made to the copy do not affect the original grid to still test/re-run Part 1 with the correct INITIAL (and not modified) grid
# - NOTE: Not using a deep copy will modify the original grid after running Part 1, therefore no correct output will be calculated anymore
part2_grid = copy.deepcopy(grid)


# %%



