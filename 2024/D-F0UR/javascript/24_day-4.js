// Day 4: Ceres Search

const fs = require("fs");
const path = require("path");

// *** [IMPORT DATA] ***
// =====================================================================================================================

// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-4_input.txt");

// Open the file and read all data
let fileData = fs.readFileSync(filePath, "utf-8");

// Split the data read from the file by every new line and store in an array list
fileData = fileData.split("\n");

// =====================================================================================================================

// Helper Functions

function find_horizontal(grid, word) {
    // Finds horizontal matches
    let numMatches = 0;

    for (const row of grid) {
        // L2R search:
        // Use regex to find all occurrences of the word in the row
        const matches = row.match(new RegExp(`(?=${word})`, "g"));
        numMatches += matches ? matches.length : 0;
    }

    return numMatches;
}

function find_vertical(grid, word) {
    // Finds vertical matches
    const numRows = grid.length;
    const numCols = grid[0].length;
    let numMatches = 0;

    for (let colIndex = 0; colIndex < numCols; colIndex++) {
        let column = "";
        for (let row = 0; row < numRows; row++) {
            column += grid[row][colIndex];
        }

        // T2B search
        // Use regex to find all occurrences of the word in the column
        const matches = column.match(new RegExp(`(?=${word})`, "g"));
        numMatches += matches ? matches.length : 0;
    }

    return numMatches;
}

function find_word_in_diagonals(grid, word) {
    const rows = grid.length;
    const cols = grid[0].length;
    const diagonals = [];
    let numMatches = 0;

    // Extract primary diagonals (top-left to bottom-right)
    for (let d = 0; d < rows + cols - 1; d++) {
        const diagonal = [];
        for (let i = Math.max(0, d - cols + 1); i < Math.min(rows, d + 1); i++) {
            diagonal.push(grid[i][d - i]);
        }
        diagonals.push(diagonal.join(""));
    }

    // Extract anti-diagonals (bottom-left to top-right)
    for (let d = 0; d < rows + cols - 1; d++) {
        const diagonal = [];
        for (let i = Math.max(0, d - cols + 1); i < Math.min(rows, d + 1); i++) {
            diagonal.push(grid[rows - 1 - i][d - i]);
        }
        diagonals.push(diagonal.join(""));
    }

    // Search for the word in each diagonal
    for (const diagonal of diagonals) {
        const matches = diagonal.match(new RegExp(`(?=${word})`, "g"));
        numMatches += matches ? matches.length : 0;
    }

    return numMatches;
}

// Part 1

// Define the words to search for
const words = ["XMAS", "SAMX"];
let numMatches = 0;

for (const word of words) {
    numMatches += find_horizontal(fileData, word);
    numMatches += find_vertical(fileData, word);
    numMatches += find_word_in_diagonals(fileData, word);
}

console.log("Number of times that 'XMAS' appears (PART 1):", numMatches);

// Part 2

// Define grid dimensions
const grid = fileData;
const numCols = grid[0].length;
const numRows = grid.length;
numMatches = 0;

// Search grid
// NOTE: Only search for 'A' within inner layers of grid
for (let row = 1; row < numRows - 1; row++) {
    for (let col = 1; col < numCols - 1; col++) {
        if (grid[row][col] === "A") {
            const topLeft = grid[row - 1][col - 1];
            const topRight = grid[row - 1][col + 1];
            const bottomLeft = grid[row + 1][col - 1];
            const bottomRight = grid[row + 1][col + 1];

            // S-A-M x S-A-M
            if (topLeft === "S" && bottomRight === "M" && topRight === "S" && bottomLeft === "M") {
                numMatches += 1;
            }

            // M-A-S x M-A-S
            if (topLeft === "M" && bottomRight === "S" && topRight === "M" && bottomLeft === "S") {
                numMatches += 1;
            }

            // S-A-M x M-A-S
            if (topLeft === "S" && bottomRight === "M" && topRight === "M" && bottomLeft === "S") {
                numMatches += 1;
            }

            // M-A-S x S-A-M
            if (topLeft === "M" && bottomRight === "S" && topRight === "S" && bottomLeft === "M") {
                numMatches += 1;
            }
        }
    }
}

console.log("Number of times that 'XMAS' appears (PART 2):", numMatches);
