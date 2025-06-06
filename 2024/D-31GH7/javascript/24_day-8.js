// Import libraries
const fs = require('fs');
const path = require('path');
// const { default: defaultdict } = require('collections/default-dict');

// Helper function to calculate GCD
function gcd(a, b) {
    while (b !== 0) {
        let temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Import data
// *** [IMPORT DATA] ***
// NOTE: In the given puzzle input:
// - The grid map represents antennas.
// - EACH antenna is represented by a *letter* or *digit*.
// - The FREQUENCY of EACH antenna is different, based on whether the antenna is a: lowercase letter, uppercase letter or digit.
// - '#': Represents an antinode. 
// =====================================================================================================================
// Get the current directory of this current file
const current_dir = path.dirname(path.resolve(__filename));

// Construct the full path to the data source file
const file_path = path.join(current_dir, "../data", "24_day-8_input.txt");

// Read all the data in the file
const file_data = fs.readFileSync(file_path, 'utf8').trim();

// Separate data by line to create rows for grid
let grid = file_data.split("\n");

// Separate data in EACH row to represent EACH column
for (let i = 0; i < grid.length; i++) {
    grid[i] = grid[i].split('');
}

// Helper functions
function get_antinodes_p1(_grid) {
    let antennas = [];
    const numRows = _grid.length;
    const numCols = _grid[0].length;
    let antinodes_map = new Map();
    let freq_map = new Map();

    // Store antennas & their respective locations
    for (let x = 0; x < numRows; x++) {
        for (let y = 0; y < numCols; y++) {
            if (_grid[x][y] !== '.') { // If the grid block is NOT empty
                antennas.push([_grid[x][y], x, y]); // E.g. ('A', 4, 2)
            }
        }
    }

    /** Calculate the positions of antinodes */
    // Group antennas by frequency
    for (const [ant_freq, x, y] of antennas) {
        if (!freq_map.has(ant_freq)) {
            freq_map.set(ant_freq, []);
        }
        freq_map.get(ant_freq).push([x, y]); // E.g. '('A', [[0,1], [2,3], ...])'
    }

    // Calculate antinodes for EACH frequency
    for (const [ant_freq, positions] of freq_map.entries()) {
        for (let i = 0; i < positions.length; i++) {
            for (let j = i + 1; j < positions.length; j++) { // Compare every single antenna (i) against every other antenna of the same frequency (j)
                const [x1, y1] = positions[i];
                const [x2, y2] = positions[j];
                
                // Calculate the DISTANCE between antenna point #2 & #1 (same freq.)
                // - NOTE: Removed 'abs' in distance calculations so that the distances between 2 or more points in a straight line can be calculated and matched based on line slopes because antinodes can only exist above and/or below antennas on the SAME line from L to R or R to L
                const dx = x2 - x1; // Minus order is IMPORTANT
                const dy = y2 - y1;

                // Traverse through EACH non-empty point in the grid to check if it is an antinode of any 1 of the current 2 antennas with same freq.
                for (let xn = 0; xn < numRows; xn++) {
                    for (let yn = 0; yn < numCols; yn++) {
                        // NOTE: Follow the SAME minus order of calculating the SAME difference in distance (+/-x; +/-y) between different points in a line
                        // - E.g. For a striaght diagonal line going upwards from L to R with 4 points (2 antennas & 2 potential antinodes): xn - x2; x2 - x1; x1 - xn
                        // Distance between antenna #1 (top) and current block
                        const dx1 = x1 - xn; // Minus order is IMPORTANT
                        const dy1 = y1 - yn;
                        // ----------------
                        // Distance between current block and antenna #2 (bottom)
                        const dx2 = xn - x2; // Minus order is IMPORTANT
                        const dy2 = yn - y2;
                        
                        // IFF the distance between the current point & either of the 2 antennas = the distance between the current 2 antennas (dx1/2 == dx && dy1/2 == dy), then ADD the current non-empty point to the list of antinodes
                        if (dx1 === dx && dy1 === dy) {
                            if (!antinodes_map.has(ant_freq)) {
                                antinodes_map.set(ant_freq, []);
                            }
                            antinodes_map.get(ant_freq).push([xn, yn]);
                        }

                        if (dx2 === dx && dy2 === dy) {
                            if (!antinodes_map.has(ant_freq)) {
                                antinodes_map.set(ant_freq, []);
                            }
                            antinodes_map.get(ant_freq).push([xn, yn]);
                        }
                    }
                }
            }
        }
    }

    // Flatten the dictionary values into a single list
    let antinodes = [];
    for (const positions of antinodes_map.values()) {
        antinodes.push(...positions);
    }

    // Remove duplicate values from the list
    const antinodes_no_duplicates = [...new Set(antinodes.map(JSON.stringify))].map(JSON.parse);

    return antinodes_no_duplicates.length;
}

function get_antinodes_p1_alt(_grid) {
    let antennas = [];
    const rows = _grid.length;
    if (rows === 0) {
        return 0;
    }
    const cols = _grid[0].length;
    
    // Collect all antennas' positions and frequencies
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            const c = _grid[i][j];
            if (c !== '.') {
                antennas.push([i, j, c]);
            }
        }
    }
    
    let antinodes = new Set();
    let freq_map = new Map();
    
    for (const [i, j, c] of antennas) {
        if (!freq_map.has(c)) {
            freq_map.set(c, []);
        }
        freq_map.get(c).push([i, j]);
    }
    
    for (const [c, positions] of freq_map.entries()) {
        const n = positions.length;
        for (let i = 0; i < n; i++) {
            const [x1, y1] = positions[i];
            for (let j = i + 1; j < n; j++) {
                const [x2, y2] = positions[j];
                
                // Calculate the distance between the 2 antennas of same frequency
                const dx = x2 - x1;
                const dy = y2 - y1;
                
                // Antinode 1: (x1 - dx, y1 - dy)
                // - NOTE: Since (dx; dy) was calculated as (x2 - x1; y2 - y1), then this means that to find the 1st possible antinode (top or bottom), minus the already calculated distance (dx, dy) between the 2 antennas of same freq. from antenna (x1, y1)
                // - NOTE: [(A2 = (x2 + dx; y2 + dy)) > (D = (x2 - x1; y2 - y1)) > (A1 = (x1 - dx; y1 - dy))]
                const ant_x1 = x1 - dx;
                const ant_y1 = y1 - dy;
                if (0 <= ant_x1 && ant_x1 < rows && 0 <= ant_y1 && ant_y1 < cols) {
                    antinodes.add(JSON.stringify([ant_x1, ant_y1]));
                }

                // Antinode 2: (x2 + dx, y2 + dy)
                // - NOTE: Since (dx; dy) was calculated as (x2 - x1; y2 - y1), then this means that to find the 2nd possible antinode (top or bottom), add the already calculated distance (dx, dy) between the 2 antennas of same freq. to antenna (x2, y2)
                // - NOTE: [(A2 = (x2 + dx; y2 + dy)) > (D = (x2 - x1; y2 - y1)) > (A1 = (x1 - dx; y1 - dy))]
                const ant_x2 = x2 + dx;
                const ant_y2 = y2 + dy;
                if (0 <= ant_x2 && ant_x2 < rows && 0 <= ant_y2 && ant_y2 < cols) {
                    antinodes.add(JSON.stringify([ant_x2, ant_y2]));
                }
            }
        }
    }
    
    return antinodes.size;
}

