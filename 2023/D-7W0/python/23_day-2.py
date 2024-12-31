# -*- coding: utf-8 -*-

# Day 2: Cube Conundrum

# *** [AoC DAY 2 Challenge] ***
# =====================================================================================================================
import os
import re

# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "23_day-2_input.txt")

# ! Open the data file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
arrFileData = file.read()
# Split the data read from the file by every new line encountered and store in an array list
arrFileData = arrFileData.split('\n')

# # ! Read all lines in the .txt file and store each line as a string in an array list
# arrFileData = file.readlines()

# # arrFileData = []

# # while True:
# #     line = file.readline()
# #     arrFileData.append(line)
        
# #     if not line:
# # 	    break

# file.close()

# # ! Remove new line('\n') from each string in array list
# for line in arrFileData:
#     #line = line.replace("\n", "")
#     line = line.strip()
#     #print(line[-1])

print(arrFileData)
print(len(arrFileData))

# *** [PART 1] ***
# ! As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. 
# - Each time you play this game, he will hide a secret number of cubes of each color in the bag.
# - Your goal is to figure out *information* about the number of cubes.
# - The Elf would first like to know which games would have been possible if the bag contained ONLY: 
#   - [12 red cubes], [13 green cubes], and [14 blue cubes]
# ---------------------------------------------------------------------------------------------------------------------
# ! Create vars that store max value restriction for how many coloured cubes exist in the bag 
#   for EACH set in EACH game
max_red = 12
max_green = 13
max_blue = 14

counter = 0 # counter var to keep track of the ID of EACH game
sumPossibleIDs = 0 # var to store the sum of IDs of POSSIBLE games

# ! Traverse through each game in the array list var 'arrFileData':
# - In EACH set in EACH game, IF the number of cubes for a particular colour cube in the CURRENT game's set 
#   is greater than (>) the maximum number of cubes for that specific colour in the bag, then the CURRENT game 
#   is regarded as NOT possible.
for game in arrFileData:
    counter = counter + 1 # increment counter for ID of CURRENT game

    num_red = 0 # var stores the total number of red coloured cubes in EACH set of EACH game
    num_green = 0
    num_blue = 0

    nonPossibleSetFound = 0 # var to determine if a non possible set has been found in the CURRENT game

    print(game)
    arrGameSplit = game.split(':')
    arrGameSets = arrGameSplit[1]
    print(arrGameSets)
    #arrGameSets = re.split('[,;]', arrGameSets) # multiple delimiters: '[xxx]' > e.g. '[,;:]'
    arrGameSets = arrGameSets.split(';')
    print(arrGameSets)

    # Traverse through EACH set in the CURRENT game
    for gameSet in arrGameSets:
        arrCubeValues = [] # var to store the number and colour of every cube drawn in EACH set for the CURRENT game

        # Separate the number of cubes drawn in the CURRENT set of the CURRENT game
        arrGameSet = gameSet.strip().split(',')
        #print("#", arrGameSet)

        # Traverse through EACH cube drawn in the CURRENT set of the CURRENT game
        for cube in arrGameSet:
            arrCubeValues = cube.strip().split(' ') # E.g ['3 red'] => ['3', 'red']
            print("#", arrCubeValues)

            # ! Check if 'red/green/blue' exists in the CURRENT value of the CURRENT set in the CURRENT game
            # - IF the respective colour exists, then set the respective number to the var holding the total
            #   number of cubes for that particular colour in the CURRENT set of the CURRENT game
            if arrCubeValues[1] == 'red':
                num_red = int(arrCubeValues[0])

            if arrCubeValues[1] == 'green':
                num_green = int(arrCubeValues[0])

            if arrCubeValues[1] == 'blue':
                num_blue = int(arrCubeValues[0])

        #print('#red:', num_red, '#green:', num_green, '#blue:', num_blue)

        # ! CHECK if the CURRENT set in the CURRENT game is POSSIBLE
        # - ALL sets in the CURRENT game MUST pass this check for the game to be deemed POSSIBLE
        if (num_red <= max_red) and (num_green <= max_green) and (num_blue <= max_blue):
            #sumPossibleIDs = sumPossibleIDs + counter
            print("POSSIBLE SET IN CURRENT GAME")
        else:
            nonPossibleSetFound = 1
            print("NON POSSIBLE SET IN CURRENT GAME")

    if nonPossibleSetFound == 0:
        sumPossibleIDs = sumPossibleIDs + counter
        print("--- POSSIBLE GAME ---")
    else:
        print("--- NON POSSIBLE GAME ---")

