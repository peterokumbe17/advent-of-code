# %% [markdown]
# # Day 6: Guard Gallivant

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
# - The whole puzzle input represents a lab (grid map) patrolled by a guard.
# - '^': Represents the guard facing upwards.
# - '#': Represents any obstructions (crates, desks, etc.). 
# =====================================================================================================================
# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-6_input-test.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

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
def next_pos_is_obstacle(_grid, _direction, _guardCurrentRow, _guardCurrentCol):
    if _direction == 'up':
        # Check if the next position *upwards* is an obstacle
        #print(_grid[_guardCurrentRow - 1][_guardCurrentCol])
        if _grid[_guardCurrentRow - 1][_guardCurrentCol] == '#': return True

    if _direction == 'down':
        if _grid[_guardCurrentRow + 1][_guardCurrentCol] == '#': return True

    if _direction == 'left':
        if _grid[_guardCurrentRow][_guardCurrentCol - 1] == '#': return True

    if _direction == 'right':
        if _grid[_guardCurrentRow][_guardCurrentCol + 1] == '#': return True

    return False

# %%
def simulate_with_obstruction(map_data, obstruction_position):
        """
        NOTE: Simulates the guard's movement with an obstruction added at a specific position.
        
        Args:
        - obstruction_position (tuple[int, int]): The position where an obstruction is added.
        
        Returns:
        - bool: True if the guard gets stuck in a loop; False otherwise.
        """
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)] #UDRL
        current_direction = 0

        # Copy map data and add obstruction
        # - NOTE: Obstruction is added on every '.' in the grid to then check and see IF it will create a loop in the guard's path (See for loops in 'find_loop_positions' func below)
        modified_map = copy.deepcopy(map_data)
        modified_map[obstruction_position[0]][obstruction_position[1]] = '#'

        visited_states = set()
        
        # Find initial guard position
        for r, row in enumerate(map_data):
            for c, cell in enumerate(row):
                if cell == '^':
                    guard_position = (r, c)

        while True:
            state = (guard_position, current_direction)

            if state in visited_states:
                #print(state)
                #print("Loop detected with obstruction at:", obstruction_position)
                
                return True # Loop detected
            
            visited_states.add(state)

            next_row = guard_position[0] + directions[current_direction][0] # guard position +/- 1
            next_col = guard_position[1] + directions[current_direction][1] # guard position +/- 1

            if (not ((0 <= next_row < len(modified_map)) and (0 <= next_col < len(modified_map[0])))):
                return False

            # IF an obstruction is found in the guard's path, then turn guard RIGHT (90 degrees)
            if modified_map[next_row][next_col] == '#':
                current_direction = (current_direction + 1) % 4 # E.g. curr_dir = 1 (+ 1) = 2 (% 4) = 2; 0 -> 1 -> 2 -> 3 -> 0 ...
            else:
                guard_position = (next_row, next_col)

def find_loop_positions(map_data):
    """
    NOTE: Finds all possible positions where a new obstruction can be placed to trap the guard in a loop.

    Args:
    - map_data (list[str]): The lab map as a list of strings.

    Returns:
    - int: The number of valid positions where an obstruction can be placed.
    """
    valid_positions = set()
    
    for r in range(len(map_data)):
        for c in range(len(map_data[0])):
            if (map_data[r][c] == '.'): #and (not any(map_data[r][c] == '^' for r in map_data)):
                #print("Checking obstruction at position:", (r, c))
                if simulate_with_obstruction(map_data, (r, c)) == True:
                    valid_positions.add((r, c))
    
    #print("Valid positions for obstructions:", valid_positions)
    
    return len(valid_positions)
