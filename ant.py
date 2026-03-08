# Holds the logic for updating pheromone levels on the edges and the movement of ants through the graph.
import graph

#will have a budget of flow, have that scalar of flow at the source
#each ant is like a flow
def create_flow(n, source, base_flow_amount):
    graph = {}
    for i in range(n):
        for j in range(n):
            if (i,j) == (source[0],source[1]):
               graph[i][j] = base_flow_amount
            else:
               graph[i][j] = 0
    return graph

#no leakage
def update_flow(flow, phermone, n):
  for u in range(n):
      for v in range(n):
        f_u = 0
        p_u = 0
        for z in range(n):
            f_u = f_u + flow(z,u)
            p_u = p_u + phermone(u,z)
        flow(u,v) = f_u*(phermone(u,v)/(p_u))
          
N = 10
source = [1,2]
base_flow_amount = 15
phermone = graph.pheromone(N)
flow = create_flow(N, source, base_flow_amount)
update_flow(flow, phermone, N)