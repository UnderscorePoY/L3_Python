def main():
    import networkx as nx
    import matplotlib.pyplot as plt

    q: int = 5
    G = nx.DiGraph()
    G.add_nodes_from(["s", "x", "y", "z", "t", "u", "v", "w"])

    G.add_weighted_edges_from([
        ("s", "x", q),
        ("x", "y", q),
        ("y", "z", q),
        ("z", "t", q),
        ("s", "u", q),
        ("u", "v", q),
        ("v", "w", q),
        ("w", "t", q),
        ("y", "v", 1),
    ])

    print(G.nodes(), G.edges())

    # Plot
    pos = nx.spring_layout(G)  # List of positions of nodes
    weights = nx.get_edge_attributes(G, "weight")  # List of weights
    nx.draw_networkx(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    nx.draw_networkx_edges(G, pos, arrowstyle="->")

    plt.title("Basic Graphs with Networkx")
    plt.gcf().canvas.manager.set_window_title("")  # Hide window title

    # Display Graph
    plt.show()


if __name__ == '__main__':
    main()
