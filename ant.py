# Holds the logic for updating pheromone levels on the edges and the movement of ants through the graph.
import graph

def update_pheromone(graph, flow, decay=0.9):
    '''Updates the pheromone levels on the edges based on the flow of ants and a decay factor.'''
    for i in graph:
        for j in graph[i]:
            graph[i][j] = decay * (graph[i][j] + flow[i][j] + flow[j][i])
    return graph

#will have a budget of flow, have that scalar of flow at the source
#each ant is like a flow
#n = length/width of square graph
#s = source
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

#no leakage
#n = length/width of square graph
#d = destination (only outputs backwards flow)
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