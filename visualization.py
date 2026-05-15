import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import torch

call_count = 0

source_node = None
destination_node = None

def visualize(pheromone: torch.Tensor):
    """
    Creates a visualiation using matplotlib of the pheromone graph at a 
    certain stage. Red color means more pheromones and blue means less.
    There are also numerical values on the edges to represent the pheremone
    values to the hundreths decimal place. Assumes that pheromone 
    was created with init_pheromones.
    Can toggle True or False with plt.show at the bottom of the code
    to pause between stages of the algorithm running.
    """
    global call_count
    call_count += 1
    print(f"Visualize called {call_count} times")
    p = pheromone.numpy()
    n = int(p.shape[0] ** 0.5)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(-0.5, n - 0.5)
    
    # Normalize pheromone values to [0, 1]
    p_min, p_max = p[p > 0].min(), p.max()
    
    for u in range(n**2):
        for v in range(u + 1, n**2):
            u_row, u_col = divmod(u, n)
            v_row, v_col = divmod(v, n)

            is_edge = (abs(u - v) == 1 and u_row == v_row) or (abs(u - v) == n and u_col == v_col)
            if not is_edge:
                continue

            mid_col = (u_col + v_col) / 2
            mid_row = (u_row + v_row) / 2

            if p[u, v] <= 0:
                ax.plot([u_col, v_col], [u_row, v_row], color=(0.75, 0.75, 0.75), linewidth=2)
            else:
                strength = (p[u, v] - p_min) / (p_max - p_min + 1e-8)
                color = (strength, 0, 1 - strength)
                ax.plot([u_col, v_col], [u_row, v_row], color=color, linewidth=2)

            ax.text(mid_col, mid_row, f"{p[u, v]:.2f}",
                    fontsize=7, ha='center', va='center',
                    color='black',
                    bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.6))
    
    for node in range(n**2):
        row, col = divmod(node, n)
        if node == source_node:
            ax.plot(col, row, 'go', markersize=10)
            ax.annotate('anthill', xy=(col, row), xytext=(col - 0.6, row + 0.5),
                        fontsize=8, color='green',
                        arrowprops=dict(arrowstyle='->', color='green'))
        elif node == destination_node:
            ax.plot(col, row, 'ro', markersize=10)
            ax.annotate('food source', xy=(col, row), xytext=(col + 0.2, row + 0.5),
                        fontsize=8, color='red',
                        arrowprops=dict(arrowstyle='->', color='red'))
        else:
            ax.plot(col, row, 'ko', markersize=4)
    
    plt.tight_layout()
    plt.show(block=True)
    plt.pause(0.1)
    plt.close()