// Import libraries
const fs = require('fs');
const path = require('path');

// *** [IMPORT DATA] ***
const currentDir = __dirname;
const filePath = path.join(currentDir, '../data', '24_day-23_input.txt');

// Read all the data in the file
const fileData = fs.readFileSync(filePath, 'utf-8').trim().split('\n');
// ====================================================================================================================
// *** [HELPER FUNCTIONS] ***
function findInterConnectedComputers(networkMap) {
    const graph = {};

    // Create a graph from the network map
    for (const connection of networkMap) {
        const [computer1, computer2] = connection.split('-');

        if (!graph[computer1]) graph[computer1] = [];
        if (!graph[computer2]) graph[computer2] = [];
        graph[computer1].push(computer2);
        graph[computer2].push(computer1);
    }

    // Find all sets of three inter-connected computers
    const interConnectedComputers = new Set();

    for (const computer in graph) {
        const neighbors = graph[computer];

        for (let i = 0; i < neighbors.length; i++) {
            for (let j = i + 1; j < neighbors.length; j++) {
                const pair = [neighbors[i], neighbors[j]];
                if (graph[neighbors[i]].includes(neighbors[j])) {
                    interConnectedComputers.add(JSON.stringify([computer, ...pair].sort()));
                }
            }
        }
    }

    // Filter sets that contain at least one computer with a name that starts with 't'
    const interConnectedComputersWithT = [...interConnectedComputers].filter(computers => 
        JSON.parse(computers).some(computer => computer.startsWith('t'))
    );

    return interConnectedComputersWithT;
}

function bronKerbosch(graph, clique = [], candidates = new Set(Object.keys(graph)), excluded = new Set()) {
    if (candidates.size === 0 && excluded.size === 0) {
        return [clique];
    }

    const maxCliques = [];

    for (const vertex of Array.from(candidates)) {
        const newClique = [...clique, vertex];
        const newCandidates = new Set([...candidates].filter(v => graph[vertex].includes(v)));
        const newExcluded = new Set([...excluded].filter(v => graph[vertex].includes(v)));
        const newCliques = bronKerbosch(graph, newClique, newCandidates, newExcluded);
        maxCliques.push(...newCliques);
        candidates.delete(vertex);
        excluded.add(vertex);
    }

    return maxCliques;
}

function findLanPartyPassword(networkMap) {
    const graph = {};

    // Create a graph from the network map
    for (const connection of networkMap) {
        const [computer1, computer2] = connection.split('-');
        if (!graph[computer1]) graph[computer1] = [];
        if (!graph[computer2]) graph[computer2] = [];
        graph[computer1].push(computer2);
        graph[computer2].push(computer1);
    }

    // Find the largest clique in the graph
    const maxCliques = bronKerbosch(graph);
    const maxClique = maxCliques.reduce((a, b) => (b.length > a.length ? b : a), []);

    // Sort the clique alphabetically and join with commas
    const password = maxClique.sort().join(',');

    return password;
}
// ====================================================================================================================
// *** [PART 1] ***
const networkMapPart1 = [...fileData]; // Create a deep copy
const interConnectedComputers = findInterConnectedComputers(networkMapPart1);
console.log("Total number of sets of 3 't' inter-connected computers (PART 1):", interConnectedComputers.length);
// ====================================================================================================================
// *** [PART 2] ***
const networkMapPart2 = [...fileData]; // Create a deep copy
const lanPassword = findLanPartyPassword(networkMapPart2);
console.log("Password to get into the LAN party (PART 2):", lanPassword);