import heapq
import networkx as nx
import matplotlib.pyplot as plt

# ==========================================
# 1. THE DIJKSTRA ALGORITHM IMPLEMENTATION
# ==========================================
def calculate_optimal_route(graph, start_node, end_node, weight_type='risk'):
    """
    Implements Dijkstra's Algorithm.
    weight_type: 'risk' (for safety) or 'distance' (for speed)
    """
    
    # Priority Queue: Stores tuples of (current_cost, current_node, path_taken)
    # We start with cost 0 at the start_node
    queue = [(0, start_node, [])]
    
    # Keep track of visited nodes and the lowest cost to get there
    visited = set()
    min_costs = {start_node: 0}

    while queue:
        # Pop the element with the lowest cost (this is the magic of Dijkstra)
        (cost, node, path) = heapq.heappop(queue)
        
        # If we've already found a cheaper way to this node, skip it
        if node in visited:
            continue
        
        # Add current node to path
        path = path + [node]
        visited.add(node)

        # If we reached the destination, return the result
        if node == end_node:
            return cost, path

        # Check neighbors
        for neighbor, attributes in graph[node].items():
            edge_weight = attributes.get(weight_type, 1) # Get risk or distance
            
            new_cost = cost + edge_weight
            
            # If this new path is cheaper than any we've seen before, add to queue
            if neighbor not in visited:
                if neighbor not in min_costs or new_cost < min_costs[neighbor]:
                    min_costs[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path))

    return float('inf'), [] # Return infinity if no path found

# ==========================================
# 2. BUILDING THE GRAPH (THE MAP)
# ==========================================
def build_city_map():
    # Create a graph object
    G = nx.Graph()

    # Add connections (edges) with Distance (km) and Risk (1-10)
    # Format: (Node A, Node B, Distance, Risk Score)
    roads = [
        ('Home', 'A', 5, 2),        # Short but slightly risky
        ('Home', 'B', 15, 1),       # Long but very safe
        ('A', 'C', 5, 8),           # Short but VERY dangerous (accident prone)
        ('B', 'C', 5, 1),           # Safe route connection
        ('A', 'Office', 20, 5),     # Moderate distance and risk
        ('C', 'Office', 5, 2),      # Final stretch
        ('B', 'Office', 25, 1)      # Long safe way around
    ]

    for u, v, dist, risk in roads:
        G.add_edge(u, v, distance=dist, risk=risk)
    
    return G

# ==========================================
# 3. VISUALIZATION
# ==========================================
def draw_map_with_path(G, path, title):
    pos = nx.spring_layout(G, seed=42) # Positions nodes automatically
    plt.figure(figsize=(8, 6))
    
    # Draw all nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    
    # Label edges with Risk scores
    edge_labels = nx.get_edge_attributes(G, 'risk')
    edge_labels_formatted = {k: f"Risk: {v}" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_formatted)

    # Highlight the chosen path in Red
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
    
    plt.title(title)
    plt.show()

# ==========================================
# 4. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    city_map = build_city_map()

    # Scenario 1: User wants the SAFEST route (Minimize Risk)
    risk_cost, safe_path = calculate_optimal_route(city_map, 'Home', 'Office', 'risk')
    print(f"🛡️  Safest Route: {safe_path} | Total Accumulated Risk: {risk_cost}")

    # Scenario 2: User wants the SHORTEST route (Minimize Distance)
    dist_cost, fast_path = calculate_optimal_route(city_map, 'Home', 'Office', 'distance')
    print(f"🚀 Fastest Route: {fast_path} | Total Distance: {dist_cost}")

    # Visualize the SAFE route
    draw_map_with_path(city_map, safe_path, "Recommended Path: Minimizing Risk")