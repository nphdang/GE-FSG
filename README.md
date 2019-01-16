# GE-FSG: Learning Graph Embeddings via Frequent Subgraphs
This is the implementation of the GE-FSG method in the paper "Learning Graph Representation via Frequent Subgraphs", SDM 2018: https://epubs.siam.org/doi/10.1137/1.9781611975321.35

# Introduction
A graph consists of nodes and edges. Each graph has a label called graph label. Similarly, each node/edge can also has a label called node label/edge label. For example, a chemical compound is a graph whose nodes correspond to the atoms of the compound and edges correspond to chemical bonds.

To apply machine learning tasks such as classification and clustering to graphs, we need to represent each graph as a feature vector since machine learning methods typically require vectors as their input. This task is challenging since graphs have no feature vectors by default.

We propose GE-FSG which learns feature vectors (aka embeddings or representations) for graphs. GE-FSG combines a recently introduced neural document embedding model with a traditional pattern mining technique. It has two main steps: (1) decompose each graph into a set of frequent subgraphs (FSGs) and (2) learn an embedding for each graph by predicting its belonging FSGs. To this end, graphs which contain similar FSGs will be mapped to nearby points on the vector space. 

![GE-FSG: Main idea](https://github.com/nphdang/GE-FSG/blob/master/main_idea.jpg)

## Graph visualization demonstration
Graph embeddings learnt by GE-FSG and other methods are visualized using t-SNE.

![Graph visualization](https://github.com/nphdang/GE-FSG/blob/master/graph_visualization.jpg)

# Installation
1. Microsoft .NET Framework 4.0 (to run C# code to mine frequent subgraphs)
2. gensim 3.4 (to run Doc2Vec model)
3. networkx 2.1 (to read graphs in GraphML format)

# How to run
- Run python main.py to learn graph embeddings and classify graphs (note that you may need to change variables such as dataset, minimum support threshold, and embedding dimension in the code)
- Run python .\utilities\convert_graphs\gen_graph_dgk.py to convert graph format used by Deep Graph Kernel to graph format used by GE-FSG
- Run python .\utilities\convert_graphs\gen_graph_gk.py to convert graph format used by Graph Kernel Suite to graph format used by GE-FSG

# Tool to mine frequent subgraphs
- File fsg_miner.exe can be used as a standalone tool to discover frequent subgraphs
- It runs fast since it is implemented in parallel
- Its parameters are as follows:
        -graphset <file>
        use graphs from <file> to mine FSGs
        -graphlabel <file>
        obtain graph labels from <file>
        -minsup <float>
        set minimum support threshold in [0,1]; default is 0.5
        -fsg <file>
        save discovered FSGs to <file> (optional)
        -output <file>
        convert each graph to a set of FSGs and save it to <file> (optional)

# Reference
Dang Nguyen, Wei Luo, Tu Dinh Nguyen, Svetha Venkatesh, Dinh Phung (2018). Learning Graph Representation via Frequent Subgraphs. SDM 2018, San Diego, USA. SIAM, 306-314
