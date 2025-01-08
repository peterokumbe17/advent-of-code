// *** Day 7: Bridge Repair ***

// *** [IMPORT LIBRARIES] ***
const fs = require("fs");
const path = require("path");

// *** [IMPORT DATA] ***
// NOTE: In the given puzzle input:
// - EACH line represents a SINGLE equation.
// - Test values appear BEFORE the colon on EACH line.
// =====================================================================================================================

// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-7_input.txt");

// Open the file and read all data
let fileData = fs.readFileSync(filePath, "utf-8");

// Separate data line by line
fileData = fileData.trim().split("\n");

// For EACH line, separate test values from equations
fileData = fileData.map(line => line.split(":"));

// For EACH line, separate equation numbers
fileData = fileData.map(line => {
    line[1] = line[1].trim().split(" ");

    return line;
});
// =====================================================================================================================
// Helper function to generate all combinations of operators
function generateCombinations(operators, length) {
    if (length === 0) return [[]];

    let smallerCombinations = generateCombinations(operators, length - 1);
    let combinations = [];

    for (let comb of smallerCombinations) 
    {
        for (let op of operators) 
        {
            combinations.push([...comb, op]);
        }
    }

    return combinations;
}  

// Helper function to evaluate an expression with given numbers and operators
function evaluateExpression(numbers, operators) {
    let result = numbers[0]; // First number in the list of equation numbers

    for (let i = 0; i < operators.length; i++) 
    {
        if (operators[i] === "+") {
            result += numbers[i + 1];
        } 
        else if (operators[i] === "*") {
            result *= numbers[i + 1];
        }
    }

    return result;
}

// Helper function to evaluate an expression with concatenation (||) included
function evaluateExpressionConcat(numbers, operators) {
    let result = numbers[0]; // First number in the list of equation numbers

    for (let i = 0; i < operators.length; i++) 
    {
        if (operators[i] === "+") {
            result += numbers[i + 1];
        } 
        else if (operators[i] === "*") {
            result *= numbers[i + 1];
        } 
        else if (operators[i] === "|") {
            let concatenatedNum = String(result) + String(numbers[i + 1]);
            result = parseInt(concatenatedNum, 10);
        }
    }

    return result;
}
// =====================================================================================================================
// *** [PART 1] ***
// ! PROBLEM: Some young elephants stole all the operators from the calibration equations!
// - Determine which numbers can be combined with operators ('+' and '*') to produce the target value.
// - Calculate the total calibration result (sum of valid targets).
// =====================================================================================================================

// Create a deep (independent) copy of the data
let equations = JSON.parse(JSON.stringify(fileData));
let arrValidTargets = [];

// Find and print the equations that match the target value
for (let equation of equations) 
{
    let target = parseInt(equation[0]);
    let numbers = equation[1].map(num => parseInt(num));

    // Generate all operator combinations
    let numOperators = numbers.length - 1;
    let operatorCombinations = generateCombinations(["+", "*"], numOperators);

    // Check each operator combination
    for (let operators of operatorCombinations) 
    {
        if (evaluateExpression(numbers, operators) === target) {
            arrValidTargets.push(target);
            break; // Break after finding the first valid target
        }
    }
}

let totalCalibrationValue = arrValidTargets.reduce((a, b) => a + b, 0);

console.log("Total calibration result (PART 1):", totalCalibrationValue);
// =====================================================================================================================
// *** [PART 2] ***
// ! PROBLEM: Add a third operator (||) to the equation to find additional valid targets.
// =====================================================================================================================

// Create a deep (independent) copy of the data
let part2Equations = JSON.parse(JSON.stringify(fileData));
let part2ArrValidTargets = [];

// Find and print the equations that match the target value
for (let equation of part2Equations) 
{
    let target = parseInt(equation[0]);
    let numbers = equation[1].map(num => parseInt(num));

    // Generate all operator combinations
    let numOperators = numbers.length - 1;
    let operatorCombinations = generateCombinations(["+", "|", "*"], numOperators);

    // Check each operator combination
    for (let operators of operatorCombinations) 
    {
        if (evaluateExpressionConcat(numbers, operators) === target) {
            part2ArrValidTargets.push(target);
            break; // Break after finding the first valid target
        }
    }
}

let part2TotalCalibrationValue = part2ArrValidTargets.reduce((a, b) => a + b, 0);

console.log("Total calibration result (PART 2):", part2TotalCalibrationValue);