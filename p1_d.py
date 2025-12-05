# Problem 1d

import collections

def plan_city_d(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment):
    
    # --- 1. Graph Setup (Residual Capacity Matrix) ---
    # Nodes: S(0), Hubs(1..n), Providers(n+1..n+k), T(n+k+1)
    
    source = 0
    sink = num_data_hubs + num_service_providers + 1
    total_nodes = sink + 1
    
    # Hubs are indexed 1 to num_data_hubs
    # Providers are indexed num_data_hubs + 1 to num_data_hubs + num_service_providers
    
    capacity = [[0] * total_nodes for _ in range(total_nodes)]
    flow = [[0] * total_nodes for _ in range(total_nodes)]
    
    # Helper to map Hub/Provider ID to Array Index
    def get_node_index(node_id):
        if node_id == 'S': return source
        if node_id == 'T': return sink
        
        # Hubs 0 to n-1 map to indices 1 to n
        if node_id < num_data_hubs:
            return node_id + 1
        
        # Providers n to n+k-1 map to indices n+1 to n+k
        return node_id + 1

    # --- 1.1 Populate Capacity Matrix C ---
    
    # S -> Hubs (Capacity 1)
    for i in range(num_data_hubs):
        hub_idx = get_node_index(i)
        capacity[source][hub_idx] = 1

    # Hubs -> Providers (Capacity 1)
    for hub_id, provider_list in connections.items():
        hub_idx = get_node_index(hub_id)
        for provider_id in provider_list:
            provider_idx = get_node_index(provider_id)
            capacity[hub_idx][provider_idx] = 1
            
    # Providers -> T (Capacity from provider_capacities)
    for j in range(num_service_providers):
        provider_id = num_data_hubs + j
        provider_idx = get_node_index(provider_id)
        cap = provider_capacities[provider_id]
        capacity[provider_idx][sink] = cap

    # --- 1.2 Initialize Flow F based on Preliminary Assignment ---
    initial_flow = 0
    for hub_id, provider_id in preliminary_assignment.items():
        hub_idx = get_node_index(hub_id)
        provider_idx = get_node_index(provider_id)
        
        # Flow path: S -> Hub -> Provider -> T
        
        # S -> Hub flow = 1
        flow[source][hub_idx] += 1
        
        # Hub -> Provider flow = 1
        flow[hub_idx][provider_idx] += 1
        
        # Provider -> T flow = 1
        flow[provider_idx][sink] += 1
        
        initial_flow += 1

    # --- 2. Edmonds-Karp Algorithm ---
    max_flow = initial_flow

    # BFS function to find an augmenting path in the residual graph
    def bfs(residual_capacity, parent):
        queue = collections.deque([source])
        # parent array tracks the path from S to T
        parent[:] = [-1] * total_nodes
        parent[source] = source
        
        while queue:
            u = queue.popleft()
            
            # Check all nodes v
            for v in range(total_nodes):
                # If v is not visited (parent[v] == -1) AND there is remaining capacity
                if parent[v] == -1 and residual_capacity[u][v] > 0:
                    parent[v] = u
                    if v == sink:
                        return True # Path found
                    queue.append(v)
        return False # No path found

    # Edmonds-Karp loop
    while True:
        # Create residual capacity graph R_c(u, v) = C(u, v) - F(u, v)
        residual_capacity = [[0] * total_nodes for _ in range(total_nodes)]
        for u in range(total_nodes):
            for v in range(total_nodes):
                # Forward residual capacity
                residual_capacity[u][v] = capacity[u][v] - flow[u][v]
                # Backward residual capacity (equal to current flow on (v, u))
                residual_capacity[u][v] += flow[v][u]
        
        # Find augmenting path using BFS
        parent = [-1] * total_nodes
        if not bfs(residual_capacity, parent):
            break # No more augmenting paths, max flow achieved

        # 3. Find path flow (bottleneck capacity)
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual_capacity[parent[s]][s])
            s = parent[s]
            
        # 4. Update flow on path
        max_flow += path_flow
        
        v = sink
        while v != source:
            u = parent[v]
            # Update flow: subtract path_flow from reverse edge, add to forward edge
            
            # Check if (u, v) is a forward edge in the original graph
            if capacity[u][v] > 0:
                flow[u][v] += path_flow
            else:
                # If (u, v) is not in C, it must be a backward edge (v, u) in C
                flow[v][u] -= path_flow

            v = parent[v]

    # --- 3. Result Check ---
    # The max flow should equal the total number of hubs (demand) for all to be connected.
    required_flow = num_data_hubs
    
    return max_flow == required_flow

if __name__ == "__main__":
    # Input from Listing 1
    num_hubs = 5
    num_providers = 5
    connections_data = {
        0: [5, 7, 8], 
        1: [5, 8], 
        2: [7, 8, 9], 
        3: [5, 6, 8, 9], 
        4: [5, 6, 7, 8]
    }
    # Capacities: [0,0,0,0,0] for hubs, [0,1,0,2,2] for providers 5,6,7,8,9
    capacities_data = [0]*5 + [0, 1, 0, 2, 2]
    pre_assignment = {0: 8, 1: 8, 2: 9, 3: 9}
    
    is_feasible = plan_city_d(
        num_data_hubs=num_hubs,
        num_service_providers=num_providers,
        connections=connections_data,
        provider_capacities=capacities_data,
        preliminary_assignment=pre_assignment
    )
    
    print(f"Can all {num_hubs} data hubs be connected? {is_feasible}")