# ====================================================================================================================

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:
# - If there is something (e.g. an obstacle = '#') directly in front of a guard, turn right 90 degrees.
# - Otherwise, take a step forward.
# - TODO: Determine which specific positions in the lab (grid map) will be in the patrol path by predicting the guard's route and calculate the total number of distinct steps taken by the guard in the patrol path.
# - NOTE: The positions (including the guard's starting position) visited by the guard before leaving the area are marked with an 'X':
# - NOTE: A guard leaves the lab (grid map) after reaching the end of any of the 4 sides of the grid map. 
# ====================================================================================================================
# ! Create a deep (independent) copy of the grid data, such that changes made to the copy do not affect the original grid to still test/re-run Part 1 with the correct INITIAL (and not modified) grid
# - NOTE: Not using a deep copy will modify the original grid after running Part 1, therefore no correct output will be calculated anymore
part1_grid = copy.deepcopy(grid)

nRows = len(part1_grid)
nCols = len(part1_grid[0])
guardCurrentRow = 0; guardCurrentCol = 0
direction = '' # string var to store the name of the current direction of the guard
steps = 0 # int var to store the total number of steps the guard takes in her patrol path.

# Determine initial position of guard
for rowIdx in range(nRows):
    for colIdx in range(nCols):
        if part1_grid[rowIdx][colIdx] == '^':
            # Set guard's initial position
            guardCurrentRow = rowIdx
            guardCurrentCol = colIdx
            direction = 'up'

# While the guard has NOT reached the END of any 1 of the 4 sides of the lab (grid)
while 0 < guardCurrentRow < (nRows - 1) and 0 < guardCurrentCol < (nCols - 1):
    # Mark current position as visited
    part1_grid[guardCurrentRow][guardCurrentCol] = 'X'
    # Check if the NEXT position (in relation to the CURRENT position) is an obstacle
    hitObstacle = next_pos_is_obstacle(part1_grid, direction, guardCurrentRow, guardCurrentCol)

    if direction == 'up':
        if hitObstacle == False:
            guardCurrentRow -= 1 # Move guard 1 position [up]
            #grid[guardCurrentRow][guardCurrentCol] = 'X'
        elif hitObstacle == True:
            # Turn guard right 90 degrees
            direction = 'right'
    # NOTE: 'elif' used to prevent previous if statement to continue to this (and remaining) if statements if not applicable
    elif direction == 'down':
        # Check if next position is an obstacle
        if hitObstacle == False:
            guardCurrentRow += 1 # Move guard 1 position [down]
        elif hitObstacle == True:
            # Turn guard right 90 degrees
            direction = 'left'

    elif direction == 'left':
        # Check if next position is an obstacle
        if hitObstacle == False:
            guardCurrentCol -= 1 # Move guard 1 position [left]
        elif hitObstacle == True:
            # Turn guard right 90 degrees
            direction = 'up'

    elif direction == 'right':
        # Check if next position is an obstacle
        if hitObstacle == False:
            guardCurrentCol += 1 # Move guard 1 position [right]
        elif hitObstacle == True:
            # Turn guard right 90 degrees
            direction = 'down'

    # while loop BREAK condition
    if guardCurrentRow == 0 or guardCurrentRow == (nRows - 1) or guardCurrentCol == 0 or guardCurrentCol == (nCols - 1):
        part1_grid[guardCurrentRow][guardCurrentCol] = 'X' # Mark last visited position
        break

# Count the total number of DISTINCT visited areas in the grid
for row in part1_grid:
    for col in row:
        if col == "X":
            steps += 1

print("Total number of distinct areas visited (PART 1):", steps)
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search. To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.
# - NOTE: In the given example (see website), there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop.
# - TODO: It doesn't really matter what you choose to use as an obstacle (0, *, %, etc.), as long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes. You need to get the guard stuck in a LOOP by adding a SINGLE new obstruction. How many different positions could you choose for this obstruction?
#====================================================================================================================
# ! Create a deep (independent) copy of the grid data, such that changes made to the copy do not affect the original grid to still test/re-run Part 1 with the correct INITIAL (and not modified) grid
# - NOTE: Not using a deep copy will modify the original grid after running Part 1, therefore no correct output will be calculated anymore
part2_grid = copy.deepcopy(grid)

# NOTE: Function below takes abit of time to run with large data grid (approx. 3min)
numLoops = find_loop_positions(part2_grid)

print("Total number of loop positions found (PART 2):", numLoops)

# %%



