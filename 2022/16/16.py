from collections import deque, defaultdict
import heapq

graph = {}
flows = {}

data = open('2022/16/test.txt').read().split('\n')
for line in data:
    node_str, edge_str = line.split('; ')
    node, flow = node_str.replace('Valve ','').replace(' has flow rate=',',').split(',')
    flows[node] = int(flow)
    graph[node] = edge_str.replace('tunnels lead to valves ','').replace('tunnel leads to valve ','').split(', ')

def condense_graph(graph, flow_values, start_node):
    """
    Condenses the graph to only nodes with flow > 0 and the starting node.
    
    graph: dict, adjacency list of the graph {node: [neighbors]}
    flow_values: dict, flow value of each node {node: flow_value}
    start_node: str, the starting node in the graph
    """
    # Filter nodes with flow > 0 or the starting node
    relevant_nodes = {node for node, flow in flow_values.items() if flow > 0 or node == start_node}

    # Helper function: Compute shortest paths using Dijkstra's algorithm
    def dijkstra(start):
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        heap = [(0, start)]  # (distance, node)
        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_distance > distances[current_node]:
                continue
            for neighbor in graph[current_node]:
                distance = current_distance + 1  # All edges have weight 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))
        return distances

    # Compute shortest distances between all relevant nodes
    condensed_distances = defaultdict(dict)
    for node in relevant_nodes:
        shortest_paths = dijkstra(node)
        for target in relevant_nodes:
            condensed_distances[node][target] = shortest_paths[target]

    condensed_flow_values = {node: flow for node, flow in flow_values.items() if node in relevant_nodes}
    return condensed_distances, condensed_flow_values

def best_flow(flow_values, distances, start_node, max_steps):
    """
    Maximizes cumulative flow with pruning and priorities.
    
    graph: dict, adjacency list of the graph {node: [neighbors]}
    flow_values: dict, flow value of each node {node: flow_value}
    distances: dict, precomputed distances between all pairs of nodes {node1: {node2: dist}}
    start_node: str, starting node in the graph
    max_steps: int, maximum number of steps allowed
    """
    best_cumulative_flow = 0
    memo = {}

    def upper_bound(remaining_steps, activated_nodes):
        # Calculate the maximum possible flow from unactivated nodes
        unactivated = [
            flow_values[node] for node in flow_values if node not in activated_nodes
        ]
        unactivated.sort(reverse=True)
        potential_flow = 0
        for flow in unactivated:
            if remaining_steps <= 1:
                break
            potential_flow += flow * (remaining_steps - 1)
            remaining_steps -= 1
        return potential_flow

    def backtrack(current_node, remaining_steps, activated_nodes, cumulative_flow):
        nonlocal best_cumulative_flow

        # Memoization state
        state = (current_node, remaining_steps, frozenset(activated_nodes))
        if state in memo and memo[state] >= cumulative_flow:
            return
        memo[state] = cumulative_flow

        # Update the best cumulative flow
        best_cumulative_flow = max(best_cumulative_flow, cumulative_flow)

        # Prune if the upper bound cannot beat the best solution
        if cumulative_flow + upper_bound(remaining_steps, activated_nodes) <= best_cumulative_flow:
            return

        # Priority calculation: potential flow for activating or moving to each unactivated node
        candidates = []
        for node in flow_values:
            if node not in activated_nodes:
                dist = distances[current_node][node]
                if remaining_steps > dist + 1:  # Only consider nodes reachable within remaining steps
                    potential_flow = flow_values[node] * (remaining_steps - (dist + 1))
                    candidates.append((node, potential_flow, dist))

        # Greedy choice: sort candidates by potential_flow descending
        candidates.sort(key=lambda x: x[1], reverse=True)

        # Process the candidates in order of their priority
        for node, _, dist in candidates:
            if node == current_node:  # Activate the current node
                activated_nodes.add(current_node)
                backtrack(
                    current_node,
                    remaining_steps - 1,
                    activated_nodes,
                    cumulative_flow + flow_values[current_node] * (remaining_steps - 1)
                )
                activated_nodes.remove(current_node)  # Backtrack
            else:  # Move to another node
                backtrack(
                    node,
                    remaining_steps - dist,
                    activated_nodes,
                    cumulative_flow
                )

    # Start the backtracking process
    backtrack(start_node, max_steps, set(), 0)
    return best_cumulative_flow

