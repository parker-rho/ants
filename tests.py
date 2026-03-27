import torch
from graph import *

def dijkstras(anthill: int, food: int, graph: torch.Tensor):
  """
  Performs Dijkstra's algorithm to find the shortest path from the ants to the food on the graph.
  Coordinates of the ants and food are given as integers corresponding to their positions on the graph taking the
  form i*n + j, where i is the row and j is the column of the grid, and the graph is represented as an 
  adjacency matrix with pheromone levels as edge weights.
  Args:
    anthill: An integer representing the position of the anthill on the graph.
    food: An integer representing the position of the food on the graph.
    graph: The graph on which to perform Dijkstra's algorithm.
  Returns:
    path: A list of nodes representing the shortest path from the anthill to the food on the graph.
  """
  n = int(graph.size(0))
  # Visited is a bool mask for a tensor
  visited = torch.zeros((n,), dtype=torch.bool)
  distances = torch.full((n,), float('inf'))
  distances[anthill] = 0

  # Used for backtracing
  previous_nodes = torch.full((n,), -1, dtype=torch.long)

  # Running Dijkstra's
  while not visited.all():
    # Choose the unvisited node with the smallest distance
    current_node = torch.argmin(distances.masked_fill(visited, float('inf'))).item()
    visited[current_node] = True

    # Uses the adjacency list given by [graph]
    neighbors = graph[current_node]
    new_distances = distances[current_node] + neighbors

    # Distances for a node are only updated if there is an edge from [current_node] and it hasn't been visited
    valid = (neighbors > 0) & ~visited
    improved = valid & (new_distances < distances)

    distances[improved] = new_distances[improved]
    previous_nodes[improved] = current_node

  # Reconstruct the path
  path = []
  current = food
  while current is not -1:
    path.append(current)
    current = previous_nodes[current]
  path.reverse()

  return path

def init_test():
  """
  Initializes random positions for the anthill and the food, and benchmarks the performance of classical 
  pathfinding algorithms (Dijkstra's, A*, BFS, DFS) in finding shortest paths from the anthill to the food on 
  the graph against the performance of our distributed pheromone-based algorithm.
  """
  n = 10
  pheromone = init_pheromones(n)
  anthill = torch.randint(0, n**2, (1,))
  food = torch.randint(0, n**2, (1,))

  path_dijkstra = dijkstras(anthill, food, pheromone)

  # TODO: finish initialization of this test suite

# TODO: potentially add logic for visualizations while the algorithm is running!