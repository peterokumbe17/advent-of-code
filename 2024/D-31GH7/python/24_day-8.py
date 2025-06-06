# %% [markdown]
# # Day 8: Resonant Collinearity

# %% [markdown]
# ## Import libraries

# %%
import os
import copy
import itertools
from collections import defaultdict
from math import gcd

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
file_path = os.path.join(current_dir, "../data", "24_day-8_input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read().strip()

# Separate data by line to create rows for grid
grid = file_data.split("\n")

# Separate data in EACH row to represent EACH column
for i in range(len(grid)):
    grid[i] = list(grid[i])

# print(grid)
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%
def get_antinodes_p1(_grid):
    antennas = []
    numRows = len(_grid)
    numCols = len(_grid[0])
    #antinodes = set()
    antinodes_map = defaultdict(list)
    freq_map = defaultdict(list)

    # Store antennas & their respective locations
    for x in range(numRows):
        for y in range(numCols):
            if _grid[x][y] != '.': # If the grid block is NOT empty
                antennas.append((_grid[x][y], x, y)) # E.g. ('A', 4, 2)

    """ Calculate the positions of antinodes """
    # Group antennas by frequency
    for ant_freq, x, y in antennas:
        freq_map[ant_freq].append((x, y)) # E.g. '('A', [(0,1), (2,3), ...])'

    # Calculate antinodes for EACH frequency
    for ant_freq, positions in freq_map.items():
        #print(ant_freq)
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)): # Compare every single antenna (i) against every other antenna of the same frequency (j)
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                # print("Point #1:", (x1, y1))
                # print("Point #2:", (x2, y2))
                
                # Calculate the DISTANCE between antenna point #2 & #1 (same freq.)
                # - NOTE: Removed 'abs' in distance calculations so that the distances between 2 or more points in a straight line can be calculated and matched based on line slopes because antinodes can only exist above and/or below antennas on the SAME line from L to R or R to L
                dx = x2 - x1 # Minus order is IMPORTANT
                dy = y2 - y1
                #print("Distance:", (dx, dy))

                # Traverse through EACH non-empty point in the grid to check if it is an antinode of any 1 of the current 2 antennas with same freq.
                for xn in range(numRows):
                    for yn in range(numCols):
                        # NOTE: Follow the SAME minus order of calculating the SAME difference in distance (+/-x; +/-y) between different points in a line
                        # - E.g. For a striaght diagonal line going upwards from L to R with 4 points (2 antennas & 2 potential antinodes): xn - x2; x2 - x1; x1 - xn
                        # Distance between antenna #1 (top) and current block
                        dx1 = x1 - xn # Minus order is IMPORTANT
                        dy1 = y1 - yn
                        # ----------------
                        # Distance between current block and antenna #2 (bottom)
                        dx2 = xn - x2 # Minus order is IMPORTANT
                        dy2 = yn - y2
                        
                        # IFF the distance between the current point & either of the 2 antennas = the distance between the current 2 antennas (dx1/2 == dx && dy1/2 == dy), then ADD the current non-empty point to the list of antinodes
                        if (dx1 == dx and dy1 == dy):
                            #print("Matched distance #1:", (dx1, dy1))
                            #print("Matched position #1:", (xn, yn))
                            antinodes_map[ant_freq].append((xn, yn))

                        if (dx2 == dx and dy2 == dy):
                            #print("Matched distance #2:", (dx2, dy2))
                            #print("Matched position #2:", (xn, yn))
                            antinodes_map[ant_freq].append((xn, yn))

    # Flatten the dictionary values into a single list
    antinodes = list(itertools.chain(*antinodes_map.values()))

    # Remove duplicate values from the list
    antinodes_no_duplicates = list(set(antinodes))

    return len(antinodes_no_duplicates)
