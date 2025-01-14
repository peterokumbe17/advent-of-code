// Day 10: Hoof It

// Import libraries
const fs = require("fs");
const path = require("path");

// Import data
// NOTE: In the given puzzle input:
// - Input represents a topographical map of a surrounding area.
// - The TM indicates the height at EACH position, using a scale from 0 (lowest) -> 9 (highest).

// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-10_input.txt");

// Open the file for reading mode (= default mode if the mode is not specified)
const file = fs.readFileSync(filePath, "utf8");

// Read all the data in the file
let fileData = file.trim();

// Helper functions
function findPaths(grid, trailheadPos) {
    // Find all *distinct* successful paths from a given trailhead (0) position in the grid.
    // NOTE: This function will return distinct paths that can reach all reachable 9s.
    // - Grid positions can be revisited in different paths, as long as each path has at least 1 different grid position in the path than other found paths
    // - This function does NOT return a list of the *first* distinct paths that can reach all reachable 9s. It returns ALL distinct paths that can reach all reachable 9s.
    // E.g. If a path 'path_1' reaches '9_1' and another distinct 'path_2' also reaches the same '9_1', then this function will return both 'path_1' and 'path_2' as distinct paths. BUT for the purpose of this challenge, we only need to count the *first* path that can reach a specific '9'.

    const rows = grid.length;
    const cols = grid[0].length;
    const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]; // right, left, down, up
    const visited = new Set();

    // Depth-first search
    function dfs(row, col, path) {
        if (visited.has(`${row},${col}`)) {
            return;
        }

        visited.add(`${row},${col}`);
        path.push([row, col]);

        if (grid[row][col] === 9) {
            paths.push([...path]);
        } else {
            for (const [dr, dc] of directions) {
                const nr = row + dr;
                const nc = col + dc;

                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] === grid[row][col] + 1) {
                    dfs(nr, nc, path);
                }
            }
        }

        visited.delete(`${row},${col}`);
        path.pop();
    }

    const paths = [];
    dfs(trailheadPos[0], trailheadPos[1], []);
    return paths;
}

function printPaths(paths, grid) {
    // Print the successful paths in a readable format.
    for (let i = 0; i < paths.length; i++) {
        console.log(`Path ${i + 1}:`);

        for (const [row, col] of paths[i]) {
            process.stdout.write(`(${row}, ${col}) = ${grid[row][col]} -> `);
        }

        console.log();
    }
}

// ====================================================================================================================

// Part 1
// PROBLEM: The reindeer is holding a book titled "Lava Island Hiking Guide". However, when you open the book, you discover that most of it seems to have been scorched by lava! As you're about to ask how you can help, the reindeer brings you a blank topographic map of the surrounding area (your puzzle input) and looks up at you excitedly. Perhaps you can help fill in the missing hiking trails?
// - Based on un-scorched scraps of the book, you determine that a good hiking trail is *as long as possible* and has an *even, gradual, uphill slope.
// - A hiking trail STARTS at height = 0; ENDS at height = 9; ALWAYS increases by a height of 1 at EACH step.
// - Hiking trails NEVER include diagonal steps - ONLY U-D-L-R movements.
// TODO: Calculate the sum total of the scores of ALL trailheads on the topographical map.
// - A trailhead is any position that STARTS one or more hiking trails => these positions will ALWAYS have height = 0.
// - A trailhead's score = the total number of reachable trails that end at height 9 (starting from the trailhead position, where height = 0).

let topMap = JSON.parse(JSON.stringify(fileData));
topMap = topMap.split('\n').filter(row => row).map(row => Array.from(row));
const numRows = topMap.length;
const numCols = numRows > 0 ? topMap[0].length : 0;
let sumScores = 0;

// Convert grid values from strings to integers
for (let i = 0; i < numRows; i++) {
    for (let j = 0; j < numCols; j++) {
        topMap[i][j] = parseInt(topMap[i][j]);
    }
}

// Calculate & sum scores of EACH trailhead found in the grid
for (let i = 0; i < numRows; i++) {
    for (let j = 0; j < numCols; j++) {
        if (topMap[i][j] === 0) { // Current position value = a trailhead
            const tHeadPos = [i, j];
            const distinctPaths = findPaths(topMap, tHeadPos);
            const reachablePaths = {};

            for (const path of distinctPaths) {
                if (path.length > 0) { // Ensure the list is not empty
                    const lastValue = path[path.length - 1]; // Get position of endtrail (9) in current path = the last element of the list

                    // If the key (lastValue) is NOT already in the dictionary, add the list to the dictionary.
                    if (!reachablePaths[lastValue]) {
                        reachablePaths[lastValue] = path;
                    }
                }
            }

            const reachablePathsList = Object.values(reachablePaths);
            // Calculate the score of the trailhead
            sumScores += reachablePathsList.length;
        }
    }
}

console.log("Total sum scores of all trailheads (PART 1):", sumScores);

// ====================================================================================================================

// Part 2
// PROBLEM: The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper. The paper describes a second way to measure a trailhead called its *rating*.
// - NOTE: A trailhead's rating is the number of *distinct hiking trails* which *begin at that trailhead*.
// TODO: Calculate the SUM of the *ratings* of ALL trailheads* in the grid.

let topMap2 = JSON.parse(JSON.stringify(fileData));
topMap2 = topMap2.split('\n').filter(row => row).map(row => Array.from(row));
const numRows2 = topMap2.length;
const numCols2 = numRows2 > 0 ? topMap2[0].length : 0;
let sumRatings = 0;

// Convert grid values from strings to integers
for (let i = 0; i < numRows2; i++) {
    for (let j = 0; j < numCols2; j++) {
        topMap2[i][j] = parseInt(topMap2[i][j]);
    }
}

// Calculate & sum ratings of EACH trailhead found in the grid
for (let i = 0; i < numRows2; i++) {
    for (let j = 0; j < numCols2; j++) {
        if (topMap2[i][j] === 0) { // Current position value = a trailhead
            const tHeadPos = [i, j];
            const distinctPaths = findPaths(topMap2, tHeadPos);

            // Calculate the score of the trailhead
            sumRatings += distinctPaths.length;
        }
    }
}

console.log("Total sum ratings of all trailheads (PART 2):", sumRatings);