function get_antinodes_p2(grid) {
    let antennas = [];
    const rows = grid.length;
    const cols = grid[0].length;

    if (rows === 0) {
        return 0;
    }
    
    // Collect all antennas' positions and frequencies
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            const c = grid[i][j];
            if (c !== '.') {
                antennas.push([i, j, c]);
            }
        }
    }
    
    let antinodes = new Set();
    let freq_map = new Map();
    
    for (const [i, j, c] of antennas) {
        if (!freq_map.has(c)) {
            freq_map.set(c, []);
        }
        freq_map.get(c).push([i, j]);
    }
    
    for (const [c, positions] of freq_map.entries()) {
        const n = positions.length;
        if (n < 2) {
            continue;
        }
        
        // For EACH position, check if it's in line with any two others (including itself? No)
        // But ANY position that is colinear with two others = an antinode.
        // So for EACH cell in the grid, check if it's colinear with at least two antennas of frequency 'c'.
        
        // But to optimize, we can first collect ALL possible lines defined by pairs of antennas of the same frequency.
        // Then, for EACH line, ALL points on that line = antinodes.
        let lines = new Set();  // To store unique lines represented in a way to avoid duplicates.
        
        // We'll represent a line by the tuple (A, B, C) where Ax + By + C = 0.
        // To avoid duplicates, we'll normalize the representation.
        for (let i = 0; i < n; i++) {
            const [x1, y1] = positions[i];

            for (let j = i + 1; j < n; j++) {
                const [x2, y2] = positions[j];

                // Calculate the line equation between (x1,y1) and (x2,y2)
                // - NOTE: Line equation: (y2 - y1)(x - x1) - (x2 - x1)(y - y1) = 0
                // - NOTE: Which can be rewritten as (y1 - y2)x + (x2 - x1)y + (x1*y2 - x2*y1) = 0
                let A = y1 - y2;
                let B = x2 - x1;
                let C = x1 * y2 - x2 * y1;
                
                // Normalize the line equation to avoid duplicate representations
                // Compute the greatest common divisor of A, B, and C
                let gcd_val = gcd(gcd(Math.abs(A), Math.abs(B)), Math.abs(C));

                if (gcd_val !== 0) {
                    A = Math.floor(A / gcd_val);
                    B = Math.floor(B / gcd_val);
                    C = Math.floor(C / gcd_val);
                }

                // Also, ensure the first non-zero coefficient is positive
                let first_non_zero = 0;

                if (A !== 0) {
                    first_non_zero = A;
                } else if (B !== 0) {
                    first_non_zero = B;
                } else {
                    first_non_zero = C;
                }
                if (first_non_zero < 0) {
                    A = -A;
                    B = -B;
                    C = -C;
                }
                
                lines.add(JSON.stringify([A, B, C]));
            }
        }
        
        // Now, for each line, mark all points on the line within grid bounds as antinodes
        for (const line of lines) {
            const [A, B, C] = JSON.parse(line);
            for (let x = 0; x < rows; x++) {
                for (let y = 0; y < cols; y++) {
                    if (A * x + B * y + C === 0) {
                        antinodes.add(JSON.stringify([x, y]));
                    }
                }
            }
        }
    }
    
    return antinodes.size;
}

