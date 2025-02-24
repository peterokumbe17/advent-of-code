// *** [IMPORT LIBRARIES] ***
const fs = require('fs');
const path = require('path');

// *** [IMPORT DATA] ***
// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-6_input.txt");

// Open the file and read all data
let fileData = fs.readFileSync(filePath, "utf-8").trim();

const grid = fileData.split("\n").map(row => row.split(''));

// console.log(grid);
// ====================================================================================================================
// *** [Helper functions] ***
function nextPosIsObstacle(grid, direction, guardCurrentRow, guardCurrentCol) {
    if (direction === 'up') {
        // Check if the next position *upwards* is an obstacle
        return grid[guardCurrentRow - 1][guardCurrentCol] === '#';
    }

    if (direction === 'down') {
        return grid[guardCurrentRow + 1][guardCurrentCol] === '#';
    }

    if (direction === 'left') {
        return grid[guardCurrentRow][guardCurrentCol - 1] === '#';
    }

    if (direction === 'right') {
        return grid[guardCurrentRow][guardCurrentCol + 1] === '#';
    }

    return false;
}

function simulateWithObstruction(mapData, obstructionPosition) {
    /**
     * NOTE: Simulates the guard's movement with an obstruction added at a specific position.
     * 
     * Args:
     * - obstructionPosition (array[int, int]): The position where an obstruction is added.
     * 
     * Returns:
     * - bool: True if the guard gets stuck in a loop; False otherwise.
     */
    const directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]; //UDRL
    let currentDirection = 0;

    // Copy map data and add obstruction
    const modifiedMap = JSON.parse(JSON.stringify(mapData));
    modifiedMap[obstructionPosition[0]][obstructionPosition[1]] = '#';

    const visitedStates = new Set();

    // Find initial guard position
    for (let r = 0; r < mapData.length; r++) {
        for (let c = 0; c < mapData[0].length; c++) {
            if (mapData[r][c] === '^') {
                let guardPosition = [r, c];

                while (true) {
                    const state = `${guardPosition[0]},${guardPosition[1]},${currentDirection}`;

                    if (visitedStates.has(state)) {
                        return true; // Loop detected
                    }

                    visitedStates.add(state);

                    const nextRow = guardPosition[0] + directions[currentDirection][0]; // guard position +/- 1
                    const nextCol = guardPosition[1] + directions[currentDirection][1]; // guard position +/- 1

                    if (!(0 <= nextRow && nextRow < modifiedMap.length && 0 <= nextCol && nextCol < modifiedMap[0].length)) {
                        return false;
                    }

                    // IF an obstruction is found in the guard's path, then turn guard RIGHT (90 degrees)
                    if (modifiedMap[nextRow][nextCol] === '#') {
                        currentDirection = (currentDirection + 1) % 4; // E.g. curr_dir = 1 (+ 1) = 2 (% 4) = 2; 0 -> 1 -> 2 -> 3 -> 0 ...
                    } else {
                        guardPosition = [nextRow, nextCol];
                    }
                }
            }
        }
    }
}

function findLoopPositions(mapData) {
    /**
     * NOTE: Finds all possible positions where a new obstruction can be placed to trap the guard in a loop.
     * 
     * Args:
     * - mapData (array[array[str]]): The lab map as a 2D array of strings.
     * 
     * Returns:
     * - int: The number of valid positions where an obstruction can be placed.
     */
    const validPositions = new Set();

    for (let r = 0; r < mapData.length; r++) {
        for (let c = 0; c < mapData[0].length; c++) {
            if (mapData[r][c] === '.') {
                if (simulateWithObstruction(mapData, [r, c])) {
                    validPositions.add(`${r},${c}`);
                }
            }
        }
    }

    return validPositions.size;
}
// ====================================================================================================================
// *** [Part 1] ***
const part1Grid = JSON.parse(JSON.stringify(grid));
const nRows = part1Grid.length;
const nCols = part1Grid[0].length;
let guardCurrentRow = 0;
let guardCurrentCol = 0;
let direction = ''; // string var to store the name of the current direction of the guard
let steps = 0; // int var to store the total number of steps the guard takes in her patrol path.

// Determine initial position of guard
for (let rowIdx = 0; rowIdx < nRows; rowIdx++) {
    for (let colIdx = 0; colIdx < nCols; colIdx++) {
        if (part1Grid[rowIdx][colIdx] === '^') {
            // Set guard's initial position
            guardCurrentRow = rowIdx;
            guardCurrentCol = colIdx;
            direction = 'up';
        }
    }
}

// While the guard has NOT reached the END of any 1 of the 4 sides of the lab (grid)
while (0 < guardCurrentRow && guardCurrentRow < (nRows - 1) && 0 < guardCurrentCol && guardCurrentCol < (nCols - 1)) {
    // Mark current position as visited
    part1Grid[guardCurrentRow][guardCurrentCol] = 'X';
    // Check if the NEXT position (in relation to the CURRENT position) is an obstacle
    const hitObstacle = nextPosIsObstacle(part1Grid, direction, guardCurrentRow, guardCurrentCol);

    if (direction === 'up') {
        if (!hitObstacle) {
            guardCurrentRow -= 1; // Move guard 1 position [up]
        } else {
            // Turn guard right 90 degrees
            direction = 'right';
        }
    }
    // NOTE: 'else if' used to prevent previous if statement to continue to this (and remaining) if statements if not applicable
    else if (direction === 'down') {
        // Check if next position is an obstacle
        if (!hitObstacle) {
            guardCurrentRow += 1; // Move guard 1 position [down]
        } else {
            // Turn guard right 90 degrees
            direction = 'left';
        }
    }

    else if (direction === 'left') {
        // Check if next position is an obstacle
        if (!hitObstacle) {
            guardCurrentCol -= 1; // Move guard 1 position [left]
        } else {
            // Turn guard right 90 degrees
            direction = 'up';
        }
    }

    else if (direction === 'right') {
        // Check if next position is an obstacle
        if (!hitObstacle) {
            guardCurrentCol += 1; // Move guard 1 position [right]
        } else {
            // Turn guard right 90 degrees
            direction = 'down';
        }
    }

    // while loop BREAK condition
    if (guardCurrentRow === 0 || guardCurrentRow === (nRows - 1) || guardCurrentCol === 0 || guardCurrentCol === (nCols - 1)) {
        part1Grid[guardCurrentRow][guardCurrentCol] = 'X'; // Mark last visited position
        break;
    }
}

// Count the total number of DISTINCT visited areas in the grid
for (let row of part1Grid) {
    for (let col of row) {
        if (col === "X") {
            steps += 1;
        }
    }
}

console.log("Total number of distinct areas visited (PART 1):", steps);
// ====================================================================================================================
// *** [Part 2] ***
const part2Grid = JSON.parse(JSON.stringify(grid));
const numLoops = findLoopPositions(part2Grid);

console.log("Total number of loop positions found (PART 2):", numLoops);