import numpy as np
import os
import networkx as nx # version 1.11

### convert graphs from GraphML format used by Graph Kernel Suite (https://github.com/BorgwardtLab/GraphKernels)
### to C# format used by Parallel gSpan (https://link.springer.com/chapter/10.1007/978-3-319-17996-4_15)

# rename node and edge labels, node/edge label starts from 0
def rename_label(data_name, data_path, n_file):
    graph_node_labels, graph_edge_labels = [], []
    for f_id in range(1, n_file + 1):
        graph_file = os.path.join(data_path, data_name + "_" + str(f_id) + ".graphml")
        # get graph data
        graph = nx.read_graphml(graph_file)
        # get all node and edge labels of this graph
        all_node_labels = nx.get_node_attributes(graph, "label").values()
        all_edge_labels = nx.get_edge_attributes(graph, "label").values()
        graph_node_labels.append(np.unique(list(map(int, all_node_labels))))
        graph_edge_labels.append(np.unique(list(map(int, all_edge_labels))))
    unique_node_labels = [node_label for node_labels in graph_node_labels for node_label in node_labels]
    unique_node_labels = np.unique(unique_node_labels)
    unique_edge_labels = [edge_label for edge_labels in graph_edge_labels for edge_label in edge_labels]
    unique_edge_labels = np.unique(unique_edge_labels)
    # map old labels to new labels
    dict_node_label = {str(old_label): new_label for new_label, old_label in enumerate(unique_node_labels)}
    dict_edge_label = {str(old_label): new_label for new_label, old_label in enumerate(unique_edge_labels)}
    return dict_node_label, dict_edge_label

### main program ###

data_names = ["mutag", "nci1", "nci109", "enzymes", "dd"]

# convert graph from Graphml format to C# format (DIMACS format)
for data_name in data_names:
    print("Converting {}...".format(data_name))
    data_path = ".\datasets\gk\{}".format(data_name)
    # count number of graphml files
    n_file = len([f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))])
    dict_node_label, dict_edge_label = rename_label(data_name, data_path, n_file)
    graph_name = ".\datasets\gk\{}_graph.txt".format(data_name)
    with open(graph_name, "w") as f:
        for f_id in range(1, n_file + 1):
            graph_file = os.path.join(data_path, data_name + "_" + str(f_id) + ".graphml")
            graph = nx.read_graphml(graph_file)
            n_node = len(graph.nodes())
            g_id = f_id - 1
            f.write("t # {}\n".format(g_id))
            for node_id in range(n_node):
                node_name = "n"+str(node_id)
                node_label = int(graph.node[node_name]["label"])
                node_label = dict_node_label[str(node_label)] # get new node label
                f.write("v {} {}\n".format(node_id, node_label))
            duplicate_edges = []
            for node_id in range(n_node):
                node_name = "n" + str(node_id)
                node_neighbors = graph.neighbors(node_name)
                for neighbor_name in node_neighbors:
                    neighbor_id = neighbor_name[1:]
                    edge1 = str(node_id) + str(neighbor_id)
                    edge2 = str(neighbor_id) + str(node_id)
                    if edge1 not in duplicate_edges:
                        duplicate_edges.append(edge1)
                        duplicate_edges.append(edge2)
                        try:
                            edge_label = int(graph[node_name][neighbor_name]["label"])
                            edge_label = dict_edge_label[str(edge_label)] # get new edge label
                        except: # this edge doesn't have label
                            edge_label = 0
                        f.write("e {} {} {}\n".format(node_id, neighbor_id, edge_label))

# generate graph label
for data_name in data_names:
    label_path = ".\datasets\gk\{}.label".format(data_name)
    with open(label_path, "r") as f:
        line = f.read()
        labels = line.split()
    # get unique labels
    unique_labels = np.unique(labels)
    # map old labels to new labels
    dict_label = {str(old_label): new_label for new_label, old_label in enumerate(unique_labels)}
    label_name = ".\datasets\gk\{}_label.txt".format(data_name)
    with open(label_name, "w") as f:
        for g_id, label in enumerate(labels):
            new_label = dict_label[str(label)]
            f.write("{}\t{}\n".format(new_label, g_id))

