// Day 3: Mull It Over

const fs = require('fs');
const path = require('path');

// *** [IMPORT DATA] ***
// =====================================================================================================================

// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-3_input.txt");

// Read all the data in the file
const fileData = fs.readFileSync(filePath, "utf-8");

// =====================================================================================================================

// Helper functions
function mul(X, Y) {
    return X * Y;
}
// =====================================================================================================================

// *** [PART 1] ***
// =====================================================================================================================
// Regular expression to match and capture 'mul(X,Y)' with X and Y as groups
const regexMul = /mul\((\d{1,3}),(\d{1,3})\)/g;

let sumResults = 0;

// Find all matches in the string
const arrMatches = [...fileData.matchAll(regexMul)];
// console.log(arrMatches)

// Call func 'mul(X,Y)' for each match and store the results
const arrResults = arrMatches.map(match => mul(parseInt(match[1], 10), parseInt(match[2], 10)));

sumResults += arrResults.reduce((sum, result) => sum + result, 0);

console.log("Multiplication result (PART 1):", sumResults);

// =====================================================================================================================

// *** [PART 2] ***
// ! PROBLEM: As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact.
// - If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.
// - TODO: There are two new instructions you'll need to handle:
//   - 'do()': Enables future 'mul()' instructions.
//   - 'don't()': Disables future 'mul()' instructions.
//   - NOTE: Only the most recent 'do()' or 'don't()' instruction applies. At the beginning of the program, all valid 'mul()' instructions are enabled.
// ---------------------------------------------------------------------------------------------------------------------

// Regular expression to match occurrences of ALL 'mul(X,Y)' in a string
const regexMul2 = /mul\(\d{1,3},\d{1,3}\)/; // Matches 'mul(' > followed by 1-3 digits > ',' > and 1-3 digits > then ')'
const regexXYGroup = /mul\((\d{1,3}),(\d{1,3})\)/; // Captures X and Y as groups: E.g. '(X, Y)'
const regexControls = /don't\(\)|do\(\)/; // Matches "don't()" or "do()"

let flag = true; // Boolean variable to enable or disable future 'mul()' instructions
let pos = 0; // Integer variable to store the index position of the current character in the string
let arrMatches2 = []; // Array variable to store all valid captured 'mul(X,Y)' occurrences

// ! Find all matches in the string
// While the end of the string has NOT been reached
while (pos < fileData.length) {
    // Search for the next occurrence of "don't()", "do()", or 'mul(X,Y)'
    const match = fileData.slice(pos).match(new RegExp(`${regexControls.source}|${regexMul2.source}`));

    // IF no matches found, then exit the loop
    if (!match) {
        break;
    }

    // Get the matched text and its position
    const matchedText = match[0];

    // Move the position to after the current match
    pos += fileData.slice(pos).indexOf(matchedText) + matchedText.length;

    // Update flag based on control patterns
    if (matchedText === "don't()") {
        flag = false;
    } else if (matchedText === "do()") {
        flag = true;
    } else if (flag === true && regexMul2.test(matchedText)) {
        // Capture 'mul(X,Y)' IFF flag == True
        arrMatches2.push(matchedText);
    }
}

//console.log(arrMatches2);

// Parse X and Y from 'mul(X,Y)' and store as pairs
arrMatches2 = arrMatches2.map(item => {
    const match = regexXYGroup.exec(item);
    return [parseInt(match[1], 10), parseInt(match[2], 10)];
});

//console.log(arrMatches2)

// Call function 'mul(X,Y)' for each match and store the results
const arrResults2 = arrMatches2.map(([ x, y ]) => mul(x, y));

// console.log(arrResults2)

// Sum the results of all multiplications
const sumResults2 = arrResults2.reduce((sum, num) => sum + num, 0);

console.log("Multiplication result (PART 2):", sumResults2);
