import numpy as np
import timeit
import datetime
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import subprocess

### represent a graph as a set of frequent subgraphs (FSGs)
### learn graph vectors using Doc2Vec (PV-DBOW model)
### use SVM as classifier


### variables ###
data_name = "mutag"
path = "./data/" + data_name
minSup = 0.35
dim = 128
n_run = 10

### functions ###
def mine_FSGs(file_graph, file_label, minSup, file_graph_fsg):
    subprocess.run("mono fsg_miner.exe -graphset {} -graphlabel {} -minsup {} -output {}".
                   format(file_graph, file_label, minSup, file_graph_fsg), shell=True)

# load graphs in the form of FSGs and their labels
def load_graph(file_graph_fsg):
    labels, graphs = [], []
    with open(file_graph_fsg) as f:
        for line in f:
            label, content = line.split("\t")
            if content != "\n":
                labels.append(label)
                graphs.append(content.rstrip().split(" "))
    return graphs, labels

# create a graph id for each graph
def assign_graph_id(graphs):
    graphs_with_ids = []
    for idx, val in enumerate(graphs):
        graph_id = "g_{}".format(idx)
        graphs_with_ids.append(TaggedDocument(val, [graph_id]))
    return graphs_with_ids

start_date_time = datetime.datetime.now()
start_time = timeit.default_timer()

print("### data: {}, minSup={}, dim={} ###".format(data_name, minSup, dim))
# mine FSGs and associate each graph with a set of FSGs
in_graph = path + "/{}_graph.txt".format(data_name)
in_graph_label = path + "/{}_label.txt".format(data_name)
out_graph_fsg = path + "/{}_graph_fsg_{}.txt".format(data_name, minSup)
mine_FSGs(in_graph, in_graph_label, minSup, out_graph_fsg)
# load graphs in the form of FSGs
data_fsg_path = path + "/{}_graph_fsg_{}.txt".format(data_name, minSup)
data_fsg_X, data_fsg_y = load_graph(data_fsg_path)
# assign a graph id to each graph
data_graph_X = assign_graph_id(data_fsg_X)
all_acc, all_mic, all_mac = [], [], []
for run in range(n_run):
    print("run={}".format(run))
    # learn graph vectors using Doc2Vec (PV-DBOW model)
    d2v_dbow = Doc2Vec(vector_size=dim, min_count=0, workers=16, dm=0, epochs=50)
    d2v_dbow.build_vocab(data_graph_X)
    d2v_dbow.train(data_graph_X, total_examples=d2v_dbow.corpus_count, epochs=d2v_dbow.iter)
    data_graph_vec = [d2v_dbow.docvecs[idx] for idx in range(len(data_graph_X))]
    del d2v_dbow  # delete unneeded model memory
    # generate train and test vectors using 10-fold CV
    train_graph_vec, test_graph_vec, train_graph_y, test_graph_y = \
        train_test_split(data_graph_vec, data_fsg_y, test_size=0.1, random_state=run, stratify=data_fsg_y)
    # tune parameters for SVM on train data
    C_range = 10. ** np.arange(-6, 8, 2)
    param_grid = dict(C=C_range)
    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
    grid = GridSearchCV(svm.LinearSVC(), param_grid=param_grid, cv=cv)
    grid.fit(train_graph_vec, train_graph_y)
    print("the best parameters are %s with a score of %0.2f" % (grid.best_params_, grid.best_score_))
    # classify test data
    g2v_svm = svm.LinearSVC(C=grid.best_params_["C"])
    g2v_svm.fit(train_graph_vec, train_graph_y)
    test_graph_pred = g2v_svm.predict(test_graph_vec)
    acc = accuracy_score(test_graph_y, test_graph_pred)
    mic = f1_score(test_graph_y, test_graph_pred, pos_label=None, average="micro")
    mac = f1_score(test_graph_y, test_graph_pred, pos_label=None, average="macro")
    all_acc.append(acc)
    all_mic.append(mic)
    all_mac.append(mac)
    # obtain accuracy and F1-scores
    print("accuracy: {}".format(np.round(acc, 4)))
    print("micro: {}".format(np.round(mic, 4)))
    print("macro: {}".format(np.round(mac, 4)))

print("avg accuracy: {} ({})".format(np.round(np.average(all_acc), 4), np.round(np.std(all_acc), 3)))
print("avg micro: {} ({})".format(np.round(np.average(all_mic), 4), np.round(np.std(all_mic), 3)))
print("avg macro: {} ({})".format(np.round(np.average(all_mac), 4), np.round(np.std(all_mac), 3)))

end_date_time = datetime.datetime.now()
end_time = timeit.default_timer()
print("start date time: {} and end date time: {}".format(start_date_time, end_date_time))
print("runtime: {}(s)".format(round(end_time-start_time, 2)))

