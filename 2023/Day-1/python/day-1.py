# -*- coding: utf-8 -*-

# Day 1: Trebuchet?!


# *** [AoC DAY 1 Challenge] ***
# =====================================================================================================================
import os
import re

# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "..\\data", "day-1-input.txt")

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
#     line = line.strip() # Remove all trailing spaces that exist in the string 'line'
#     #print(line[-1])



print(arrFileData)
print(len(arrFileData))

# *** [PART 1] ***
# ! The newly-improved calibration document consists of lines of text:
# - Each line originally contained a specific *calibration value* that the Elves now need to recover. 
# - On each line, the *calibration value* can be found by combining the *FIRST* digit and the *LAST* digit (in that order) to form a single two-digit number (calibration value).
# - Add the obtained *calibration values* in each line to derive the final answer.
# ---------------------------------------------------------------------------------------------------------------------
arrCalibrationValues = [] # array list to store derived calibration values of each string line in 'arrFileData' var

for line in arrFileData:
    # Get list of all digits in current string line and store in array list
    lineDigits = re.findall(r'\d', line)

    # Combine the *first* and *last* digits found to create a 2-digit number = calibration value of the current string line
    calibrationValue = lineDigits[0] + lineDigits[-1]
    
    arrCalibrationValues.append(calibrationValue)

print('Calibration values:', arrCalibrationValues)

totalValue = 0 # var to store the total value of adding all of the calibration values together 

for digit in arrCalibrationValues:
    totalValue = totalValue + int(digit)

print('Sum of calibration values:', totalValue)

# ====================================================================================================================

# *** [PART 2] ***
# ! Your calculation isn't quite right. It looks like some of the digits in the calibration document's lines of text are actually spelled out with letters:
# - 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', and 'nine' also count as valid "digits".
# - Equipped with this new information, you now need to find the real *first* and *last* digit on each line.
# --------------------------------------------------------------------------------------------------------------------
arrCalibrationValues = [] # array list to store derived calibration values of each string line in 'arrFileData' var
numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
counter = 0

for line in arrFileData:
    calibrationValue = ''
    digitWordFound = -1
    lineWordDigits = []

    counter = counter + 1

    # Get list of all digits in current string line and store in array list
    lineDigits = re.findall(r'\d', line)
    #lineWordDigits = re.findall(r'one|two|three|four|five|six|seven|eight|nine|ten', line)

    # ! EDGE CASE HINT: Cater for edge cases such as 'xxxseveninexxx' = '79'
    # - Traverse through the current string line, then find EVERY occurrence of a word digit in the current line's
    #   string and store EACH found word digit in an array list ('lineWordDigits')
    for i, letter in enumerate(line):
        # IF 'one' exists anywhere between the ith and 'i + len('one')'th indexed char of the current string line 
        for wordDigit in numbers:
            if wordDigit in line[i:(i + len(wordDigit))]: 
                lineWordDigits.append(wordDigit)

    # # Store the index number of EVERY word digit found in the current string line in an array list
    # wordDigitIndexes = []

    # for wordDigit in lineWordDigits:
    #     wordDigitIndex = line.find(wordDigit)
    #     wordDigitIndexes.append(wordDigitIndex)

    # # Re-arrange the order (ASC) of EVERY stored word digit as per the index numbers of EACH word digit
    # for i in range(len(lineWordDigits)):
    #     for j in range((i + 1), len(lineWordDigits)):
    #         if wordDigitIndexes[j] < wordDigitIndexes[i]:
    #             temp = wordDigitIndexes[j]
    #             wordDigitIndexes[j] = wordDigitIndexes[i]
    #             wordDigitIndexes[i] = temp

    #             temp = lineWordDigits[j]
    #             lineWordDigits[j] = lineWordDigits[i]
    #             lineWordDigits[i] = temp

    #print(lineDigits)
    #print(lineWordDigits)

    if (counter == 49): #990
        print(lineDigits)
        print(lineWordDigits)
        #print(wordDigitIndexes)
