Each folder has two files: (1) "xxx_graph.txt" contains a set of graphs and (2) "xxx_label.txt" contains their corresponding graph labels, where "xxx" is a dataset name.

Each graph in "xxx_graph.txt" has the following format:
```
      t # <graph_id>
      v <node_id> <node_label>
      e <node_id_1> <node_id_2> <edge_label>
```

Each row in "xxx_label.txt" has the following format:
```
      <graph_label> <tab> <graph_id>
```
