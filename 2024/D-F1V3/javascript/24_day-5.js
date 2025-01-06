// Day 5: Print Queue

const fs = require("fs");
const path = require("path");

// *** [IMPORT DATA] ***
// =====================================================================================================================

// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-5_input.txt");

// Open the file and read all data
let fileData = fs.readFileSync(filePath, "utf-8").trim();
// console.log(fileData)

// Split the data read from the file by the empty line encountered and store in an array list
fileData = fileData.split("\r\n"); // "\r\n" - js generates this delimiter after text in each line after reading in the data from the file

let found = 0; // bool var to check if the empty line has been encountered
let rules = []
let updates = []


for (let i = 0; i < fileData.length; i++) {
    if (fileData[i] == '') {
        found = 1
    }

    if (found == 0) {
        rules.push(fileData[i]) // ALL data AFTER the empty line = a rule
    }

    if (found == 1 && fileData[i] != '') { 
        updates.push(fileData[i]) // ALL data AFTER the empty line = an update of page numbers
    }
}

// let rules = fileData[0].split("\n");

for (let i = 0; i < rules.length; i++) {
    rules[i] = rules[i].split("|");
}

// console.log(updates)

// let updates = fileData[1].split("\n");

for (let j = 0; j < updates.length; j++) {
    updates[j] = updates[j].split(",");
}

// console.log(rules);
// console.log(rules.length);
// console.log(updates);
// console.log(updates.length);
// ====================================================================================================================

// Helper Functions
function isCorrectUpdate(rules, update) {
    let arrCheckUpdates = [];

    for (let rule of rules) {
        let leftPN = rule[0];
        let rightPN = rule[1];

        // Check IF the left page number (PN) of the CURRENT rule exists in the CURRENT update
        let leftPNIdx = update.includes(leftPN) ? update.indexOf(leftPN) : -1;
        let rightPNIdx = update.includes(rightPN) ? update.indexOf(rightPN) : -1;

        // Check IF the LHS page number comes BEFORE the RHS page number in the CURRENT update
        if (leftPNIdx === -1 || rightPNIdx === -1) {
            arrCheckUpdates.push(true);
        } else {
            if (leftPNIdx < rightPNIdx) {
                arrCheckUpdates.push(true);
            }
            if (leftPNIdx > rightPNIdx) {
                arrCheckUpdates.push(false);
            }
        }
    }

    // Check IF ALL rule checks pass for the list of page numbers in the CURRENT update
    if (!arrCheckUpdates.includes(false)) {
        return true;
    }

    return false;
}

function isIncorrectUpdate(rules, update) {
    let arrCheckUpdates = [];

    for (let rule of rules) {
        let leftPN = rule[0];
        let rightPN = rule[1];

        // Check IF the left page number (PN) of the CURRENT rule exists in the CURRENT update
        let leftPNIdx = update.includes(leftPN) ? update.indexOf(leftPN) : -1;
        let rightPNIdx = update.includes(rightPN) ? update.indexOf(rightPN) : -1;

        // Check IF the LHS page number comes BEFORE the RHS page number in the CURRENT update
        if (leftPNIdx === -1 || rightPNIdx === -1) {
            arrCheckUpdates.push(true);
        } else {
            if (leftPNIdx < rightPNIdx) {
                arrCheckUpdates.push(true);
            }
            if (leftPNIdx > rightPNIdx) {
                arrCheckUpdates.push(false);
            }
        }
    }

    // Get list of INCORRECT updates
    // NOTE: Check IF NOT all rule checks pass for the list of page numbers in the CURRENT update
    if (arrCheckUpdates.includes(false)) {
        return true;
    }

    return false;
}

// *** [PART 1] ***
// =====================================================================================================================
let arrValidUpdates = [];
let sumMiddlePNs = 0;

for (let update of updates) {
    if (isCorrectUpdate(rules, update)) {
        arrValidUpdates.push(update);
    }
}

// Get sum of all middle page numbers in the list of valid updates
for (let update of arrValidUpdates) {
    let middlePNIdx = Math.floor(update.length / 2);
    let middlePN = update[middlePNIdx];

    sumMiddlePNs += parseInt(middlePN);
}

console.log("Sum of all correct middle page numbers (PART 1):", sumMiddlePNs);
// ====================================================================================================================

// *** [PART 2] ***
// =====================================================================================================================
let arrInvalidUpdates = [];
arrValidUpdates = [];
sumMiddlePNs = 0;

for (let update of updates) {
    if (isIncorrectUpdate(rules, update)) {
        arrInvalidUpdates.push(update);
    }
}

// Correctly order the invalid updates
for (let update of arrInvalidUpdates) {
    // Generate permutations lazily
    const permute = (arr, prefix = []) => {
        if (arr.length === 0) {
            return [prefix];
        }
        return arr.flatMap((v, i) => permute(arr.slice(0, i).concat(arr.slice(i + 1)), prefix.concat(v)));
    };

    let allPerms = permute(update);

    for (let perm of allPerms) {
        if (isCorrectUpdate(rules, perm)) {
            let validUpdate = [...perm]; // Clone the valid permutation
            arrValidUpdates.push(validUpdate);
        }
    }
}

// Get sum of all middle page numbers in the new list of correctly ordered & now valid updates
for (let update of arrValidUpdates) {
    let middlePNIdx = Math.floor(update.length / 2);
    let middlePN = update[middlePNIdx];

    sumMiddlePNs += parseInt(middlePN);
}

console.log("Sum of all correct middle page numbers (PART 2):", sumMiddlePNs);
// =====================================================================================================================