# ---------------------------------------------------------------------------------------------------------------
    # Retrieve indexes of *first* and *last* numeric AND word digits found in current string line
    firstDigitIndex = -1
    firstWordDigitIndex = -1
    lastDigitIndex = -1
    lastWordDigitIndex = -1

    if (lineDigits and len(lineDigits) == 1) and (lineWordDigits and len(lineWordDigits) == 1): #e.g. '9seven'
        firstDigitIndex = line.find(lineDigits[0])
        firstWordDigitIndex = line.find(lineWordDigits[0])

        if firstDigitIndex < firstWordDigitIndex:
            calibrationValue = lineDigits[0] + lineWordDigits[0]
        elif firstDigitIndex > firstWordDigitIndex:
            calibrationValue = lineWordDigits[0] + lineDigits[0]
    # Calibration values of string lines that have 1 digit/word digit = duplicated appeneded value of the singular
    # digit/word digit: e.g. Calibration value of 'xxxxx2xxxxx' = '22'
    elif (lineDigits and len(lineDigits) == 1) and (not lineWordDigits):
        calibrationValue = lineDigits[0] + lineDigits[0] 
    elif (lineWordDigits and len(lineWordDigits) == 1) and (not lineDigits):
        calibrationValue = lineWordDigits[0] + lineWordDigits[0]
    else:
        # If numeric digits have been found in the current string line, then store index of *first* numeric digit
        if lineDigits:
            firstDigitIndex = line.find(lineDigits[0])
            #print(line, firstDigitIndex)
        
        # If word digits have been found in the current string line, then store index of *first* word digit
        if lineWordDigits:
            firstWordDigitIndex = line.find(lineWordDigits[0])
            #print(line, firstWordDigitIndex)

        # If *first* numeric digit's index < *first* word digit's index, then select *first* numeric digit as digit #1 for
        # the calibration value, ELSE select *first* word digit as digit #1 for the calibration value
        if (firstDigitIndex != -1 and firstWordDigitIndex == -1):
            calibrationValue = lineDigits[0]
        elif (firstWordDigitIndex != -1 and firstDigitIndex == -1):
            calibrationValue = lineWordDigits[0]
        elif (firstDigitIndex != -1 and firstWordDigitIndex != -1):
            if firstDigitIndex < firstWordDigitIndex:
                calibrationValue = lineDigits[0]
            elif firstDigitIndex > firstWordDigitIndex:
                calibrationValue = lineWordDigits[0]     #'nineeightfour7'
    # ---------------------------------------------------------------------
        # If numeric digits have been found in the current string line, then store index of *last* numeric digit
        if lineDigits:
            lastDigitIndex = line.rfind(lineDigits[-1])
        
        # If word digits have been found in the current string line, then store index of *last* word digit
        if lineWordDigits:
            lastWordDigitIndex = line.rfind(lineWordDigits[-1])

        # If *last* numeric digit's index < *last* word digit's index, then select *last* numeric digit as 
        # digit #1 for the calibration value, ELSE select *last* word digit as digit #1 for the calibration value
        if (lastDigitIndex != -1 and lastWordDigitIndex == -1):
            calibrationValue = calibrationValue + lineDigits[-1]
        elif (lastWordDigitIndex != -1 and lastDigitIndex == -1):
            calibrationValue = calibrationValue + lineWordDigits[-1]
        elif (lastDigitIndex != -1 and lastWordDigitIndex != -1):
            if lastDigitIndex > lastWordDigitIndex:
                # Combine the *first* and *last* digits found to create a 2-digit number = calibration value 
                # of the current string line
                calibrationValue = calibrationValue + lineDigits[-1]
            elif lastDigitIndex < lastWordDigitIndex:
                # Combine the *first* and *last* digits found to create a 2-digit number = calibration value 
                # of the current string line
                calibrationValue = calibrationValue + lineWordDigits[-1]

    #print("\n\n")
# ---------------------------------------------------------------------------------------------------------------
    # # Combine the first and last digits found to create a 2-digit number = calibration value of the current string line
    # calibrationValue = lineDigits[0] + lineDigits[-1]
    
    arrCalibrationValues.append(calibrationValue)

print('Calibration values:', arrCalibrationValues)

arrDigitCalibrationValues = []