print("Sum of possible game IDs:", sumPossibleIDs)
# --------------------------------------------------------------------------------------------------------------------
    # ! Traverse through EACH set's values in the CURRENT game
    #for gameSet in arrGameSets: 

        # # ! Check if 'red' exists in the CURRENT value of the CURRENT set in the CURRENT game
        # if gameSet.find('red') != -1:
        #     arrDigits = re.findall(r'\d', gameSet)
        #     # IF the respective colour exists, then add the respective number to the var holding the sum of cubes
        #     # for that particular colour in the CURRENT game
        #     if arrDigits:
        #         number = '' # var to store built string number value

        #         # for ALL found digits in the CURRENT value of the CURRENT set in the CURRENT game
        #         for digit in arrDigits:
        #             number = number + digit # append digit to string number var - e.g. '2' + '1' = '21'

        #         num_red = num_red + int(number)

        # # ! Check if 'green' exists in the CURRENT value of the CURRENT set in the CURRENT game
        # if gameSet.find('green') != -1:
        #     arrDigits = re.findall(r'\d', gameSet)
        #     # IF the respective colour exists, then add the respective number to the var holding the sum of cubes
        #     # for that particular colour in the CURRENT game
        #     if arrDigits:
        #         number = '' # var to store built string number value

        #         # for ALL found digits in the CURRENT value of the CURRENT set in the CURRENT game
        #         for digit in arrDigits:
        #             number = number + digit # append digit to string number var - e.g. '2' + '1' = '21'

        #         num_green = num_green + int(number)

        # # ! Check if 'blue' exists in the CURRENT value of the CURRENT set in the CURRENT game
        # if gameSet.find('blue') != -1:
        #     arrDigits = re.findall(r'\d', gameSet)
        #     # IF the respective colour exists, then add the respective number to the var holding the sum of cubes
        #     # for that particular colour in the CURRENT game
        #     if arrDigits:
        #         number = '' # var to store built string number value

        #         # for ALL found digits in the CURRENT value of the CURRENT set in the CURRENT game
        #         for digit in arrDigits:
        #             number = number + digit # append digit to string number var - e.g. '2' + '1' = '21'

        #         num_blue = num_blue + int(number)
    
#     print('#red:', num_red, '#green:', num_green, '#blue:', num_blue)

#     if (num_red <= max_red) and (num_green <= max_green) and (num_blue <= max_blue):
#         sumPossibleIDs = sumPossibleIDs + counter

#         print("POSSIBLE")
#     else:
#         print("NOT POSSIBLE")

print('# =====================================================================================================================')

# *** [PART 2] ***
# ! As you continue your walk, the Elf poses a second question: In each game you played, what is the *fewest* number #   of cubes of EACH color that could have been in the bag to make the game possible?
# - For each game, find the *minimum* set of cubes that must have been present to make the game possible.
# - What is the sum of the power of these sets?
# - The power of a set of cubes = the number of red, green, and blue cubes multiplied together.
# --------------------------------------------------------------------------------------------------------------------
counter = 0 # counter var to keep track of the ID of EACH game
sumPowers = 0 # var to store the sum of the powers of ALL games

# ! Traverse through each game in the array list var 'arrFileData':
for game in arrFileData:
    counter = counter + 1 # increment counter for ID of CURRENT game

    # ! Create vars that store max value restriction for how many coloured cubes exist in the bag 
    #   for EACH set in EACH game
    max_red = 0
    max_green = 0
    max_blue = 0

    power = 0

    print(game)
    arrGameSplit = game.split(':')
    arrGameSets = arrGameSplit[1]
    print(arrGameSets)
    #arrGameSets = re.split('[,;]', arrGameSets) # multiple delimiters: '[xxx]' > e.g. '[,;:]'
    arrGameSets = arrGameSets.split(';')
    print(arrGameSets)

    # Traverse through EACH set in the CURRENT game
    for gameSet in arrGameSets:
        arrCubeValues = [] # var to store the number and colour of every cube drawn in EACH set for the CURRENT game

        # Separate the number of cubes drawn in the CURRENT set of the CURRENT game
        arrGameSet = gameSet.strip().split(',')
        #print("#", arrGameSet)

        # Traverse through EACH cube drawn in the CURRENT set of the CURRENT game
        for cube in arrGameSet:
            arrCubeValues = cube.strip().split(' ') # E.g ['3 red'] => ['3', 'red']
            print("#", arrCubeValues)

            # ! Check if 'red/green/blue' exists in the CURRENT value of the CURRENT set in the CURRENT game
            # - IF the respective colour exists, then set the respective number to the var holding the highest
            #   number of cubes for that particular colour in the CURRENT game
            if (arrCubeValues[1] == 'red') and (int(arrCubeValues[0]) > max_red):
                max_red = int(arrCubeValues[0])

            if (arrCubeValues[1] == 'green') and (int(arrCubeValues[0]) > max_green):
                max_green = int(arrCubeValues[0])

            if (arrCubeValues[1] == 'blue') and (int(arrCubeValues[0]) > max_blue):
                max_blue = int(arrCubeValues[0])

        #print('#red:', num_red, '#green:', num_green, '#blue:', num_blue)

    power = max_red * max_green * max_blue
    sumPowers = sumPowers + power

    print("--- Game", counter, ":", "min_red =", max_red, "min_green =", max_green, "min_blue =", max_blue, "---")
    print(" --- POWER =", power)

print("*Sum of powers of ALL games:", sumPowers)

# # *** !!! TESTING !!! ***
# # =====================================================================================================================
# arrSet = ' red'
# lineDigits = re.findall(r'\d', arrSet)


# if lineDigits:
#     print('not empty')
# else:
#     print('empty')

# print(arrSet.find('red'))
# print(lineDigits)