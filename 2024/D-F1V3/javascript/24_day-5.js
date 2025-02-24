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
// =====================================================================================================================

// Helper Functions
function isCorrectUpdate(_rules, _update) {
    const _arrCheckUpdates = [];

    for (const rule of _rules) {
        const _leftPN = rule[0];
        const _rightPN = rule[1];

        // Check IF the left page number (PN) of the CURRENT rule exists in the CURRENT update
        const _leftPN_idx = _update.includes(_leftPN) ? _update.indexOf(_leftPN) : -1;
        const _rightPN_idx = _update.includes(_rightPN) ? _update.indexOf(_rightPN) : -1;

        // Check IF the LHS page number comes BEFORE the RHS page number in the CURRENT update
        if (_leftPN_idx === -1 || _rightPN_idx === -1) {
            _arrCheckUpdates.push(true);
        } else {
            if (_leftPN_idx < _rightPN_idx) {
                _arrCheckUpdates.push(true);
            }
            if (_leftPN_idx > _rightPN_idx) {
                _arrCheckUpdates.push(false);
            }
        }
    }

    // Check IF ALL rule checks pass for the list of page numbers in the CURRENT update
    return !_arrCheckUpdates.includes(false);
}

function isIncorrectUpdate(_rules, _update) {
    const _arrCheckUpdates = [];

    for (const rule of _rules) {
        const _leftPN = rule[0];
        const _rightPN = rule[1];

        // Check IF the left page number (PN) of the CURRENT rule exists in the CURRENT update
        const _leftPN_idx = _update.includes(_leftPN) ? _update.indexOf(_leftPN) : -1;
        const _rightPN_idx = _update.includes(_rightPN) ? _update.indexOf(_rightPN) : -1;

        // Check IF the LHS page number comes BEFORE the RHS page number in the CURRENT update
        if (_leftPN_idx === -1 || _rightPN_idx === -1) {
            _arrCheckUpdates.push(true);
        } else {
            if (_leftPN_idx < _rightPN_idx) {
                _arrCheckUpdates.push(true);
            }
            if (_leftPN_idx > _rightPN_idx) {
                _arrCheckUpdates.push(false);
            }
        }
    }

    // Get list of INCORRECT updates
    // NOTE: Check IF NOT all rule checks pass for the list of page numbers in the CURRENT update
    return _arrCheckUpdates.includes(false);
}

// *** [PART 1] ***
// =====================================================================================================================
let arrValidUpdates = [];
let sumMiddlePNs = 0;

for (const update of updates) {
    if (isCorrectUpdate(rules, update)) {
        arrValidUpdates.push(update);
    }
}

// Get sum of all middle page numbers in the list of valid updates
for (const update of arrValidUpdates) {
    const middlePN_idx = Math.floor(update.length / 2);
    const middlePN = update[middlePN_idx];

    sumMiddlePNs += parseInt(middlePN, 10);
}

console.log("Sum of all correct middle page numbers (PART 1):", sumMiddlePNs);
// =====================================================================================================================

// *** [PART 2] ***
// =====================================================================================================================
let arrInvalidUpdates = [];
arrValidUpdates = [];
sumMiddlePNs = 0;

// Create a deep (independent) copy of the updates array
const updatesCopy = JSON.parse(JSON.stringify(updates));

for (const update of updatesCopy) {
    if (isIncorrectUpdate(rules, update)) {
        arrInvalidUpdates.push(update);
    }
}

// Correctly order the invalid updates
for (const update of arrInvalidUpdates) {
    const arrCheckUpdates = [];
    let ruleCounter = 0;

    while (ruleCounter < rules.length) {
        const rule = rules[ruleCounter];
        const leftPN = rule[0];
        const rightPN = rule[1];

        // Check IF the left page number (PN) of the CURRENT rule exists in the CURRENT update
        const leftPN_idx = update.includes(leftPN) ? update.indexOf(leftPN) : -1;
        const rightPN_idx = update.includes(rightPN) ? update.indexOf(rightPN) : -1;

        // Check IF the LHS page number comes BEFORE the RHS page number in the CURRENT update
        if (leftPN_idx === -1 || rightPN_idx === -1) {
            arrCheckUpdates.push(true);
        } else {
            if (leftPN_idx < rightPN_idx) {
                arrCheckUpdates.push(true);
            }
            if (leftPN_idx > rightPN_idx) {
                arrCheckUpdates.push(false);

                // Swap the positions of these 2 values in the array to make them pass the rule check
                const temp = update[leftPN_idx];
                update[leftPN_idx] = update[rightPN_idx];
                update[rightPN_idx] = temp;

                // Reset the rule counter to see if the newly ordered list will pass ALL rule checks
                ruleCounter = 0;
                arrCheckUpdates.length = 0;
            }
        }

        ruleCounter++;
    }

    // Get list of newly CORRECTED updates
    if (!arrCheckUpdates.includes(false)) {
        arrValidUpdates.push(update);
    }
}

// Get sum of all middle page numbers in the new list of correctly ordered updates
for (const update of arrValidUpdates) {
    const middlePN_idx = Math.floor(update.length / 2);
    const middlePN = update[middlePN_idx];

    sumMiddlePNs += parseInt(middlePN, 10);
}

console.log("Sum of all correct middle page numbers (PART 2):", sumMiddlePNs);
// =====================================================================================================================
