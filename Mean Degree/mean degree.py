# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 16:47:10 2023
lam,mu = 2.6, 3.5, 6.4
@author: zziya
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import copy
from scipy.special import comb
import json
def get_active_subgraph(G,node_state):
    g_temp=copy.deepcopy(G)
    remove_set=[k for k,v in node_state.items() if v==0]
    g_temp.remove_nodes_from(remove_set)
    return g_temp
#参数列
lam=3.5
LAM=np.linspace(2.6,6.4,25)
mu=2.6
MU=[2.6, 3.5, 6.4]
N=500
k=4
T=300
comm=50
REAL=['infect-dublin','mammalia-voles','bn-mouse_visual-cortex_2']
GENERATED=['ban','wsn']
network='wsn'
if network == 'ban':
    G=nx.generators.barabasi_albert_graph(N, int(k/2))
if network == 'wsn':
    G=nx.generators.watts_strogatz_graph(N, 4, .4)
if network in REAL:
    filename='.\\saves\\nets\\'+network+'.txt'
    G=nx.Graph()
    with open(filename) as file:
        for line in file:
            head, tail=[str(x) for x in line.split()]
            G.add_edge(int(head),int(tail))
    N=G.number_of_nodes()
colors=['red', 'green', 'blue']
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
'''
component_result={}
for mu in MU:
    temp_component=[]
    for lam in LAM:
        next_transition={}#所有节点的下一次相变时间
        node_state={}#节点状态，1为活跃，0为不活跃
        size_record=[]
        tnow=0
        T_record=[]
        for i in G.nodes:
            node_state[i]=int(0<random.uniform(0,1)<0.5)
            if node_state[i]==0:
                next_transition[i]=powerlaw_sample(lam)#幂律分布的随机数,参数为lam
            if node_state[i]==1:
                next_transition[i]=powerlaw_sample(mu)#幂律分布的随机数，参数为mu
        active=sum(node_state.values())
        print("\r MEAN DEGREE net : {}, lam : {:.2f}, mu : {:.2f}".format(network,lam,mu), end='      ')
        component_list=[]
        while (tnow<T):
            changer=min(next_transition.items(),key=lambda x: x[1])[0]
            tnow=next_transition[changer]
            T_record.append(tnow)
            if node_state[changer]==1:
                node_state[changer]=0
                next_transition[changer]+=powerlaw_sample(lam)#幂律分布的随机数，参数为lam
                active=active-1
            elif node_state[changer]==0:
                node_state[changer]=1
                next_transition[changer]+=powerlaw_sample(mu)#幂律分布的随机数，参数为mu
                active=active+1
            if tnow>50:
                g=get_active_subgraph(G,node_state)
                #glargest=max(nx.connected_components(g),key=len)
                component_list.append(2*g.number_of_edges()/g.number_of_nodes())
        temp_component.append(np.mean(np.array(component_list)))
    component_result['{:.2f}'.format(mu)]=temp_component
json_str=json.dumps(component_result)
with open('.\\saves\\{}.json'.format(network), 'w') as json_file:
    json_file.write(json_str)'''
plt.figure(figsize=(8,8))
filename1='.\\saves\\{}.json'.format(network)
f1=open(filename1)
data1=json.load(f1)
for mu in MU:
    tep=data1["{:.2f}".format(mu)]
    plt.plot(LAM, tep, c=colors[MU.index(mu)],label='$\mu={:.2f}$'.format(mu),marker='o',linestyle='--',markersize=13,lw=2.5)
if network=='wsn':
    plt.ylabel('$<k>$', fontsize=20)
    plt.legend(fontsize=20)
if network == 'bn-mouse_visual-cortex_2':
    plt.ylabel('$<k>$', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#plt.ylim([0,1])
plt.xlabel('$\lambda$', fontsize=20)
#plt.xscale('log')
plt.savefig('.\\saves\\{}.pdf'.format(network), bbox_inches='tight', dpi=500)
plt.show()