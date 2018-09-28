import pickle
from collections import Counter
import numpy as np

### convert graphs from Python format used by Deep Graph Kernel (http://www.mit.edu/~pinary/kdd/)
### to C# format used by Parallel gSpan (https://link.springer.com/chapter/10.1007/978-3-319-17996-4_15)

# load graph dataset in Python format
def load_data(ds_name):
    with open(ds_name, "rb") as f:
        data = pickle.load(f, encoding='latin1')
        graph_data = data["graph"]
        labels = data["labels"]
        labels  = np.array(labels, dtype = np.int)
    return graph_data, labels

# print graph dataset statistic
def printDataset(ds):
    print("Reading dataset:", ds)
    ds_name = ".\datasets\deep_gk\{}.graph".format(ds)
    graphs, labels = load_data(ds_name)
    if ds == "proteins":
        labels = labels[0]
    print("Length: %s, Label distribution: %s" % (len(graphs), Counter(labels)))
    avg_nodes = []
    for gidx, nodes in graphs.items():
        avg_nodes.append(len(nodes))
    print("Avg #nodes: %s, Median #nodes: %s, Max #nodes: %s, Min #nodes: %s" %
          (np.mean(avg_nodes), np.median(avg_nodes), max(avg_nodes), min(avg_nodes)))

# rename node labels, node label starts from 0
def rename_node_label(graphs):
    # this is a list of lists where each element is a list of unique node labels of a graph
    graph_node_labels = []
    for gidx, graph in graphs.items():
        # get all node labels of this graph
        all_node_labels = []
        for nidx, node in graph.items():
            nlabel = 0 if node["label"] == "" else node["label"][0]  # each node has only one label
            all_node_labels.append(nlabel)
        graph_node_labels.append(np.unique(all_node_labels))
    # convert a list of lists to a list
    unique_node_labels = [node_label for node_labels in graph_node_labels for node_label in node_labels]
    unique_node_labels = np.unique(unique_node_labels)
    # map old labels to new labels
    dict_node_label = {str(old_label): new_label for new_label, old_label in enumerate(unique_node_labels)}
    return dict_node_label

# create node labels, node label is the degree
def create_node_label(graphs):
    # this is a list of lists where each element is a list of unique node labels of a graph
    graph_node_labels = []
    for gidx, graph in graphs.items():
        # get all node labels of this graph
        all_node_labels = []
        for nidx, node in graph.items():
            nlabel = len(node["neighbors"]) # each node has no label
            node["label"] = nlabel
            all_node_labels.append(nlabel)
        graph_node_labels.append(np.unique(all_node_labels))
    # convert a list of lists to a list
    unique_node_labels = [node_label for node_labels in graph_node_labels for node_label in node_labels]
    unique_node_labels = np.unique(unique_node_labels)
    # map old labels to new labels
    dict_node_label = {str(old_label): new_label for new_label, old_label in enumerate(unique_node_labels)}
    return dict_node_label


### main program ###

dataset1 = ["mutag", "ptc", "enzymes", "proteins", "nci1", "nci109"]
dataset2 = ["imdb_binary", "imdb_multi"]

# print statistic of graph datasets
dataset = dataset1 + dataset2
for ds in dataset:
    printDataset(ds)

# convert graph from Python format to C# format (DIMACS format)
# graphs have node labels
for ds in dataset1:
    print("Converting {}...".format(ds))
    ds_name = ".\datasets\deep_gk\{}.graph".format(ds)
    graphs, labels = load_data(ds_name)
    dict_node_label = rename_node_label(graphs)
    graph_name = ".\datasets\deep_gk\{}_graph.txt".format(ds)
    with open(graph_name, "w") as f:
        for gidx, graph in graphs.items():
            f.write("t # {}\n".format(gidx))
            for nidx, node in graph.items():
                nlabel = 0 if node["label"] == "" else dict_node_label[str(node["label"][0])] # each node has only one label
                f.write("v {} {}\n".format(nidx, nlabel))
            duplicate_edges = []
            for nidx, node in graph.items():
                neighbors = node["neighbors"]
                for nei_idx in neighbors:
                    edge1 = str(nidx) + str(nei_idx)
                    edge2 = str(nei_idx) + str(nidx)
                    if edge1 not in duplicate_edges:
                        duplicate_edges.append(edge1)
                        duplicate_edges.append(edge2)
                        f.write("e {} {} 0\n".format(nidx, nei_idx)) # each edge has default label of 0
    label_name = ".\datasets\deep_gk\{}_label.txt".format(ds)
    if ds == "proteins": # fix error
        labels = labels[0]
    with open(label_name, "w") as f:
        for gidx, glabel in enumerate(labels):
            f.write("{}\t{}\n".format(glabel, gidx))

# graphs don't have node labels => label of a node is its degree
for ds in dataset2:
    print("Converting {}...".format(ds))
    ds_name = ".\datasets\deep_gk\{}.graph".format(ds)
    graphs, labels = load_data(ds_name)
    dict_node_label = create_node_label(graphs)
    graph_name = ".\datasets\deep_gk\{}_graph.txt".format(ds)
    with open(graph_name, "w") as f:
        for gidx, graph in graphs.items():
            f.write("t # {}\n".format(gidx))
            for nidx, node in graph.items():
                nlabel = dict_node_label[str(node["label"])]
                f.write("v {} {}\n".format(nidx, nlabel))
            duplicate_edges = []
            for nidx, node in graph.items():
                neighbors = node["neighbors"]
                for nei_idx in neighbors:
                    edge1 = str(nidx) + str(nei_idx)
                    edge2 = str(nei_idx) + str(nidx)
                    if edge1 not in duplicate_edges:
                        duplicate_edges.append(edge1)
                        duplicate_edges.append(edge2)
                        f.write("e {} {} 0\n".format(nidx, nei_idx)) # each edge has default label of 0
    label_name = ".\datasets\deep_gk\{}_label.txt".format(ds)
    with open(label_name, "w") as f:
        for gidx, glabel in enumerate(labels):
            f.write("{}\t{}\n".format(glabel, gidx))



