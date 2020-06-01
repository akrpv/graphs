import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import numpy as np


options = {
    'node_color': 'black',
    'line_color': 'grey',
    'node_size': 1,
    'width': 0.1,
    'font_size': 0
}


def generate_random_graph(n, k):
    deg_seq = [1]
    while sum(deg_seq) % 2 != 0:
        deg_seq = [random.randint(1, int(n * k)) for i in range(n)]
    return nx.configuration_model(deg_seq)
    # return nx.erdos_renyi_graph(n, 0.3)


def get_n(file_n):
    nodes = {
        1: 1000,
        2: 7000,
        3: 19588,
        4: 47104,
        5: 110971,
        6: 262144,
        7: 536108,
        8: 1864433,
        9: 7733822,
        10: 11950757
    }
    return nodes[file_n[0]]


def get_params(graph, a, b):
    n = graph.number_of_nodes()
    e = graph.number_of_edges()
    if (n * (n - 3) + 2) == 0:
        print(n)
    param = {}
    param['avg_degree'] = np.mean([d for n, d in graph.degree() if n in range(a, b + 1) and d > 1])
    param['density'] = 2 * (e - n + 1) / (n * (n - 3) + 2)
    return param


graph = generate_random_graph(100, 0.075)
print(graph.number_of_nodes())
n = graph.number_of_nodes()
p = 0.1
