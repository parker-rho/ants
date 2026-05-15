import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import torch

call_count = 0

def visualize(pheromone: torch.Tensor):
    """
    Assumes that pheromone was created with init_pheromones
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
            if p[u, v] > 0:
                u_row, u_col = divmod(u, n)
                v_row, v_col = divmod(v, n)
                
                strength = (p[u, v] - p_min) / (p_max - p_min + 1e-8)
                color = (strength, 0, 1 - strength)
                
                ax.plot([u_col, v_col], [u_row, v_row], color=color, linewidth=2)

                mid_col = (u_col + v_col) / 2
                mid_row = (u_row + v_row) / 2
                ax.text(mid_col, mid_row, f"{p[u, v]:.2f}",
                        fontsize=7, ha='center', va='center',
                        color='black',
                        bbox=dict(boxstyle='round,pad=0.1', fc='white', alpha=0.6))
    
    for node in range(n**2):
        row, col = divmod(node, n)
        ax.plot(col, row, 'ko', markersize=4)
    
    plt.tight_layout()
    plt.show(block=True)  # <-- change this line
    plt.pause(0.1)         # <-- add this line
    plt.close()            # <-- add this line