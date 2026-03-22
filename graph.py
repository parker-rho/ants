import torch

# Holds the logic for the generation of graphs and maintaining pheromone levels on the edges.

def init_pheromones(n):
    """
    Initializes an n^2 x n^2 grid graph with pheromone levels set to 1.0.
    A node at row i and column j in the grid corresponds to the index i*n + j in the graph. Edges are created
    between nodes that are adjacent in the grid (up, down, left, right), and the pheromone level on each edge 
    is initialized to 1.0.
    """
    graph = torch.zeros((n**2, n**2), dtype=torch.float32)
    nodes = torch.arange(n**2)

    # Horizontal edges are drawn between nodes that are not on the rightmost column
    mask_h = (nodes % n) < (n - 1)
    u_h = nodes[mask_h]
    graph[u_h, u_h + 1] = graph[u_h + 1, u_h] = 1.0

    # Vertical edges are drawn between nodes that are not on the bottom row
    mask_v = nodes < (n**2 - n)
    u_v = nodes[mask_v]
    graph[u_v, u_v + n] = graph[u_v + n, u_v] = 1.0

    return graph