for cValue in arrCalibrationValues:
    cValue = re.sub('one', '1', cValue)
    cValue = re.sub('two', '2', cValue)
    cValue = re.sub('three', '3', cValue)
    cValue = re.sub('four', '4', cValue)
    cValue = re.sub('five', '5', cValue)
    cValue = re.sub('six', '6', cValue)
    cValue = re.sub('seven', '7', cValue)
    cValue = re.sub('eight', '8', cValue)
    cValue = re.sub('nine', '9', cValue)
    #print(cValue)
    arrDigitCalibrationValues.append(cValue)

print('DIGIT Calibration values:', arrDigitCalibrationValues)

totalValue = 0 # var to store the total value of adding all of the calibration values together 

for digit in arrDigitCalibrationValues:
    totalValue = totalValue + int(digit)

print('Sum of calibration values:', totalValue)

# # -- tinkerassist part 2 solution -- 
# sum = 0 # create our sum integer
# # create list of integers spelled-out in english
# integer_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
# calValues2 = []
# arrNums = []
# for line in arrFileData:
#     #print(line)
#     nums = [] # craate empty list that we will use to track all integers in list
#     for i, letter in enumerate(line): # loop through each character in the current string line and associate an index value to it: (1,'x')
#         for val, name in enumerate(integer_names): # loop through all word digit options: '(val, name)' = (0, 'zero')
#             if name in line[i:i+len(name)]: # if the current spelled-out number we are looking for is found starting at index i, add it to our nums list: e.g. if 'one' in 'xxxonexxxxxx' from i = 0 to 11 in 'line'
#                 nums.append(str(val)) # append to our list of integer characters
#         if ord(letter) <= 57: # if unicode value of character is <=57, we know it's an integer
#             nums.append(letter) # append to our list of integer characters

#     arrNums.append(nums)
#     # concat the first and last characters of our list and add their integer representation to our sum
#     calValue = int(nums[0] + nums[-1])
#     sum += calValue
#     calValues2.append(calValue)
#     #print("line:", line, "digits:", nums, "calValue:", calValue)


# for i in range(len(calValues2)):
#     if int(arrDigitCalibrationValues[i]) != int(calValues2[i]):
#         print("#" + str(i) + ":", arrDigitCalibrationValues[i], "!=", calValues2[i])
#         print(arrFileData[i])
#         print(arrCalibrationValues[i], "!=", arrNums[i])
#         print("===================")


# # print(len(arrDigitCalibrationValues))
# # print(len(calValues2))
# print(sum) # print solution to part 2

# *** !!! TESTING !!! ***
# =====================================================================================================================
lineDigitWords = 'this one is one4my name  peter 3five onehaha'
#lineDigitWords = re.findall(r'one|two|three|four|five|six|seven|eight|nine|ten', lineDigitWords)
lineDigitIdx = lineDigitWords.find('one')

print(lineDigitIdx)


text = 'twonine'

text = re.sub('two', '2', text)
text = re.sub('five', '5', text)
text = re.sub('nine', '9', text)

arrWords = ['one', 'five', 'nine']
arrIndexes = [22, 0, 4]

print(arrWords[0], arrIndexes[0])
print(arrWords[1], arrIndexes[1])
print(arrWords[2], arrIndexes[2])

for i in range(len(arrWords)):
    for j in range(i+1, len(arrWords)):
        if arrIndexes[j] < arrIndexes[i]:
            temp = arrIndexes[j]
            arrIndexes[j] = arrIndexes[i]
            arrIndexes[i] = temp

            temp = arrWords[j]
            arrWords[j] = arrWords[i]
            arrWords[i] = temp

if not('five' in arrWords):
    print('five does not exist')
else:
    print('five exists')

# arrtest = []

# if (not arrtest):
#     print('empty')
# else:
#     print('not empty')

word = 'abcdefg'

print(list(enumerate(word)))

wordTest = 'wordonegoingoneagaintwoback'
wordTestDigits = []

for i, letter in enumerate(wordTest):
    if 'one' in wordTest[i:i + len('one')]:
        wordTestDigits.append('one')

print(wordTestDigits)

print(arrIndexes)
print(arrWords)
# print(text)
# arr = ['1']
# print(arr[-1])