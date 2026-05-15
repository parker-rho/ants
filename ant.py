import torch
from collections import deque
import visualization

def init_pheromones(n):
    """
    Initializes an n^2 x n^2 grid graph with pheromone levels set to 1.0.
    A node at row i and column j in the grid corresponds to the index i*n + j in the graph. Edges are created
    between nodes that are adjacent in the grid (up, down, left, right), and the pheromone level on each edge 
    is initialized to 1.0.
    """
    pheromone = torch.zeros((n**2, n**2), dtype=torch.float32)
    nodes = torch.arange(n**2)

    # Horizontal edges are drawn to the right from nodes that are not on the rightmost column
    mask_h = (nodes % n) < (n - 1)
    u_h = nodes[mask_h]
    pheromone[u_h, u_h + 1] = pheromone[u_h + 1, u_h] = 1.0

    # Vertical edges are drawn down from nodes that are not on the bottom row
    mask_v = nodes < (n**2 - n)
    u_v = nodes[mask_v]
    pheromone[u_v, u_v + n] = pheromone[u_v + n, u_v] = 1.0

    return pheromone

def get_edge_mask(pheromone, source, n):
    """
    Returns a mask where mask[u,v] = True if v is further from source than u.
    The distances are computed using standard BFS. Note that pheromone
    works as an adjacency matrix here since we only call this function before
    any pheromone updates have been made.
    """
    n_nodes = n**2
    
    # BFS via repeated matrix-vector multiplication
    dist = torch.full((n_nodes,), float('inf'))
    dist[source] = 0
    frontier = torch.zeros(n_nodes)
    frontier[source] = 1.0
    
    for d in range(n_nodes):
        # Spread the frontier to the next layer of nodes
        next_frontier = (pheromone @ frontier) > 0
        # Only keep nodes not yet visited
        unvisited = dist == float('inf')
        newly_reached = next_frontier & unvisited
        if not newly_reached.any():
            break
        dist[newly_reached] = d + 1
        frontier = newly_reached.float()
    mask = dist.unsqueeze(1) < dist.unsqueeze(0)
    return mask

def simulate_ants(n, source, destination, initial_ants, ants_rate, decay, iterations):
    '''
    Simulates the ant algorithm for a given number of iterations. Initializes the pheromone levels and ant flows, then iteratively updates them.
    '''
    pheromone = init_pheromones(n)
    # These vectors hold the flow at each node (i.e. the value of f_u in the paper)
    forward_nodes = torch.zeros(n**2)
    backward_nodes = torch.zeros(n**2)
    forward_nodes[source] = initial_ants
    backward_nodes[destination] = initial_ants

    # Compute masks for determining forward and backward edges.
    forward_mask = get_edge_mask(pheromone, source, n)
    backward_mask = get_edge_mask(pheromone, destination, n)

    for step in range(iterations):
        # Normalize pheromone rows by the row sum in line with the formula for flow:
        # f_{uv} = (pheromone[i,j] / sum(pheromone[i,:])) * f_u for u != destination
        # In other words, fractions is the (pheromone[i,j] / sum(pheromone[i,:])) part of the formula
        fractions = (pheromone * forward_mask) / (pheromone * forward_mask).sum(dim=1, keepdim=True).clamp(min=1e-10)
        fractions[destination] = 0
        fractions_b = (pheromone * backward_mask) / (pheromone * backward_mask).sum(dim=1, keepdim=True).clamp(min=1e-10)
        fractions_b[source] = 0

        # Calculate the flow of ants along each edge based on the pheromone levels and the current flow of ants at each node
        forward_ants = fractions * forward_nodes.unsqueeze(1)
        backward_ants = fractions_b * backward_nodes.unsqueeze(1)

        # New values for the flow at each node
        new_forward_nodes = forward_ants.sum(dim=0)
        new_backward_nodes = backward_ants.sum(dim=0)

        # Reinject at sources, absorb at sinks
        new_forward_nodes[source] = initial_ants + (ants_rate * step)
        new_forward_nodes[destination] = 0
        new_backward_nodes[destination] = initial_ants + (ants_rate * step)
        new_backward_nodes[source] = 0

        # Pheromone update
        total_ants = forward_ants + backward_ants
        pheromone = decay * (pheromone + total_ants + total_ants.T)

        forward_nodes = new_forward_nodes
        backward_nodes = new_backward_nodes

        if step % 50 == 0:
            visualization.visualize(pheromone)    
    visualization.visualize(pheromone)
    return pheromone

def print_pheromones(pheromone: torch.Tensor, label: str = ""):
    """
    Pretty prints the pheromone edge graph. Matches the visualization values
    """
    p = pheromone.numpy()
    n = int(p.shape[0] ** 0.5)
    print(f"\n{label}")
    
    for row in range(n - 1, -1, -1):  
        h_line = ""
        for col in range(n):
            node = row * n + col
            h_line += f"*"
            if col < n - 1:
                edge_val = p[node, node + 1]
                h_line += f"--{edge_val:6.2f}--"
        print(h_line)
        
        if row > 0:
            v_line = ""
            for col in range(n):
                node = row * n + col
                edge_val = p[node, node - n]
                v_line += f"|{edge_val:6.2f} "
                if col < n - 1:
                    v_line += "         "
            print(v_line)