import networkx as nx
import matplotlib.pyplot as plt

def plan_city_a(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment):

    # --- 1. Initialize Base Flow Network (Capacities C) ---
    C = nx.DiGraph()
    source_node = 'S'
    sink_node = 'T'
    
    # 1.1 S -> Hubs (Capacity 1)
    for i in range(num_data_hubs):
        C.add_edge(source_node, i, capacity=1)

    # 1.2 Hubs -> Providers (Capacity 1 based on connections)
    for hub, providers in connections.items():
        for provider in providers:
            C.add_edge(hub, provider, capacity=1)

    # 1.3 Providers -> T (Capacity based on provider_capacities)
    for j in range(num_service_providers):
        provider_node = num_data_hubs + j 
        cap = provider_capacities[provider_node]
        C.add_edge(provider_node, sink_node, capacity=cap)

    # --- 2. Calculate Flow F based on Preliminary Assignment ---
    F = nx.DiGraph()
    # Initialize all existing edges in F with 0 flow
    for u, v, data in C.edges(data=True):
        F.add_edge(u, v, flow=0)

    # Apply the flow for each assignment: S -> u -> v -> T
    for hub, provider in preliminary_assignment.items():
        # S -> Hub (u) flow
        F[source_node][hub]['flow'] += 1
        
        # Hub (u) -> Provider (v) flow
        F[hub][provider]['flow'] += 1
        
        # Provider (v) -> T flow (accumulate if multiple hubs use same provider)
        F[provider][sink_node]['flow'] += 1

    # --- 3. Build the Residual Graph R_final (Residual Capacities) ---
    R_final = nx.DiGraph()

    # Define all nodes for iteration
    all_nodes = list(C.nodes())
    
    # 3.1 Forward Edges: c_f(u, v) = c(u, v) - f(u, v)
    for u, v, data in C.edges(data=True):
        flow_uv = F.edges[u, v]['flow'] if F.has_edge(u, v) else 0
        residual_cap = data['capacity'] - flow_uv
        if residual_cap > 0:
            R_final.add_edge(u, v, capacity=residual_cap, direction='forward')
            
    # 3.2 Backward Edges: c_f(v, u) = f(u, v)
    for u, v, data in F.edges(data=True):
        flow_uv = data['flow']
        if flow_uv > 0:
            # Add the reverse edge (v -> u) with capacity equal to the flow
            if R_final.has_edge(v, u):
                
                R_final[v][u]['capacity'] += flow_uv 
            else:
                R_final.add_edge(v, u, capacity=flow_uv, direction='backward')

    # --- 4. Visualization Setup ---
    
    G_plot = R_final
    plt.figure(figsize=(14, 8))
    
    pos = {}
    hub_nodes = list(range(num_data_hubs))
    provider_nodes = list(range(num_data_hubs, num_data_hubs + num_service_providers))

    # Position: Source (Far Left)
    pos[source_node] = (-2, num_data_hubs / 2.0)
    
    # Position: Data Hubs (Left Column)
    for i in range(num_data_hubs):
        pos[i] = (0, num_data_hubs - 1 - i)
        
    # Position: Service Providers (Right Column)
    for j in range(num_service_providers):
        provider_node = num_data_hubs + j 
        pos[provider_node] = (2, num_service_providers - 1 - j)
        
    # Position: Sink (Far Right)
    pos[sink_node] = (4, num_data_hubs / 2.0)

    # Draw Nodes and Labels
    node_colors = []
    for node in G_plot.nodes():
        if node == source_node or node == sink_node:
            node_colors.append('#90EE90') # Light Green
        elif node in hub_nodes:
            node_colors.append('#ADD8E6') # Light Blue (Hubs)
        elif node in provider_nodes:
            node_colors.append('#FFDAB9') # Peach (Providers)
        else: 
            node_colors.append('lightgray')

    nx.draw_networkx_nodes(G_plot, pos, node_size=800, node_color=node_colors)
    nx.draw_networkx_labels(G_plot, pos)
    
    # Separate Edges by direction for distinct visualization
    forward_edges = [(u, v) for u, v, d in G_plot.edges(data=True) if d.get('direction') == 'forward']
    backward_edges = [(u, v) for u, v, d in G_plot.edges(data=True) if d.get('direction') == 'backward']

    # Forward edges (Remaining original capacity) - Gray
    nx.draw_networkx_edges(G_plot, pos, edgelist=forward_edges, edge_color='gray', arrows=True, arrowsize=20)
    # Backward edges (Flow pushed, allowing cancellation) - Red dashed
    nx.draw_networkx_edges(G_plot, pos, edgelist=backward_edges, edge_color='red', arrows=True, arrowsize=20, style='dashed')
    
    # Draw Edge Labels (Capacities)
    edge_labels = nx.get_edge_attributes(G_plot, 'capacity')
    nx.draw_networkx_edge_labels(G_plot, pos, edge_labels=edge_labels, label_pos=0.6, font_size=9)

    plt.title("Problem 1.c: Residual Graph after Preliminary Assignment Flow")
    plt.axis('off')
    
    plt.show()

if __name__ == "__main__":
    # Input from Listing 1
    plan_city_a(
        num_data_hubs=5,
        num_service_providers=5,
        connections={
            0: [5, 7, 8], 
            1: [5, 8], 
            2: [7, 8, 9], 
            3: [5, 6, 8, 9], 
            4: [5, 6, 7, 8]
        },
        # Capacities: [0,0,0,0,0] for hubs, [0,1,0,2,2] for providers 5,6,7,8,9
        provider_capacities=[0]*5 + [0, 1, 0, 2, 2],
        preliminary_assignment={0: 8, 1: 8, 2: 9, 3: 9}
    )