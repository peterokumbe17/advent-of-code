// Day 2: Red-Nosed Reports

const fs = require('fs');
const path = require('path');

// *** [IMPORT DATA] ***
// =====================================================================================================================

// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-2_input.txt");

// Open the file and read the data
const fileData = fs.readFileSync(filePath, "utf-8");

// Split the data read from the file by every new line
let arrFileData = fileData.trim().split('\n');

// =====================================================================================================================

// Helper Functions
// =====================================================================================================================
function checkSafeReport(arrLevels) {
    // Check if the list of level numbers are strictly INCREASING with a difference of at least 1 and at most 3
    const validIncrease = arrLevels.every((_, i) =>
        i === arrLevels.length - 1 || 
        (arrLevels[i] < arrLevels[i + 1] && (1 <= arrLevels[i + 1] - arrLevels[i] && arrLevels[i + 1] - arrLevels[i] <= 3))
    );

    // Check if the list of level numbers are strictly DECREASING with a difference of at least 1 and at most 3
    const validDecrease = arrLevels.every((_, i) =>
        i === arrLevels.length - 1 || 
        (arrLevels[i] > arrLevels[i + 1] && (1 <= arrLevels[i] - arrLevels[i + 1] && arrLevels[i] - arrLevels[i + 1] <= 3))
    );

    // Safe report = all level numbers either strictly increasing OR decreasing
    return validIncrease || validDecrease;
}

function problemDampener(arrLevels) {
    // Check if the current report becomes safe if any one level is removed
    for (let i = 0; i < arrLevels.length; i++) {
        const modifiedArrLevels = arrLevels.slice(0, i).concat(arrLevels.slice(i + 1)); // Remove the i-th element
        if (checkSafeReport(modifiedArrLevels)) {
            return true;
        }
    }
    return false;
}
// =====================================================================================================================

// *** [PART 1] ***
// =====================================================================================================================

let totalSafeReports = 0;
let arrSafeReportsCheck = [];

// Process each report
arrFileData.forEach(report => {
    // Split the report string line of numbers (levels) into an array of integers
    let arrLevels = report.split(' ').map(Number);

    // Check if the current report is safe
    const isSafeReport = checkSafeReport(arrLevels);

    if (isSafeReport) {
        arrSafeReportsCheck.push(true);
    } else {
        arrSafeReportsCheck.push(false);
    }
});

// Count the total number of safe reports
totalSafeReports = arrSafeReportsCheck.filter(Boolean).length;

console.log("Total safe reports (PART 1):", totalSafeReports);
// =====================================================================================================================

// *** [PART 2] ***
// =====================================================================================================================

totalSafeReports = 0;
arrSafeReportsCheck = [];

// Process each report
arrFileData.forEach(report => {
    // Split the report string line of numbers (levels) into an array of integers
    let arrLevels = report.split(' ').map(Number);

    // Check if the current report is safe after applying the Problem Dampener
    const isSafeReport = problemDampener(arrLevels);

    if (isSafeReport) {
        arrSafeReportsCheck.push(true);
    } else {
        arrSafeReportsCheck.push(false);
    }
});

// Count the total number of safe reports
totalSafeReports = arrSafeReportsCheck.filter(Boolean).length;

console.log("Total safe reports (PART 2):", totalSafeReports);