import networkx as nx
import matplotlib.pyplot as plt

def draw_dependency_graph(classes):
    G = nx.DiGraph(directed=True)
    nx.to_directed(G)

    max_dep = 0
    for class_object in classes:
        num_dep = len(class_object.dependencies)
        if (num_dep > max_dep):
            max_dep = num_dep

    for class_object in classes:
        G.add_node(class_object.name)
        for dependency in class_object.dependencies:
            G.add_edge(class_object.name, dependency)
    
    pos = nx.circular_layout(G)
    options = {
        'pos': pos,
        'with_labels': True,
        'arrows': True,
        'node_color': '#6e52ff',
        'node_size': 1000,
        'width': 1,
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }
    nx.draw(G, **options)
    plt.savefig("dependency_graph.png")