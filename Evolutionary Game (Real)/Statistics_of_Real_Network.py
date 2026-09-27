# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 00:08:03 2023

@author: zziya
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import json
import copy
filenames=['arenas-email','infect-dublin','petster-hamster-household','dimacs10-netscience','mammalia-voles']
filenames=['mammalia-voles']
for filename in filenames:
    file='.\\saves\\{}\\{}.txt'.format(filename,filename)
    G=nx.Graph()
    with open(file) as file:
        for line in file:
            head, tail=[str(x) for x in line.split()]
            G.add_edge(int(head),int(tail))
    if filename=='petster-hamster-household' or filename=='dimacs10-netscience':
        components=nx.connected_components(G)
        max_component=max(components, key=len)
        G_temp=G.subgraph(max_component)
        G=G_temp
    print('===================================================')
    print(filename)
    print("N:", nx.number_of_nodes(G))
    print("<k>: ", 2*G.number_of_edges()/G.number_of_nodes())
    print("Density: ", nx.density(G))
    print("Clustering:",nx.average_clustering(G))
    print("Average Path:",nx.average_shortest_path_length(G))
    print("Diameter:", nx.diameter(G))
    print("Assortativity:",nx.degree_assortativity_coefficient(G))