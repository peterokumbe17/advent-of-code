// Day 1: Historian Hysteria

// Import required modules
const fs = require('fs');
const path = require('path');

// *** [IMPORT DATA] ***
// =====================================================================================================================

// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-1_input.txt");

// Open the file for reading mode
const fileData = fs.readFileSync(filePath, "utf-8");

// Initialize arrays to store numbers in left and right columns
let arrLColumn = []; // Array to store list of numbers in left column of text file
let arrRColumn = []; // Array to store list of numbers in right column of text file

// Read through each line in the text file
const lines = fileData.split("\n");
lines.forEach(line => {
    //console.log(line)
    const [num1, num2] = line.trim().split("   "); // Split each line by 3x space (as in textfile) and convert to integers
    arrLColumn.push(num1);
    arrRColumn.push(num2);
});

// Sort the arrays
arrLColumn.sort((a, b) => a - b);
arrRColumn.sort((a, b) => a - b);

// Output the sorted arrays
// console.log("Column 1 (L):", arrLColumn);
// console.log("Column 2 (R):", arrRColumn);
// =====================================================================================================================

// *** [PART 1] ***
// =====================================================================================================================

// Initialize variables for calculating total distance
let totalDistance = 0; // Total distance between all pairings
let arrPairDistances = []; // Array to store distances between each pairing

// Calculate distance between each pairing
arrLColumn.forEach((lNum, index) => {
    const rNum = arrRColumn[index];
    const distance = Math.abs(lNum - rNum); // Calculate absolute difference
    arrPairDistances.push(distance);
});

// Calculate total distance between all pairings
totalDistance = arrPairDistances.reduce((sum, dist) => sum + dist, 0);

// console.log("Pair distances:", arrPairDistances);
console.log("Total distance (PART 1):", totalDistance);
// =====================================================================================================================

// *** [PART 2] ***
// =====================================================================================================================

// Count the occurrences of each number in the right column
const counter = arrRColumn.reduce((acc, num) => {
    acc[num] = (acc[num] || 0) + 1;
    return acc;
}, {});

// Initialize variables for calculating total similarity score
let totalSimilarityScore = 0; // Total similarity score
let arrLColumnSimilarityScores = []; // Array to store similarity scores for each number in the left column

// Calculate similarity scores for each number in the left column
arrLColumn.forEach(num => {
    const similarityScore = num * (counter[num] || 0); // Multiply number by its count in the right column
    arrLColumnSimilarityScores.push(similarityScore);
});

// Calculate total similarity score
totalSimilarityScore = arrLColumnSimilarityScores.reduce((sum, score) => sum + score, 0);

// console.log("Similarity scores:", arrLColumnSimilarityScores);
console.log("Total similarity score (PART 2):", totalSimilarityScore);