# ====================================================================================================================
# %%
def get_antinodes_p1_alt(_grid):
    antennas = []
    rows = len(_grid)
    if rows == 0:
        return 0
    cols = len(_grid[0])
    
    # Collect all antennas' positions and frequencies
    for i in range(rows):
        for j in range(cols):
            c = _grid[i][j]
            if c != '.':
                antennas.append((i, j, c))
    
    antinodes = set()
    
    # For each pair of antennas with the same frequency
    from collections import defaultdict
    freq_map = defaultdict(list)
    for i, j, c in antennas:
        freq_map[c].append((i, j))
    
    for c in freq_map:
        positions = freq_map[c]
        n = len(positions)
        for i in range(n):
            x1, y1 = positions[i]
            for j in range(i + 1, n):
                x2, y2 = positions[j]
                
                # Calculate the distance between the 2 antennas of same frequency
                dx = x2 - x1
                dy = y2 - y1
                
                # Antinode 1: (x1 - dx, y1 - dy)
                # - NOTE: Since (dx; dy) was calculated as (x2 - x1; y2 - y1), then this means that to find the 1st possible antinode (top or bottom), minus the already calculated distance (dx, dy) between the 2 antennas of same freq. from antenna (x1, y1)
                # - NOTE: [(A2 = (x2 + dx; y2 + dy)) > (D = (x2 - x1; y2 - y1)) > (A1 = (x1 - dx; y1 - dy))]
                ant_x1 = x1 - dx
                ant_y1 = y1 - dy
                if 0 <= ant_x1 < rows and 0 <= ant_y1 < cols:
                    antinodes.add((ant_x1, ant_y1))

                # Antinode 2: (x2 + dx, y2 + dy)
                # - NOTE: Since (dx; dy) was calculated as (x2 - x1; y2 - y1), then this means that to find the 2nd possible antinode (top or bottom), add the already calculated distance (dx, dy) between the 2 antennas of same freq. to antenna (x2, y2)
                # - NOTE: [(A2 = (x2 + dx; y2 + dy)) > (D = (x2 - x1; y2 - y1)) > (A1 = (x1 - dx; y1 - dy))]
                ant_x2 = x2 + dx
                ant_y2 = y2 + dy
                if 0 <= ant_x2 < rows and 0 <= ant_y2 < cols:
                    antinodes.add((ant_x2, ant_y2))
    
    return len(antinodes)
# ====================================================================================================================
# %%
def get_antinodes_p2(grid):
    antennas = []
    rows = len(grid)
    cols = len(grid[0])

    if rows == 0:
        return 0
    
    # Collect all antennas' positions and frequencies
    for i in range(rows):
        for j in range(cols):
            c = grid[i][j]
            if c != '.':
                antennas.append((i, j, c))
    
    antinodes = set()
    
    from collections import defaultdict
    freq_map = defaultdict(list)
    for i, j, c in antennas:
        freq_map[c].append((i, j))
    
    for c in freq_map:
        positions = freq_map[c]
        n = len(positions)
        if n < 2:
            continue
        
        # For EACH position, check if it's in line with any two others (including itself? No)
        # But ANY position that is colinear with two others = an antinode.
        # So for EACH cell in the grid, check if it's colinear with at least two antennas of frequency 'c'.
        
        # But to optimize, we can first collect ALL possible lines defined by pairs of antennas of the same frequency.
        # Then, for EACH line, ALL points on that line = antinodes.
        lines = set()  # To store unique lines represented in a way to avoid duplicates.
        
        # We'll represent a line by the tuple (A, B, C) where Ax + By + C = 0.
        # To avoid duplicates, we'll normalize the representation.
        for i in range(n):
            x1, y1 = positions[i]

            for j in range(i + 1, n):
                x2, y2 = positions[j]

                # Calculate the line equation between (x1,y1) and (x2,y2)
                # - NOTE: Line equation: (y2 - y1)(x - x1) - (x2 - x1)(y - y1) = 0
                # - NOTE: Which can be rewritten as (y1 - y2)x + (x2 - x1)y + (x1*y2 - x2*y1) = 0
                A = y1 - y2
                B = x2 - x1
                C = x1 * y2 - x2 * y1
                
                # Normalize the line equation to avoid duplicate representations
                # Compute the greatest common divisor of A, B, and C
                gcd_val = gcd(gcd(abs(A), abs(B)), abs(C))

                if gcd_val != 0:
                    A //= gcd_val
                    B //= gcd_val
                    C //= gcd_val

                # Also, ensure the first non-zero coefficient is positive
                first_non_zero = 0

                if A != 0:
                    first_non_zero = A
                elif B != 0:
                    first_non_zero = B
                else:
                    first_non_zero = C
                if first_non_zero < 0:
                    A, B, C = -A, -B, -C
                    
                lines.add((A, B, C))
        
        # Now, for each line, mark all points on the line within grid bounds as antinodes
        for (A, B, C) in lines:
            for x in range(rows):
                for y in range(cols):
                    if A * x + B * y + C == 0:
                        antinodes.add((x, y))
    
    return len(antinodes)
# ====================================================================================================================
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
grid_p1 = copy.deepcopy(grid)
numAntinodes = get_antinodes_p1_alt(grid_p1)

print("Number of unique locations within grid with antinodes (PART 1):", numAntinodes)
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).
# - TODO: Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
#====================================================================================================================
# ! Create a deep (independent) copy of the grid data, such that changes made to the copy do not affect the original grid to still test/re-run Part 1 with the correct INITIAL (and not modified) grid
# - NOTE: Not using a deep copy will modify the original grid after running Part 1, therefore no correct output will be calculated anymore
grid_p2 = copy.deepcopy(grid)
numAntinodes = get_antinodes_p2(grid_p2)

print("Number of unique locations within grid with antinodes (PART 2):", numAntinodes)