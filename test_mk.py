import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import pytest
from collections import Counter
import numpy as np
from mk import generate_random_graph, get_n, get_params
file_number = [0]
n = [1000]
p = [0.9, 1]
q = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.2, 0.3, 0.4, 0.5]
k = [1]
options = {
    'node_color': 'black',
    'line_color': 'grey',
    'node_size': 1,
    'width': 0.1,
    'font_size': 0
}


def idfn_n(val):
    if file_number[0] == 0:
        return "[n={0}]".format(str(val))
    else:
        return "[n={0}]".format(str(get_n(file_number)))


def idfn_p(val):
    return "[p={0}]".format(str(val))


def idfn_q(val):
    return "[q={0}]".format(str(val))


@pytest.mark.parametrize("n", n, ids=idfn_n)
@pytest.mark.parametrize("file_n", file_number)
@pytest.mark.parametrize("p", p, ids=idfn_p)
@pytest.mark.parametrize("q", q, ids=idfn_q)
@pytest.mark.parametrize("k", k)
def test_mk(n, file_n, p, q, k):
    # n (int) – The number of nodes.
    # p (float) – The percentage of subgraph out of graph
    # q (float) – The percentage of subsubgraph out of subgraph
    # k (int) - The number of attemts of Monte Carlo method
    k = int(1 / p / q)
    if file_n == 0:
        graph = generate_random_graph(n, 0.075)
    else:
        graph = nx.Graph()
        with open('data/' + str(file_n) + '.txt') as fo:
            for rec in fo:
                a, b = map(int, rec.split())
                graph.add_edge(a, b)
        n = graph.number_of_nodes()

    main_params = get_params(graph, 0, n + 1)
    e = graph.edges([x for x in range(int(n * p))])
    s = [(x, y) for (x, y) in e if x < int(n * p) and y < int(n * p)]
    subgraph = nx.Graph(s)

    temp_params = {}
    for i in range(k):
        r = random.randint(0, int(n * p) - int(n * p * q))
        e = subgraph.edges([x for x in range(r, r + int(n * p * q))])
        s = [(x, y) for (x, y) in e if x >= r and x < r + int(n * p * q)]
        subsubgraph = nx.Graph(s)
        temp_params = dict(Counter(temp_params) + Counter(get_params(subsubgraph, r, r + int(n * p * q))))
    temp_params = {t: x / k for t, x in temp_params.items()}
    print(abs(temp_params['avg_degree'] - main_params['avg_degree']) / main_params['avg_degree'] * 100)
    print(temp_params['avg_degree'], main_params['avg_degree'])
    assert abs(temp_params['avg_degree'] - main_params['avg_degree']) / main_params['avg_degree'] * 100 < 20
