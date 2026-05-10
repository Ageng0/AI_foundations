from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B', 'G'],
    'E': ['B', 'H', 'I'],
    'F': ['C', 'J'],
    'G': ['D'],
    'H': ['E'],
    'I': ['E'],
    'J': ['F', 'K'],
    'K': ['J'],      # K is the goal node
}

START = 'A'
GOAL  = 'K'

#BREADTH FIRST SEARCH
def bfs(graph, start, goal):
    """
    Breadth First Search: explores nodes level by level.
    Guarantees the shortest path in an unweighted graph.

    Parameters
    ----------
    graph : dict  – adjacency list
    start : str   – initial node
    goal  : str   – goal node

    Returns
    -------
    path         : list of nodes from start to goal (or None)
    visited_order: list of nodes in the order they were visited
    """
  
    queue         = deque([(start, [start])])
    visited       = set([start])
    visited_order = [start]

    print("BFS Exploration Log ")
    print(f"  Start: {start}  |  Goal: {goal}")
    print(f"  {'Step':<5} {'Node':<8} {'Queue (front→)'}")
    step = 0

    while queue:
        node, path = queue.popleft()
        step += 1
        queue_preview = [q[0] for q in list(queue)[:5]]
        print(f"  {step:<5} {node:<8} {queue_preview}")

        if node == goal:
            print(f"\n  ✓ Goal '{goal}' reached!")
            return path, visited_order

        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                visited_order.append(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return None, visited_order   # Goal not reachable


# DEPTH FIRST SEARCH 
def dfs(graph, start, goal):
    """
    Depth First Search: explores as far as possible down each branch.
    Uses an explicit stack (iterative – avoids Python recursion limits).

    Parameters
    ----------
    graph : dict  – adjacency list
    start : str   – initial node
    goal  : str   – goal node

    Returns
    -------
    path         : list of nodes from start to goal (or None)
    visited_order: list of nodes in the order they were visited
    """
  
    stack         = [(start, [start])]
    visited       = set()
    visited_order = []

    print(" DFS Exploration Log")
    print(f"  Start: {start}  |  Goal: {goal}")
    print(f"  {'Step':<5} {'Node':<8} {'Stack top-5 (top→)'}")
    step = 0

    while stack:
        node, path = stack.pop()   # Pop from the TOP (LIFO)

        if node in visited:
            continue

        visited.add(node)
        visited_order.append(node)
        step += 1
        stack_preview = [s[0] for s in reversed(stack[-5:])]
        print(f"  {step:<5} {node:<8} {stack_preview}")

        if node == goal:
            print(f"\n  ✓ Goal '{goal}' reached!")
            return path, visited_order

        # Push neighbours in reverse order so leftmost neighbour is explored first
        for neighbour in reversed(graph[node]):
            if neighbour not in visited:
                stack.append((neighbour, path + [neighbour]))

    return None, visited_order



print("=" * 55)
print("  CCS 2226 – Task 4: Search and Optimization")
print(f"  Graph: {dict(GRAPH)}")
print(f"  Start Node: {START}   |   Goal Node: {GOAL}")
print("=" * 55)

print("\n[1] BREADTH FIRST SEARCH (BFS)")
print("─" * 55)
bfs_path, bfs_order = bfs(GRAPH, START, GOAL)

print("\n[2] DEPTH FIRST SEARCH (DFS)")
print("─" * 55)
dfs_path, dfs_order = dfs(GRAPH, START, GOAL)


print("\n" + "=" * 55)
print("  RESULTS SUMMARY")
print("=" * 55)

def print_path(label, path, order):
    print(f"\n  {label}")
    if path:
        print(f"    Path   : {' → '.join(path)}")
        print(f"    Length : {len(path) - 1} steps")
    else:
        print(f"    No path found.")
    print(f"    Visit order: {' → '.join(order)}")

print_path("BFS Result:", bfs_path, bfs_order)
print_path("DFS Result:", dfs_path, dfs_order)

print("\n  Comparison:")
if bfs_path and dfs_path:
    print(f"    BFS path length : {len(bfs_path) - 1} steps  (always optimal for unweighted graphs)")
    print(f"    DFS path length : {len(dfs_path) - 1} steps  (first path found, not necessarily optimal)")


def draw_search(graph, path_bfs, path_dfs, start, goal):
    """Draw the graph twice: once with BFS path, once with DFS path highlighted."""

    # Approximate tree-like layout
    pos = {
        'A': (4, 4),
        'B': (2, 3), 'C': (6, 3),
        'D': (1, 2), 'E': (3, 2), 'F': (7, 2),
        'G': (0, 1), 'H': (2, 1), 'I': (4, 1), 'J': (8, 1),
        'K': (9, 0),
    }

    G_nx = nx.Graph()
    for node, nbrs in graph.items():
        for nbr in nbrs:
            G_nx.add_edge(node, nbr)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle(
        "Search & Optimization – BFS vs DFS\n"
        f"Start: {start}   Goal: {goal}",
        fontsize=15, fontweight='bold'
    )

    for ax, path, title, colour in zip(
        axes,
        [path_bfs, path_dfs],
        ["Breadth First Search (BFS)", "Depth First Search (DFS)"],
        ["#4472C4", "#FF4C4C"]
    ):
        ax.set_title(title, fontsize=13, fontweight='bold')

        # Colour coding
        path_edges = list(zip(path[:-1], path[1:])) if path else []
        node_colours = []
        for n in G_nx.nodes():
            if n == start:
                node_colours.append("#70AD47")   # Green = start
            elif n == goal:
                node_colours.append("#FF4C4C")   # Red = goal
            elif path and n in path:
                node_colours.append(colour)       # Highlight path nodes
            else:
                node_colours.append("#D9D9D9")   # Grey = unvisited

        edge_colours = []
        edge_widths  = []
        for e in G_nx.edges():
            if e in path_edges or (e[1], e[0]) in path_edges:
                edge_colours.append(colour)
                edge_widths.append(4)
            else:
                edge_colours.append("#AAAAAA")
                edge_widths.append(1.5)

        nx.draw(
            G_nx, pos, ax=ax,
            labels={n: n for n in G_nx.nodes()},
            node_color=node_colours,
            node_size=1400,
            font_size=12,
            font_weight='bold',
            edge_color=edge_colours,
            width=edge_widths,
        )
        if path:
            ax.set_xlabel(
                f"Path: {' → '.join(path)}   ({len(path)-1} steps)",
                fontsize=11
            )

        # Legend
        legend_items = [
            mpatches.Patch(color="#70AD47", label=f"Start ({start})"),
            mpatches.Patch(color="#FF4C4C", label=f"Goal ({goal})"),
            mpatches.Patch(color=colour,    label="Path nodes"),
            mpatches.Patch(color="#D9D9D9", label="Unvisited"),
        ]
        ax.legend(handles=legend_items, loc='lower left', fontsize=9)

    plt.tight_layout()
    plt.savefig("search_bfs_dfs.png", dpi=120)
    plt.show()
    print("\nSearch visualisation saved to search_bfs_dfs.png")

draw_search(GRAPH, bfs_path, dfs_path, START, GOAL)
