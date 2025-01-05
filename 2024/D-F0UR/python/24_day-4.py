# %% [markdown]
# # Day 4: Ceres Search

# %% [markdown]
# ## Import data

# %%
# *** [IMPORT DATA] ***
# =====================================================================================================================
import os
import re

# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-4_input.txt")

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
def find_horizontal(grid, word): # Finds horizontal matches
    numMatches = 0

    for row in grid:
        # L2R search:
        # - Use re.finditer to find all occurrences of the word in the row
        matches = re.finditer(word, row)
        numMatches += sum(1 for _ in matches)

    return numMatches

# %%
def find_vertical(grid, word): # Finds vertical matches
    num_rows = len(grid)
    num_cols = len(grid[0])
    numMatches = 0

    for col_index in range(num_cols):
        column = ''.join(grid[row][col_index] for row in range(num_rows))
        
        # T2B search
        # - Use re.finditer to find all occurrences of the word in the row
        matches = re.finditer(word, column)
        numMatches += sum(1 for _ in matches)

    return numMatches

# %%
def find_word_in_diagonals(grid, word):
    rows = len(grid)
    cols = len(grid[0])
    diagonals = []
    numMatches = 0
    
    # Extract primary diagonals (top-left to bottom-right)
    for d in range(rows + cols - 1):
        diagonal = []

        for i in range(max(0, d - cols + 1), min(rows, d + 1)):
            diagonal.append(grid[i][d - i])

        diagonals.append("".join(diagonal))
    
    # Extract anti-diagonals (bottom-left to top-right)
    for d in range(rows + cols - 1):
        diagonal = []

        for i in range(max(0, d - cols + 1), min(rows, d + 1)):
            diagonal.append(grid[rows - 1 - i][d - i])

        diagonals.append("".join(diagonal))
    
    # Search for the word in each diagonal
    for diagonal in diagonals:
        matches = re.finditer(word, diagonal)
        count = sum(1 for _ in matches)
        numMatches += count
    
    return numMatches

# %%
# def find_diagonal(grid, word):
#     num_cols = len(grid[0])
#     numMatches = 0
#     num_rows = len(grid)
#     #max_diag = num_rows + num_cols - 1  # Total possible diagonals
    
#     # ! Search diagonals from middle to top-right (incl. middle) AND to bottom-left (symmetrical excl. middle)
#     for colStart in range(num_cols): # 0 -> (n - 1)
#         currentRow = 0
#         diagonal = ''   
#         symmetricalDiagonal = ''

#         # NOTE: The end of any diagonal (L2R) in the grid is dependent on the end of the last column
#         for currentCol in range(colStart, num_cols):
#             diagonal += grid[currentRow][currentCol] # middle to top-right search
#             symmetricalDiagonal += grid[currentCol][currentRow] # middle to bottom-left search
            
#             currentRow += 1
        
#         # Find all matches of 'word' in the currently built diagonal string
#         # for match in re.finditer(word, diagonal):
#         #     matches.append(match.start())
#         matches = re.finditer(word, diagonal)
#         numMatches += sum(1 for _ in matches)
        
#         # Find all matches of 'word' in the currently built symmetrical diagonal string
#         # - NOTE: Skip searching through middle diagonal for symmetrical diagonal
#         #reversedSymmDiagonal = ''.join(reversed(symmetricalDiagonal)) # Reverse string to match original diagonal string, since symm diag string is built in reverse

#         # NOTE: Middle diag is NOT checked against reversed symmetrical version because [0,0]; [1,1], etc. (for middle diag in 4x4 grid) co-ords swapped = the same string built
#         if diagonal != symmetricalDiagonal:
#             # for match in re.finditer(word, symmetricalDiagonal):
#             #     matches.append(match.start())
#             matches = re.finditer(word, symmetricalDiagonal)
#             numMatches += sum(1 for _ in matches)
#     # ------------------------------------------------------------------------------------------------------------
#     # TODO: Search diagonals from middle to top-left (incl. middle)
#     for colStart in range((num_cols - 1), -1, -1): # (n - 1) -> 0
#         currentRow = 0
#         #currentRow2 = 0
#         diagonal = ''   
#         #symmetricalDiagonal = ''

#         # NOTE: The end of any diagonal (R2L) in the grid is dependent on the end of the first column
#         for currentCol in range(colStart, -1, -1): # (n - 1) -> 0
#             diagonal += grid[currentRow][currentCol] # middle to top-left search
#             #symmetricalDiagonal += grid[currentCol][currentRow] # middle to bottom-right search
            
