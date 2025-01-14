# %% [markdown]
# # Day 10: Hoof It

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
# - Input represents a topographical map of a surrounding area.
# - The TM indicates the height at EACH position, using a scale from 0 (lowest) -> 9 (highest).
# =====================================================================================================================
# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-10_input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read().strip()

# file_data = file_data.split("\n")

# print(file_data)
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%
def find_paths(grid, trailheadPos):
    """
    Find all *distinct* successful paths from a given trailhead (0) position in the grid.
    NOTE: This function will return distinct paths that can reach all reachable 9s.
    - Grid positions can be revisited in different paths, as long as each path has at least 1 different grid position in the path than other found paths
    - This function does NOT return a list of the *first* distinct paths that can reach all reachable 9s. It returns ALL distinct paths that can reach all reachable 9s.
    - E.g. If a path 'path_1' reaches '9_1' and another distinct 'path_2' also reaches the same '9_1', then this function will return both 'path_1' and 'path_2' as distinct paths. BUT for the purpose of this challenge, we only need to count the *first* path that can reach a specific '9'.

    Args:
    - grid (list of lists): A 2D grid of integers.
    - trailheadPos (tuple): The row and column indices of the trailhead.

    Returns:
    - list of lists: A list of successful paths, where each path is a list of tuples representing the row and column indices of the path.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    visited = set()

    # Depth-first search
    def dfs(row, col, path):
        if (row, col) in visited:
            return
        
        visited.add((row, col))
        path.append((row, col))

        if grid[row][col] == 9:
            paths.append(path[:])
        else:
            for dr, dc in directions:
                nr, nc = row + dr, col + dc

                if (0 <= nr < rows) and (0 <= nc < cols) and (grid[nr][nc] == grid[row][col] + 1):
                    dfs(nr, nc, path)
                    
        visited.remove((row, col))
        path.pop()

    paths = []
    
    dfs(trailheadPos[0], trailheadPos[1], [])
    
    return paths

# %%
def print_paths(paths, grid):
    """
    Print the successful paths in a readable format.

    Args:
    - paths (list of lists): A list of successful paths, where each path is a list of tuples representing the row and column indices of the path.
    - grid (list of lists): A 2D grid of integers.
    """
    for i, path in enumerate(paths):
        print(f"Path {i+1}:")

        for row, col in path:
            print(f"({row}, {col}) = {grid[row][col]}", end=" -> ")
        
        print()
# ====================================================================================================================

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: The reindeer is holding a book titled "Lava Island Hiking Guide". However, when you open the book, you discover that most of it seems to have been scorched by lava! As you're about to ask how you can help, the reindeer brings you a blank topographic map of the surrounding area (your puzzle input) and looks up at you excitedly. Perhaps you can help fill in the missing hiking trails?# - Based on un-scorched scraps of the book, you determine that a good hiking trail is *as long as possible* and has an *even, gradual, uphill slope.
# - A hiking trail STARTS at height = 0; ENDS at height = 9; ALWAYS increases by a height of 1 at EACH step.
# - Hiking trails NEVER include diagonal steps - ONLY U-D-L-R movements.
# ! TODO: Calculate the sum total of the scores of ALL trailheads on the topographical map.
# - A trailhead is any position that STARTS one or more hiking trails => these positions will ALWAYS have height = 0.
# - A trailhead's score = the total number of reachable trails that end at height 9 (starting from the trailhead position, where height = 0).
# ====================================================================================================================
# ! Create a deep (independent) copy of the data, such that changes made to the copy do not affect the original data to still test/re-run Part 1/2 with the correct INITIAL (and not modified) data
# - NOTE: Not using a deep copy will modify the original data after running Part 1/2, therefore no correct output will be calculated anymore.
top_map = copy.deepcopy(file_data)
top_map = [list(row) for row in top_map.split('\n') if row]
numRows = len(top_map)
numCols = len(top_map[0]) if numRows > 0 else 0
sumScores = 0

# Convert grid values from strings to integers
# - NOTE: This is because func 'find_paths' handles grid values as integers, not as strings
for i in range(numRows):
    for j in range(numCols):
        top_map[i][j] = int(top_map[i][j])

# # Example usage
# grid = [
#     [8, 9, 0, 1, 0, 1, 2, 3],
#     [7, 8, 1, 2, 1, 8, 7, 4],
#     [8, 7, 4, 3, 0, 9, 6, 5],
#     [9, 6, 5, 4, 9, 8, 7, 4],
#     [4, 5, 6, 7, 8, 9, 0, 3],
#     [3, 2, 0, 1, 9, 0, 1, 2],
#     [0, 1, 3, 2, 9, 8, 0, 1],
#     [1, 0, 4, 5, 6, 7, 3, 2]
# ]

# tHeadPos = (0, 2)
# distinctPaths = find_paths(grid, tHeadPos)

# print_paths(distinctPaths, grid)

# reachablePaths = {}

# for path in distinctPaths:
#     if path:  # Ensure the list is not empty
#         last_value = path[-1]  # Get position of endtrail (9) in current path = the last element of the list
#         # If the key (last_value) is NOT already in the dictionary, add the list to the dictionary.
#         if last_value not in reachablePaths:
#             reachablePaths[last_value] = path

# reachablePaths = list(reachablePaths.values())

# # Calculate the score of the trailhead
# sumScore = len(reachablePaths)

#print(sumScore)

"""Calculate & sum scores of EACH trailhead found in the grid"""
for i in range(numRows):
    for j in range(numCols):
        if top_map[i][j] == 0: # Current position value = a trailhead
            tHeadPos = (i, j)
            # print(tHeadPos)
            distinctPaths = find_paths(top_map, tHeadPos)
            reachablePaths = {}

            for path in distinctPaths:
                if path:  # Ensure the list is not empty
                    last_value = path[-1]  # Get position of endtrail (9) in current path = the last element of the list
                    
                    # If the key (last_value) is NOT already in the dictionary, add the list to the dictionary.
                    if last_value not in reachablePaths:
                        reachablePaths[last_value] = path

            reachablePaths = list(reachablePaths.values())
            
            # Calculate the score of the trailhead
            sumScores += len(reachablePaths)

print("Total sum scores of all trailheads (PART 1):", sumScores)
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper. The paper describes a second way to measure a trailhead called its *rating*.
# - NOTE: A trailhead's rating is the number of *distinct hiking trails* which *begin at that trailhead*.
# ! TODO: Calculate the SUM of the *ratings* of ALL trailheads* in the grid.
#====================================================================================================================
top_map2 = copy.deepcopy(file_data)
top_map2 = [list(row) for row in top_map2.split('\n') if row]
numRows = len(top_map2)
numCols = len(top_map2[0]) if numRows > 0 else 0
sumRatings = 0

# # Example usage
# grid = [
#     [8, 9, 0, 1, 0, 1, 2, 3],
#     [7, 8, 1, 2, 1, 8, 7, 4],
#     [8, 7, 4, 3, 0, 9, 6, 5],
#     [9, 6, 5, 4, 9, 8, 7, 4],
#     [4, 5, 6, 7, 8, 9, 0, 3],
#     [3, 2, 0, 1, 9, 0, 1, 2],
#     [0, 1, 3, 2, 9, 8, 0, 1],
#     [1, 0, 4, 5, 6, 7, 3, 2]
# ]

# tHeadPos = (0, 4)
# distinctPaths = find_paths(grid, tHeadPos)
# reachablePaths = {}

# print_paths(distinctPaths, grid)

# Convert grid values from strings to integer
# - NOTE: This is because func 'find_paths' handles grid values as integers, not as strings
for i in range(numRows):
    for j in range(numCols):
        top_map2[i][j] = int(top_map2[i][j])

"""Calculate & sum ratings of EACH trailhead found in the grid"""
for i in range(numRows):
    for j in range(numCols):
        if top_map2[i][j] == 0: # Current position value = a trailhead
            tHeadPos = (i, j)
            # print(tHeadPos)
            distinctPaths = find_paths(top_map2, tHeadPos)
            
            # Calculate the score of the trailhead
            sumRatings += len(distinctPaths)

print("Total sum ratings of all trailheads (PART 2):", sumRatings)

# %%