// *** [PART 1] ***
// ! PROBLEM: The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas.
// - In particular, an *antinode* occurs at *any point* that is perfectly *in line* with TWO antennas of the SAME frequency - but ONLY when ONE of the antennas is TWICE as far away as the other. This means that for any PAIR of antennas with the SAME frequency, there are TWO antinodes, one on EITHER side of them.
// - Antennas with DIFFERENT frequencies DO NOT create antinodes; however, antinodes CAN occur at the SAME locations that CONTAIN antennas.
// - TODO: Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?
// ====================================================================================================================
// ! Create a deep (independent) copy of the grid data, such that changes made to the copy do not affect the original grid to still test/re-run Part 1 with the correct INITIAL (and not modified) grid
// - NOTE: Not using a deep copy will modify the original grid after running Part 1, therefore no correct output will be calculated anymore
const grid_p1 = JSON.parse(JSON.stringify(grid));
const numAntinodes_p1 = get_antinodes_p1(grid_p1);

console.log("Number of unique locations within grid with antinodes (PART 1):", numAntinodes_p1);

// *** [PART 2] ***
// ! PROBLEM: After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).
// - TODO: Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
//====================================================================================================================
// ! Create a deep (independent) copy of the grid data, such that changes made to the copy do not affect the original grid to still test/re-run Part 1 with the correct INITIAL (and not modified) grid
// - NOTE: Not using a deep copy will modify the original grid after running Part 1, therefore no correct output will be calculated anymore
const grid_p2 = JSON.parse(JSON.stringify(grid));
const numAntinodes_p2 = get_antinodes_p2(grid_p2);

console.log("Number of unique locations within grid with antinodes (PART 2):", numAntinodes_p2);