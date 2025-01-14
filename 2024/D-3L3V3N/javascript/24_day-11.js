// # Day 11: Plutonian Pebbles

// ## Import libraries
const fs = require('fs');
const path = require('path');

// ## Import data

// *** [IMPORT DATA] ***
// NOTE: In the given puzzle input:
// - A string list of stones (represented by numbers) in a straight line.
// =====================================================================================================================
// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-11_input.txt");

// ! Open the file for reading mode (= default mode if the mode is not specified)
let fileData = fs.readFileSync(filePath, 'utf8').trim();

// Read all the data in the file
fileData = fileData.split(" ");

console.log(fileData);
// ====================================================================================================================

// ## Helper functions

function changeNumbers(numbers) {
    /**
     * Process a list of string numbers according to the following rules:
     * 1. If the value is '0', replace it with '1'.
     * 2. If the value has an even number of digits, split it into two numbers.
     * 3. If the value does not meet the above conditions, multiply it by 2024.
     *
     * Args:
     * - numbers (list): A list of string numbers.
     *
     * Returns:
     * - list: The processed list of numbers.
     */
    const arrChangedNumbers = [];

    numbers.forEach(num => {
        // Rule 1: Replace '0' with '1'
        if (num === '0') {
            arrChangedNumbers.push('1');
        } else {
            // Rule 2: Split even-length numbers into two
            if (num.length % 2 === 0) {
                const half = num.length / 2;
                let num1 = num.slice(0, half);
                let num2 = num.slice(half);
                // Remove leading zeros
                num1 = num1.replace(/^0+/, '') || '0';
                num2 = num2.replace(/^0+/, '') || '0';
                arrChangedNumbers.push(num1, num2);
            } else {
                // Rule 3: Multiply by 2024
                arrChangedNumbers.push((parseInt(num) * 2024).toString());
            }
        }
    });

    return arrChangedNumbers;
}
// =====================================================================================================================

// ## Part 1

// *** [PART 1] ***
// ! PROBLEM: The ancient civilization on Pluto was known for its ability to manipulate spacetime, and while The Historians explore their infinite corridors, you've noticed a strange set of physics-defying stones. At first glance, they seem like normal stones: they're arranged in a perfectly *straight line*, and EACH stone has a *number* engraved on it. The strange part is that every time you BLINK, the stones CHANGE:
// - If the stone is engraved with the number '0', it is replaced by a stone engraved with the number '1'.
// - If the stone is engraved with a number that has an EVEN number of *digits*, it is REPLACED by TWO stones. The LEFT half of the CURRENT stone's digits are engraved on the new left stone, and the RIGHT half of the digits are engraved on the new right stone. (NOTE: The new numbers don't keep extra leading zeroes: E.g. '1000' would become stones '10'(L) and '0'(R).)
// - If none of the above rules apply, then the stone is REPLACED by a new stone = the old stone's number * 2024.
// - NOTE: No matter how the stones CHANGE, their order is PRESERVED, and they stay on their perfectly straight line.
// ! TODO: Consider the arrangement of stones in front of you (puzzle input). How many stones will you have after blinking 25 times?
// ====================================================================================================================
// ! Create a deep (independent) copy of the data, such that changes made to the copy do not affect the original data to still test/re-run Part 1/2 with the correct INITIAL (and not modified) data
// - NOTE: Not using a deep copy will modify the original data after running Part 1/2, therefore no correct output will be calculated anymore.
let stones = [...fileData]; // Create a shallow copy of the data
let blink = 25;

// Change stones every time you blink
for (let i = 0; i < blink; i++) {
    stones = changeNumbers(stones);
}

// Calculate the number of stones after x blinks
let sumStones = stones.length;

// print(stones);

console.log("Total number of stones after 25 blinks (PART 1):", sumStones);
// ====================================================================================================================