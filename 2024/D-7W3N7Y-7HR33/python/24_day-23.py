# %% [markdown]
# # Day 23: LAN Party

# %% [markdown]
# ## Import libraries

# %%
import os
import copy
from collections import defaultdict
from itertools import combinations

# %% [markdown]
# ## Import data

# %%
# *** [IMPORT DATA] ***
# NOTE: In the given puzzle input:
# - Represents a map of a local network.
# - EACH line represents a SINGLE connection between 2 computers.
# - NOTE: Connections aren't directional (E.g. 'tc-kh' = 'kh-tc').
# ====================================================================================================================
# Get the current directory of this current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the data source file
file_path = os.path.join(current_dir, "../data", "24_day-23_input.txt")

# ! Open the file for reading mode (= default mode if the mode is not specified)
file = open(file_path, "r")

# Read all the data in the file
file_data = file.read().strip()

# Split by each line
file_data = file_data.split("\n")

# print(file_data)
# ====================================================================================================================

# %% [markdown]
# ## Helper functions

# %%
def find_inter_connected_computers(network_map):
    """
    Find all sets of three inter-connected computers in a network map.

    Args:
    - network_map (list): A list of connections between computers.

    Returns:
    - A list of sets of three inter-connected computers.
    """

    # Create a graph from the network map
    graph = defaultdict(list)

    for connection in network_map:
        computer1, computer2 = connection.split('-')
        graph[computer1].append(computer2)
        graph[computer2].append(computer1)

    # Find all sets of three inter-connected computers
    inter_connected_computers = set()

    for computer in graph:
        for pair in combinations(graph[computer], 2):
            if pair[0] in graph[pair[1]]:
                inter_connected_computers.add(tuple(sorted([computer, pair[0], pair[1]])))

    # Filter sets that contain at least one computer with a name that starts with 't'
    inter_connected_computers_with_t = [computers for computers in inter_connected_computers if any(computer.startswith('t') for computer in computers)]

    return inter_connected_computers_with_t

# %%
def bron_kerbosch(graph, clique=None, candidates=None, excluded=None):
    if clique is None:
        clique = []
    if candidates is None:
        candidates = set(graph.keys())
    if excluded is None:
        excluded = set()

    if not candidates and not excluded:
        return [clique]

    max_cliques = []

    for vertex in list(candidates):
        new_candidates = candidates & set(graph[vertex])
        new_excluded = excluded & set(graph[vertex])
        new_clique = clique + [vertex]
        new_cliques = bron_kerbosch(graph, new_clique, new_candidates, new_excluded)
        max_cliques.extend(new_cliques)
        candidates.remove(vertex)
        excluded.add(vertex)

    return max_cliques

def find_lan_party_password(network_map):
    """
    Find the password to get into the LAN party.

    Args:
    - network_map (list): A list of connections between computers.

    Returns:
    - The password to get into the LAN party.
    """
    # Create a graph from the network map
    graph = defaultdict(list)

    for connection in network_map:
        computer1, computer2 = connection.split('-')
        graph[computer1].append(computer2)
        graph[computer2].append(computer1)

    # Find the largest clique in the graph
    max_cliques = bron_kerbosch(graph)
    max_clique = max(max_cliques, key=len)

    # Sort the clique alphabetically and join with commas
    password = ','.join(sorted(max_clique))

    return password
# ====================================================================================================================

# %% [markdown]
# ## Part 1

# %%
# *** [PART 1] ***
# ! PROBLEM: As The Historians wander around a secure area at Easter Bunny HQ, you come across posters for a LAN party scheduled for today! Maybe you can find it; you connect to a nearby datalink port and download a map of the local network (your puzzle input). LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups of connected computers. Start by looking for sets of 3 computers where EACH computer in the set is CONNECTED to the other 2 computers.
# ! TODO: If the Chief Historian is here, and he's at the LAN party, it would be best to know that right away. You're pretty sure his computer's name starts with 't', so consider only sets of 3 computers where *at least* ONE computer's name starts with 't'. Find all the sets of 3 inter-connected computers. How many computers contain at least ONE computer with a name that starts with 't'?
# ====================================================================================================================
# ! Create a deep (independent) copy of the data, such that changes made to the copy do not affect the original data to still test/re-run in Part 1/2 with the correct INITIAL (and not modified) data
# - NOTE: Not using a deep copy will modify the original data after running Part 1/2, therefore incorrect output will be calculated.
networkMap = copy.deepcopy(file_data)

interConnectedComputers = find_inter_connected_computers(networkMap)

print("Total number of sets of 3 't' inter-connected computers (PART 1):", len(interConnectedComputers))
# ====================================================================================================================

# %% [markdown]
# ## Part 2

# %%
# *** [PART 2] ***
# ! PROBLEM: There are still way too many results to go through them all. You'll have to find the LAN party another way and go there yourself. Since it doesn't seem like any employees are around, you figure they must all be at the LAN party. If that's true, the LAN party will be the LARGEST set of computers that are ALL connected to each other. That is, for EACH computer at the LAN party, that computer will have a connection to EVERY other computer at the LAN party.
# ! TODO: The LAN party posters say that the PASSWORD to get into the LAN party = the name of EVERY computer at the LAN party, sorted alphabetically, then joined together with commas. (The people running the LAN party are clearly a bunch of nerds). Determine the password to get into the LAN party.
#====================================================================================================================
# ! Create a deep (independent) copy of the data, such that changes made to the copy do not affect the original data to still test/re-run Part in 1/2 with the correct INITIAL (and not modified) data
# - NOTE: Not using a deep copy will modify the original data after running Part 1/2, therefore incorrect output will be calculated.
networkMap = copy.deepcopy(file_data)

lanPassword = find_lan_party_password(networkMap)

print("Password to get into the LAN party (PART 2):", lanPassword)

# %%



