# Holds the logic for updating pheromone levels on the edges and the movement of ants through the graph.

def update_pheromone(graph, flow, decay=0.9):
    '''Updates the pheromone levels on the edges based on the flow of ants and a decay factor.'''
    for i in graph:
        for j in graph[i]:
            graph[i][j] = decay * (graph[i][j] + flow[i][j] + flow[j][i])
    return graph