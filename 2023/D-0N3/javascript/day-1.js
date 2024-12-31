const fs = require('fs');
const path = require('path');

// Get the current directory of this file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "23_day-1_input.txt");

// Open the data file for reading
const fileData = fs.readFileSync(filePath, 'utf-8');

// Read all the data in the file and split by new lines
let arrFileData = fileData.split('\n');

// Remove trailing spaces from each line
arrFileData = arrFileData.map(line => line.trim());

console.log(arrFileData);
console.log(arrFileData.length);

// *** [PART 1] ***
let arrCalibrationValues = []; // Array to store calibration values

// Process each line in arrFileData
arrFileData.forEach(line => {
    // Extract all digits from the line
    const lineDigits = line.match(/\d/g);

    if (lineDigits) {
        // Combine the *first* and *last* digits to create a calibration value
        const calibrationValue = lineDigits[0] + lineDigits[lineDigits.length - 1];
        arrCalibrationValues.push(calibrationValue);
    }
});

console.log('Calibration values (Part 1):', arrCalibrationValues);

// Calculate the sum of all calibration values
let totalValue = 0;
arrCalibrationValues.forEach(digit => {
    totalValue += parseInt(digit, 10);
});

console.log('Sum of calibration values (Part 1):', totalValue);

// *** [PART 2] ***
arrCalibrationValues = []; // Reset calibration values
const numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'];

arrFileData.forEach((line, counter) => {
    let calibrationValue = '';
    let lineDigits = line.match(/\d/g) || [];
    let lineWordDigits = [];

    // EDGE CASE HINT: Cater for edge cases such as 'xxxseveninexxx' = '79'
    // - Traverse through the current string line, then find EVERY occurrence of a word digit in the current line's
    //   string and store EACH found word digit in an array list ('lineWordDigits')
    for (let i = 0; i < line.length; i++) {
        // IF 'one' exists anywhere between the ith and 'i + wordDigit.length'th indexed char of the current string line
        numbers.forEach(wordDigit => {
            if (line.substring(i, i + wordDigit.length).includes(wordDigit)) {
                lineWordDigits.push(wordDigit);
            }
        });
    }

    // console.log(lineWordDigits);

    // if (counter === 48) {
    //     console.log(lineDigits);
    //     console.log(lineWordDigits);
    // }

    // Determine the first and last digits
    let firstDigitIndex = lineDigits.length > 0 ? line.indexOf(lineDigits[0]) : -1;
    let firstWordDigitIndex = lineWordDigits.length > 0 ? line.indexOf(lineWordDigits[0]) : -1;
    let lastDigitIndex = lineDigits.length > 0 ? line.lastIndexOf(lineDigits[lineDigits.length - 1]) : -1;
    let lastWordDigitIndex = lineWordDigits.length > 0 ? line.lastIndexOf(lineWordDigits[lineWordDigits.length - 1]) : -1;

    if (lineDigits.length === 1 && lineWordDigits.length === 1) {
        if (firstDigitIndex < firstWordDigitIndex) {
            calibrationValue = lineDigits[0] + lineWordDigits[0];
        } else {
            calibrationValue = lineWordDigits[0] + lineDigits[0];
        }
    } else if (lineDigits.length === 1 && lineWordDigits.length === 0) {
        calibrationValue = lineDigits[0] + lineDigits[0];
    } else if (lineWordDigits.length === 1 && lineDigits.length === 0) {
        calibrationValue = lineWordDigits[0] + lineWordDigits[0];
    } else {
        if (firstDigitIndex !== -1 && firstWordDigitIndex === -1) {
            calibrationValue = lineDigits[0];
        } else if (firstWordDigitIndex !== -1 && firstDigitIndex === -1) {
            calibrationValue = lineWordDigits[0];
        } else if (firstDigitIndex !== -1 && firstWordDigitIndex !== -1) {
            calibrationValue = firstDigitIndex < firstWordDigitIndex ? lineDigits[0] : lineWordDigits[0];
        }

        if (lastDigitIndex !== -1 && lastWordDigitIndex === -1) {
            calibrationValue += lineDigits[lineDigits.length - 1];
        } else if (lastWordDigitIndex !== -1 && lastDigitIndex === -1) {
            calibrationValue += lineWordDigits[lineWordDigits.length - 1];
        } else if (lastDigitIndex !== -1 && lastWordDigitIndex !== -1) {
            calibrationValue += lastDigitIndex > lastWordDigitIndex
                ? lineDigits[lineDigits.length - 1]
                : lineWordDigits[lineWordDigits.length - 1];
        }
    }

    arrCalibrationValues.push(calibrationValue);
});

console.log('Calibration values (Part 2):', arrCalibrationValues);

// Replace word-based digits with numeric equivalents
let arrDigitCalibrationValues = arrCalibrationValues.map(cValue => {
    numbers.forEach((word, index) => {
        cValue = cValue.replace(new RegExp(word, 'g'), (index + 1).toString());
    });
    return cValue;
});

console.log('DIGIT Calibration values:', arrDigitCalibrationValues);

// Calculate the sum of all calibration values
totalValue = arrDigitCalibrationValues.reduce((sum, digit) => sum + parseInt(digit, 10), 0);

console.log('Sum of calibration values (Part 2):', totalValue);
