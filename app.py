import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# ==========================================
# CORE ALGORITHMS 
# ==========================================
def calculate_optimal_route(graph, start_node, end_node, weight_type='risk'):
    queue = [(0, start_node, [])]
    visited = set()
    min_costs = {start_node: 0}

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited: continue
        
        path = path + [node]
        visited.add(node)

        if node == end_node:
            return cost, path

        for neighbor, attributes in graph[node].items():
            edge_weight = attributes.get(weight_type, 1)
            new_cost = cost + edge_weight
            
            if neighbor not in visited:
                if neighbor not in min_costs or new_cost < min_costs[neighbor]:
                    min_costs[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path))

    return float('inf'), []

def build_city_map():
    G = nx.Graph()
    # (Node A, Node B, Distance, Risk Score)
    roads = [
        ('Home', 'A', 5, 2),
        ('Home', 'B', 15, 1),
        ('A', 'C', 5, 8),
        ('B', 'C', 5, 1),
        ('A', 'Office', 20, 5),
        ('C', 'Office', 5, 2),
        ('B', 'Office', 25, 1)
    ]
    for u, v, dist, risk in roads:
        G.add_edge(u, v, distance=dist, risk=risk)
    return G

# ==========================================
# STREAMLIT FRONTEND
# ==========================================

# set up the page title
st.set_page_config(page_title="SafeRoute AI", layout="wide")
st.title("🛡️ SafeRoute AI: Risk-Aware Navigation")
st.markdown("Choose your priority: **Safety** vs **Speed**")

# create two columns for layout
col1, col2 = st.columns([1, 2])

# LEFT COLUMN: User Inputs
with col1:
    st.header("📍 Trip Settings")
    
    # load the map data
    city_map = build_city_map()
    all_nodes = list(city_map.nodes())

    # dropdowns for user to pick start/end
    start_loc = st.selectbox("Start Location", all_nodes, index=0)
    end_loc = st.selectbox("Destination", all_nodes, index=3) # Default to Office

    # radio button for preference
    preference = st.radio(
        "What is more important?",
        ("Minimize Risk (Safety First)", "Minimize Distance (Fastest Route)")
    )

    calculate_btn = st.button("Find Best Route 🚀")

# RIGHT COLUMN: The Result 
with col2:
    if calculate_btn:
        # determine which weight to use based on user choice
        weight_mode = 'risk' if "Risk" in preference else 'distance'
        
        # run the algorithm
        cost, path = calculate_optimal_route(city_map, start_loc, end_loc, weight_mode)

        if not path:
            st.error("No path found between these locations!")
        else:
            # show the Result Metrics
            st.success(f"**Recommended Route Found:** {' → '.join(path)}")
            st.metric(label="Total Cost (Risk Score or Km)", value=cost)

            # draw the Map
            fig, ax = plt.subplots(figsize=(8, 6))
            pos = nx.spring_layout(city_map, seed=42)
            
            # draw base graph
            nx.draw(city_map, pos, ax=ax, with_labels=True, node_color='#e0e0e0', node_size=2000)
            
            # draw risk labels on edges
            edge_labels = nx.get_edge_attributes(city_map, 'risk')
            edge_labels_formatted = {k: f"Risk: {v}" for k, v in edge_labels.items()}
            nx.draw_networkx_edge_labels(city_map, pos, edge_labels=edge_labels_formatted, font_color='red')

            # highlight the path
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(city_map, pos, edgelist=path_edges, edge_color='#00C851', width=4)
            nx.draw_networkx_nodes(city_map, pos, nodelist=path, node_color='#00C851', node_size=2000)

            # show the plot in the web app
            st.pyplot(fig)