// Day 23: LAN Party

// Import libraries
const fs = require('fs'); // For file system operations
const path = require('path'); // For path operations
// const { default: Set } = require('collections/set'); // For set operations (if needed)

// Import data
// Get the current directory of this current file
const currentDir = __dirname;

// Construct the full path to the data source file
const filePath = path.join(currentDir, "../data", "24_day-23_input-test.txt");

// Open the file for reading mode
const fileData = fs.readFileSync(filePath, 'utf8').trim();

// Split by claw machines
const networkMap = fileData.split("\n");

// Helper functions

/**
 * Generate all combinations of a specific length from an array.
 *
 * @param {Array} array - The array to generate combinations from.
 * @param {number} length - The length of each combination.
 * @returns {Array} - An array of combinations, where each combination is an array.
 */
function combinations(array, length) {
    const result = [];

    function combine(start, combo) {
        if (combo.length === length) {
            result.push(combo);
            return;
        }

        for (let i = start; i < array.length; i++) {
            combine(i + 1, combo.concat(array[i]));
        }
    }

    combine(0, []);

    return result;
}

function findInterConnectedComputers(networkMap) {
    /**
     * Find all sets of three inter-connected computers in a network map.
     *
     * @param {Array} networkMap - A list of connections between computers.
     * @returns {Array} - A list of sets of three inter-connected computers.
     */

    // Create a graph from the network map
    const graph = {};

    networkMap.forEach(connection => {
        const [computer1, computer2] = connection.split('-');
        if (!graph[computer1]) graph[computer1] = [];
        if (!graph[computer2]) graph[computer2] = [];
        graph[computer1].push(computer2);
        graph[computer2].push(computer1);
    });

    // Find all sets of three inter-connected computers
    const interConnectedComputers = new Set();

    for (const computer in graph) {
        const pairs = combinations(graph[computer], 2);
        pairs.forEach(pair => {
            if (graph[pair[1]].includes(pair[0])) {
                interConnectedComputers.add([computer, pair[0], pair[1]].sort());
            }
        });
    }

    // Filter sets that contain at least one computer with a name that starts with 't'
    const interConnectedComputersWithT = [...interConnectedComputers].filter(computers => 
        computers.some(computer => computer.startsWith('t'))
    );

    return interConnectedComputersWithT;
}

function bronKerbosch(graph, clique = [], candidates = new Set(Object.keys(graph)), excluded = new Set()) {
    if (candidates.size === 0 && excluded.size === 0) {
        return [clique];
    }

    const maxCliques = [];

    candidates.forEach(vertex => {
        const newCandidates = new Set([...candidates].filter(v => graph[vertex].includes(v)));
        const newExcluded = new Set([...excluded].filter(v => graph[vertex].includes(v)));
        const newClique = [...clique, vertex];
        const newCliques = bronKerbosch(graph, newClique, newCandidates, newExcluded);
        maxCliques.push(...newCliques);
        candidates.delete(vertex);
        excluded.add(vertex);
    });

    return maxCliques;
}

function findLanPartyPassword(networkMap) {
    /**
     * Find the password to get into the LAN party.
     *
     * @param {Array} networkMap - A list of connections between computers.
     * @returns {String} - The password to get into the LAN party.
     */

    // Create a graph from the network map
    const graph = {};

    networkMap.forEach(connection => {
        const [computer1, computer2] = connection.split('-');
        if (!graph[computer1]) graph[computer1] = [];
        if (!graph[computer2]) graph[computer2] = [];
        graph[computer1].push(computer2);
        graph[computer2].push(computer1);
    });

    // Find the largest clique in the graph
    const maxCliques = bronKerbosch(graph);
    const maxClique = maxCliques.reduce((a, b) => a.length > b.length ? a : b);

    // Sort the clique alphabetically and join with commas
    const password = maxClique.sort().join(',');

    return password;
}

// Part 1
// Create a deep (independent) copy of the data
const networkMapPart1 = [...networkMap]; // Shallow copy is sufficient for strings

const interConnectedComputers = findInterConnectedComputers(networkMapPart1);

console.log("Total number of sets of 3 't' inter-connected computers (PART 1):", interConnectedComputers.length);

// Part 2
// Create a deep (independent) copy of the data
const networkMapPart2 = [...networkMap]; // Shallow copy is sufficient for strings

const lanPassword = findLanPartyPassword(networkMapPart2);

console.log("Password to get into the LAN party (PART 2):", lanPassword);