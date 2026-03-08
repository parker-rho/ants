# Holds the logic for the generation of graphs and maintaining pheromone levels on the edges.

def pheromone(n):
    """Initializes an n x n grid graph with pheromone levels set to 1.0."""
    graph = {}
    for i in range(n):
        for j in range(n):
            if i > 0:
                graph[(i, j)][(i - 1, j)] = 1.0
                graph[(i - 1, j)][(i, j)] = 1.0
            if i < n - 1:
                graph[(i, j)][(i + 1, j)] = 1.0
                graph[(i + 1, j)][(i, j)] = 1.0
            if j > 0:
                graph[(i, j)][(i, j - 1)] = 1.0
                graph[(i, j - 1)][(i, j)] = 1.0
            if j < n - 1:
                graph[(i, j)][(i, j + 1)] = 1.0
                graph[(i, j + 1)][(i, j)] = 1.0
    return graph

