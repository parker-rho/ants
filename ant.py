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


def update_pheromone(pheromone : torch.Tensor, ants : torch.Tensor, decay=0.9, step=None):
    '''
    Updates the pheromone levels on the edges based on the flow of ants and a decay factor.
    The pheromone levels are updated according to the formula:
    pheromone = decay * (pheromone + ants[i,j] + ants[j,i])
    '''
    pheromone = decay * (pheromone + ants + ants.T)
    if step is not None and step % 50 == 0:
        print_pheromones(pheromone, label="Pheromones")
        visualization.visualize(pheromone)
    return pheromone


def init_ants(n):
    '''
    Initializes a tensor to hold the flow of ants in the graph. Each ant is represented as a flow along an edge in the graph.
    Each edge is set to zero for initialization.
    '''
    ants = torch.zeros((n**2, n**2), dtype=torch.float32)
    return ants

def update_ants(ants : torch.Tensor, pheromone : torch.Tensor, source : int, destination : int, ants_per_step : int):
    '''
    Updates the flow of ants in the graph based on the pheromone levels and the source and destination nodes.
    The flow of ants is updated according to the formula:
    ants[i,j] = (pheromone[i,j] / sum(pheromone[i,:])) * v_ants[i] for i != destination
    ants[destination,:] = ants_per_step for all edges leading out of the destination node
    '''
    # Calculate the total flow for each node using pytorch's sum function to sum along the columns of the ants matrix
    # This follows the paper's equation for the flow on a node being the sum of flow going into that node
    v_ants = torch.sum(ants, dim=0)
    v_ants[source] = ants_per_step  # Add new ants at the source node
    queue = deque([source])
    visited = set()
    
    while queue and queue[0] != destination:
        curr_node = queue.popleft()
        if curr_node in visited:
            continue
        visited.add(curr_node)
        
        # Calculate the flow of ants from the current node to its neighbors based on the pheromone levels
        ants[curr_node] = pheromone[curr_node] / torch.sum(pheromone[curr_node]) * v_ants[curr_node]
        
        # Add unvisited neighbors to the queue
        neighbors = torch.nonzero(pheromone[curr_node] > 0).squeeze()
        if neighbors.dim() == 0:
            neighbors = neighbors.unsqueeze(0)
        for neighbor in neighbors:
            neighbor_int = neighbor.item()
            if neighbor_int not in visited:
                queue.append(int(neighbor_int))
    
    return ants

def simulate_ants(n, source, destination, ants_per_step, decay, iterations):
    '''
    Simulates the ant algorithm for a given number of iterations. Initializes the pheromone levels and ant flows, then iteratively updates them.
    '''
    pheromone = init_pheromones(n)
    ants = init_ants(n)

    print_pheromones(pheromone, label="Initial pheromones:")
    
    for step in range(iterations):
        ants = update_ants(ants, pheromone, source, destination, ants_per_step)
        ants = update_ants(ants, pheromone, destination, source, ants_per_step)
        pheromone = update_pheromone(pheromone, ants, decay, step=step)

    print_pheromones(pheromone, label="Final pheromones:")
    
    return pheromone, ants

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

# TODO: implement the path recovery function for the ant algorithm