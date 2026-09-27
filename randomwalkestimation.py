# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 16:47:10 2023

@author: zziya
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import copy
#参数列
lam=3.5
mu=2.6
N=100
k=4
print((((mu-1)/(mu-2))/((lam-1)/(lam-2)+(mu-1)/(mu-2)))*N)
q0=((mu-1)/(mu-2))/((lam-1)/(lam-2)+(mu-1)/(mu-2))
G=nx.random_regular_graph(k,N)
T=250
tnow=0
#函数列
#幂律分布随机数函数
def powerlaw_sample(alpha):
    xmin=1
    u=random.uniform(0,1)
    result=xmin*math.pow(u, 1/(1-alpha))
    while result>100000:
        u=random.uniform(0,1)
        result=xmin*math.pow(u, 1/(1-alpha))
    return result
def delete_hidden(G,state):
    result=copy.deepcopy(G)
    for i in G.nodes:
        if state[i]==0:
            result.remove_node(i)
    return result
def count_random_walk_proba(i,j,G,state):
    neis=G.neighbors(i)
    actneis=0
    for k in neis:
        if state[k]==1:
            actneis+=1
    if state[j]==0:
        return 0
    else:
        return 1/(actneis)
#初始化
next_transition={}#所有节点的下一次相变时间
node_state={}#节点状态，1为活跃，0为不活跃
RWP={}
for i in G.nodes:
    node_state[i]=int(0<random.uniform(0,1)<0.5)
    if node_state[i]==0:
        next_transition[i]=powerlaw_sample(lam)#幂律分布的随机数,参数为lam
    if node_state[i]==1:
        next_transition[i]=powerlaw_sample(mu)#幂律分布的随机数，参数为mu
active=sum(node_state.values())
while (tnow<T):
    print("\r t = {:.2f}, N_1(t) = {:d}".format(tnow, active),end='    ')
    changer=min(next_transition.items(),key=lambda x: x[1])[0]
    tnow=next_transition[changer]
    if node_state[changer]==1:
        node_state[changer]=0
        next_transition[changer]+=powerlaw_sample(lam)#幂律分布的随机数，参数为lam
        active=active-1
    elif node_state[changer]==0:
        node_state[changer]=1
        next_transition[changer]+=powerlaw_sample(mu)#幂律分布的随机数，参数为mu
        active=active+1
    if tnow>100:
        for i in G. nodes:
            for j in G.neighbors(i):
                if node_state[i]==1:
                    if (i,j) not in RWP.keys():
                        RWP[(i,j)]=[count_random_walk_proba(i,j,G,node_state)]
                    else:
                        RWP[(i,j)].append(count_random_walk_proba(i,j,G,node_state))
rs=[]
for i in G.nodes:
    for j in G.neighbors(i):
        print(np.mean(RWP[(i,j)]))
        rs.append(np.mean(RWP[(i,j)]))
print('============')
l=np.mean(rs)
print(l)
print(1/k-(1-q0)**k/k)
print((N-2)/(N*l-2))