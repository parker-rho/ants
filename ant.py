# Holds the logic for updating pheromone levels on the edges and the movement of ants through the graph.
import graph

# TODO: use pytorch!
# TODO: make documentation cleaner

def update_pheromone(graph, flow, decay=0.9):
    '''Updates the pheromone levels on the edges based on the flow of ants and a decay factor.'''
    for i in graph:
        for j in graph[i]:
            graph[i][j] = decay * (graph[i][j] + flow[i][j] + flow[j][i])
    return graph

# will have a budget of flow, have that scalar of flow at the source
# each ant is like a flow
# n = length/width of square graph
# s = source
def create_flow(forward, n, s, base_flow_amount):
    flow = {}
    for u in range(n):
        for v in range(n):
            if (u,v) == s and forward:
                total_phermones = phermone[(u,v)][(u+1,v)]+phermone[(u,v)][(u-1,v)]+phermone[(u,v)][(u,v+1)]+phermone[(u,v)][(u,v-1)]
                flow[(u,v)][(u+1,v)] = base_flow_amount*(phermone[(u,v)][(u+1,v)]/total_phermones)
                flow[(u,v)][(u-1,v)] = base_flow_amount*(phermone[(u,v)][(u-1,v)]/total_phermones)
                flow[(u,v)][(u,v+1)] = base_flow_amount*(phermone[(u,v)][(u,v+1)]/total_phermones)
                flow[(u,v)][(u,v-1)] = base_flow_amount*(phermone[(u,v)][(u,v-1)]/total_phermones)
            else:
                flow[(u,v)][(u+1,v)] = 0
                flow[(u,v)][(u-1,v)] = 0
                flow[(u,v)][(u,v+1)] = 0
                flow[(u,v)][(u,v-1)] = 0
    return graph

# no leakage
# n = length/width of square graph
# d = destination (only outputs backwards flow)
def update_flow(flow, forward, backward, phermone, n, d):
  for u in range(n):
      for v in range(n):
        if (u,v) == d:
            flow[(u,v)] = forward[(u-1,v)][(u,v)]+forward[(u+1)][(u,v)]+forward[(u,v-1)][(u,v)]+forward[(u,v+1)][(u,v)]
            total_phermones = phermone[(u,v)][(u+1,v)]+phermone[(u,v)][(u-1,v)]+phermone[(u,v)][(u,v+1)]+phermone[(u,v)][(u,v-1)]

            forward[(u,v)][(u+1,v)] = flow[(u,v)]*(phermone[(u,v)][(u+1,v)]/total_phermones)
            backward[(u+1,v)][(u,v)] = forward[(u,v)][(u+1,v)]
            forward[(u,v)][(u-1,v)] = flow[(u,v)]*(phermone[(u,v)][(u-1,v)]/total_phermones)
            backward[(u,v)][(u-1,v)] = forward[(u,v)][(u-1,v)]
            forward[(u,v)][(u,v+1)] = flow[(u,v)]*(phermone[(u,v)][(u,v+1)]/total_phermones)
            backward[(u,v)][(u,v+1)] = forward[(u,v)][(u,v+1)]
            forward[(u,v)][(u,v-1)] = flow[(u,v)]*(phermone[(u,v)][(u,v-1)]/total_phermones)
            backward[(u,v)][(u,v-1)] = forward[(u,v)][(u,v-1)]
          
N = 10
source = [1,2]
base_flow_amount = 15
phermone = graph.pheromone(N)
flow = create_flow(True, N, source, base_flow_amount)
update_flow(flow, phermone, N)

# TODO: implement new flow update function!
# goal: a helper function to update the flow to t + 1, determining "forward" by the interpretation of who is source and who is sink
# input: pheromone values, forward edge values, t, source, sink
# output: updated forward edge values
# 
# step 0: initialize new edge values and initialize vertex flow values to 0 for the time being
# step 1: take in edge values and compute the flow at vertices at t + 1
# step 1.1: add a base value to the source vertex to represent the generation of new ants at the source
# step 2: use vertices to compute edge values for t + 1 in a bfs style with a visited set and neighbor set
# step 2.1: only update edge values for edges that have a value = 0/haven't been visited yet
# step 2.2: only write edge values for the exact direction of flow to aid in the vertex computation at the next step and for the continued running
# step 3: output the updated edge values
#
# intended use: run this function for both the source as the source and the sink as the source (to get both forward and backward), then update the pheromone values based on the flow values
# this will be involved in an overall t-iterated loop that goes until we reach convergence to the shortest path

# TODO: implement the path recovery function for the ant algorithm