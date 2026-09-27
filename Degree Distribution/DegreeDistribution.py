# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 16:47:10 2023

@author: zziya
"""
network_types=['sf', 'sw']
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import copy
import scipy.stats as st
import seaborn as sns
#参数列
network_type='sf'#'sf' or 'sw'
lam=3.5#3.5
mu=2.6#2.6, 3.7, 6.4
MU=[2.6, 3.7]
N=2000
#k = 8 or 16 or 24
Ks=[8, 16, 24]
#G=nx.random_regular_graph(k,N)
T=200
cs=['red', 'green', 'blue']
#函数列
#幂律分布随机数函数
def powerlaw_sample(alpha):
    xmin=1
    u=random.uniform(0,1)
    result=xmin*math.pow(u, 1/(1-alpha))
    if result>10000:
        return 10000
    #while result>1000:
        #u=random.uniform(0,1)
        #result=xmin*math.pow(u, 1/(1-alpha))
    return result
def delete_hidden(G,state):
    result=copy.deepcopy(G)
    for i in G.nodes:
        if state[i]==0:
            result.remove_node(i)
    return result
#初始化
plt.figure(figsize=(8,6))
skewnesses_mean=[]
kurtosises_mean=[]
#网络G的度分布
for k in Ks:
    if network_type=='sf':
        G=nx.generators.barabasi_albert_graph(N, int(k/2))
    if network_type=='sw':
        G=nx.generators.watts_strogatz_graph(N, k, 0.4)
    '''
    degrees=nx.degree_histogram(G)
    for z in range(len(degrees)):
        if z>int(k/2):
            plt.scatter(z, degrees[z]/float(sum(degrees)), s=30, c='black')#, label='Origin')
    plt.scatter(z, degrees[z]/float(sum(degrees)), s=30, c='black', label='Origin')
    degree_list=list(dict(G.degree()).values())
    '''
    skewnesses=[]
    kurtosises=[]
    comm=20
    comstep=10
    tnow=0
    next_transition={}#所有节点的下一次相变时间
    node_state={}#节点状态，1为活跃，0为不活跃
    for i in G.nodes:
        node_state[i]=int(0<random.uniform(0,1)<0.5)
        if node_state[i]==0:
            next_transition[i]=powerlaw_sample(lam)#幂律分布的随机数,参数为lam
        if node_state[i]==1:
            next_transition[i]=powerlaw_sample(mu)#幂律分布的随机数，参数为mu
    while (tnow<T):
        print("\r t = {:.2f}".format(tnow),end='    ')
        changer=min(next_transition.items(),key=lambda x: x[1])[0]
        tnow=next_transition[changer]
        if node_state[changer]==1:
            node_state[changer]=0
            next_transition[changer]+=powerlaw_sample(lam)#幂律分布的随机数，参数为lam
        elif node_state[changer]==0:
            node_state[changer]=1
            next_transition[changer]+=powerlaw_sample(mu)#幂律分布的随机数，参数为mu
        if tnow>comm:
            comm+=comstep
            g=delete_hidden(G, node_state)
            degrees=nx.degree_histogram(g)
            degree_list=list(dict(g.degree).values())
            skewnesses.append(st.skew(degree_list))
            kurtosises.append(st.kurtosis(degree_list))
            plt.scatter(range(len(degrees)), [z/float(sum(degrees)) for z in degrees], c=cs[Ks.index(k)], s=30, alpha=0.4)
    skewnesses_mean.append(np.mean(skewnesses))
    kurtosises_mean.append(np.mean(kurtosises))
    plt.scatter(range(len(degrees)), [z/float(sum(degrees)) for z in degrees], c=cs[Ks.index(k)], s=30, alpha=0.4, label='$k = {:d}$'.format(k))
plt.legend(fontsize=25)
plt.xlabel('$k$', fontsize=25)
plt.ylabel('$p(k)$', fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
if network_type=='sf':
    plt.xscale('log')
    plt.yscale('log')
if network_type=='sw':
    plt.xlim([0, 30])
    plt.ylim([0, 0.3])
plt.savefig(".\\saves\\{}_{:.2f}.pdf".format(network_type, mu), bbox_inches='tight',dpi=500)
plt.show()
print('skew:',skewnesses_mean)
print('kurtosis:',kurtosises_mean)