def best_flow_two_agents(flow_values, distances, start_node, max_steps):
    """
    Optimized function for maximizing cumulative flow with two agents using memoization.
    
    flow_values: dict, flow value of each node {node: flow_value}
    distances: dict, precomputed distances between all pairs of nodes {node1: {node2: dist}}
    start_node: str, starting node in the graph
    max_steps: int, maximum number of steps allowed for each agent
    """
    best_cumulative_flow = 0
    memo = {}

    def upper_bound(remaining_steps1, remaining_steps2, activated_nodes):
        # Calculate the maximum possible flow from unactivated nodes
        unactivated = [
            flow_values[node] for node in flow_values if node not in activated_nodes
        ]
        unactivated.sort(reverse=True)
        potential_flow = 0
        steps = max(remaining_steps1, remaining_steps2)
        for flow in unactivated:
            if steps <= 1:
                break
            potential_flow += flow * (steps - 1)
            steps -= 1
        return potential_flow

    def backtrack(agent1_pos, agent2_pos, remaining_steps1, remaining_steps2, activated_nodes, cumulative_flow):
        nonlocal best_cumulative_flow

        # Canonicalize state representation
        if agent1_pos > agent2_pos or (agent1_pos == agent2_pos and remaining_steps1 < remaining_steps2):
            agent1_pos, agent2_pos = agent2_pos, agent1_pos
            remaining_steps1, remaining_steps2 = remaining_steps2, remaining_steps1

        # Memoization state
        state = (agent1_pos, agent2_pos, remaining_steps1, remaining_steps2, frozenset(activated_nodes))
        if state in memo and memo[state] >= cumulative_flow:
            return
        memo[state] = cumulative_flow

        # Update the best cumulative flow
        best_cumulative_flow = max(best_cumulative_flow, cumulative_flow)

        # Prune if the upper bound cannot beat the best solution
        if cumulative_flow + upper_bound(remaining_steps1, remaining_steps2, activated_nodes) <= best_cumulative_flow:
            return

        # Generate candidates for both agents
        candidates1 = []
        if remaining_steps1 > 0:
            for node in flow_values:
                if node not in activated_nodes:
                    dist = distances[agent1_pos][node]
                    if remaining_steps1 > dist + 1:  # Only consider nodes reachable within remaining steps
                        potential_flow = flow_values[node] * (remaining_steps1 - (dist + 1))
                        candidates1.append((node, potential_flow, dist))

        candidates2 = []
        if remaining_steps2 > 0:
            for node in flow_values:
                if node not in activated_nodes:
                    dist = distances[agent2_pos][node]
                    if remaining_steps2 > dist + 1:  # Only consider nodes reachable within remaining steps
                        potential_flow = flow_values[node] * (remaining_steps2 - (dist + 1))
                        candidates2.append((node, potential_flow, dist))

        # Sort candidates by potential flow
        candidates1.sort(key=lambda x: x[1], reverse=True)
        candidates2.sort(key=lambda x: x[1], reverse=True)

        # Process actions for both agents
        for node1, _, dist1 in candidates1:
            for node2, _, dist2 in candidates2:
                if node1 == node2:  # Avoid activating the same node twice
                    continue
                # Agent 1 activates or moves to node1, Agent 2 activates or moves to node2
                activated_nodes.add(node1)
                activated_nodes.add(node2)
                backtrack(
                    node1,
                    node2,
                    remaining_steps1 - (dist1 if node1 != agent1_pos else 1),
                    remaining_steps2 - (dist2 if node2 != agent2_pos else 1),
                    activated_nodes,
                    cumulative_flow +
                    (flow_values[node1] * (remaining_steps1 - (dist1 if node1 != agent1_pos else 1))) +
                    (flow_values[node2] * (remaining_steps2 - (dist2 if node2 != agent2_pos else 1)))
                )
                activated_nodes.remove(node1)
                activated_nodes.remove(node2)

    # Start the backtracking process with both agents at the start node
    backtrack(start_node, start_node, max_steps, max_steps, set(), 0)
    return best_cumulative_flow

condensed_distances, condensed_flows = condense_graph(graph, flows, 'AA')
# print(condensed_distances)
# print(condensed_flows)
result = best_flow(condensed_flows, condensed_distances, 'AA', 30)
print('part 1:', result)

# result_pt2 = best_flow_two_agents(condensed_flows, condensed_distances, 'AA', 26)
result_pt2 = best_flow_two_agents(condensed_flows, condensed_distances, 'AA', 24)
print('part 2:', result_pt2)
