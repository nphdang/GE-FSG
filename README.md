# GE-FSG: Learning Graph Embeddings via Frequent Subgraphs
This is the implementation of the GE-FSG method in the paper "Learning Graph Representation via Frequent Subgraphs", SDM 2018: https://epubs.siam.org/doi/10.1137/1.9781611975321.35

# Installation
1. Microsoft .NET Framework 4.0 (to run C# code to mine frequent subgraphs)
2. gensim 3.4 (to run Doc2Vec model)
3. networkx 2.1 (to read graphs in GraphML format)

# How to run
- Run python main.py to learn graph embeddings and classify graphs
- Run python .\utilities\convert_graphs\gen_graph_dgk.py to convert graph format used by Deep Graph Kernel to graph format used by GE-FSG
- Run python .\utilities\convert_graphs\gen_graph_gk.py to convert graph format used by Graph Kernel Suite to graph format used by GE-FSG

# Reference
Dang Nguyen, Wei Luo, Tu Dinh Nguyen, Svetha Venkatesh, Dinh Phung (2018). Learning Graph Representation via Frequent Subgraphs. SDM 2018, San Diego, USA. SIAM, 306-314