#             currentRow += 1 # top -> bottom

#         # Find all matches of 'word' in the currently built diagonal string
#         # for match in re.finditer(word, diagonal):
#         #     matches.append(match.start())
#         matches = re.finditer(word, diagonal)
#         numMatches += sum(1 for _ in matches)

#     # TODO: Search diagonals from middle to bottom-right (symmetrical excl. middle)
#     for colStart in range(num_cols): # 0 -> (n - 1)
#         currentRow = num_rows - 1
#         diagonal = ''   
#         symmetricalDiagonal = ''

#         # NOTE: The end of any diagonal (R2L) in the grid is dependent on the end of the first column
#         for currentCol in range(colStart, num_cols): # 0 -> (n - 1)
#             symmetricalDiagonal += grid[currentRow][currentCol] # bottom to top build
#             diagonal += grid[currentCol][currentRow] # top to bottom build
            
#             currentRow -= 1 # bottom -> top
        
#         # Find all matches of 'word' in the currently built symmetrical diagonal string
#         # - NOTE: Skip searching through middle diagonal for symmetrical diagonal
#         reversedSymmDiagonal = ''.join(reversed(symmetricalDiagonal)) # Reverse string to match original diagonal string since symm diag string is built in reverse

#         # NOTE: Middle diag IS checked against reversed symmetrical version because [0,3]; [1,2], etc. (for middle diag in 4x4 grid) co-ords swapped != the same string built
#         # - It is the reversed version built from bottom to top, so need to reverse it back to original version read from top to bottom
#         if diagonal != reversedSymmDiagonal:
#             # for match in re.finditer(word, symmetricalDiagonal):
#             #     matches.append(match.start())
#             matches = re.finditer(word, reversedSymmDiagonal)
#             numMatches += sum(1 for _ in matches)

#     return numMatches

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: 'AssertionErrorXMAS'.
# - TODO: Find all occurrences (horizontal, vertical, diagonal) of the word 'XMAS' (forwards & backwards) in the provided word search grid (puzzle input).
# ====================================================================================================================
# Define the words to search for
words = ["XMAS", "SAMX"]
numMatches = 0
       
for word in words:
    numMatches += find_horizontal(file_data, word)
    numMatches += find_vertical(file_data, word)
    numMatches += find_word_in_diagonals(file_data, word)

# print(find_diagonal(file_data, words[0]))
# print(find_word_in_diagonals(file_data, words[0]))
# print(find_diagonal(file_data, words[1]))
# print(find_word_in_diagonals(file_data, words[1]))

print("Number of times that 'XMAS' appears (PART 1):", numMatches)

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two 'MAS' in the shape of an 'X'.
# - TODO: Determine how many times two 'MAS' in the shape of an 'X' (diagonally) appears in the grid word search.
# ---------------------------------------------------------------------------------------------------------------------
grid = file_data
num_cols = len(grid[0]) # Size of string in first line of grid
num_rows = len(grid)
numMatches = 0

# ! Search grid
# NOTE: Only search for 'A' within inner layers of grid
for row in range(num_rows):
    for col in range(num_cols):
        # Inner layer of grid search
        if (row != 0) and (row != num_rows - 1) and (col != 0) and (col != num_cols - 1):
            if grid[row][col] == 'A':
                topLeft = grid[row - 1][col - 1]
                topRight = grid[row - 1][col + 1]
                bottomLeft = grid[row + 1][col - 1]
                bottomRight = grid[row + 1][col + 1]

                # S-A-M x S-A-M
                if topLeft == 'S' and bottomRight == 'M':
                    if topRight == 'S' and bottomLeft == 'M':
                        numMatches += 1
                
                # M-A-S x M-A-S
                if topLeft == 'M' and bottomRight == 'S':
                    if topRight == 'M' and bottomLeft == 'S':
                        numMatches += 1
                # -------------------------------------------
                # S-A-M x M-A-S
                if topLeft == 'S' and bottomRight == 'M':
                    if topRight == 'M' and bottomLeft == 'S':
                        numMatches += 1
                
                # M-A-S x S-A-M
                if topLeft == 'M' and bottomRight == 'S':
                    if topRight == 'S' and bottomLeft == 'M':
                        numMatches += 1

print("Number of times that 'XMAS' appears (PART 2):", numMatches)

# %%



