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
#参数列
lam=3.5
mu=2.6
MU=[2.6, 3.5, 6.4]
N=1000
k=8
G=nx.random_regular_graph(k,N)
T=600
comm=50
network='ban'
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
plt.figure(figsize=(8,6))
for mu in MU:
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
    while (tnow<T):
        print("\r t = {:.2f}, N_1(t) = {:d}".format(tnow, active),end='    ')
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
        if tnow>comm:
            size_record.append(active)
    counter={}
    for i in size_record:
        if i not in counter.keys():
            counter[i]=1
        else:
            counter[i]+=1
    #实验值
    for i in counter.keys():
        counter[i]/=len(size_record)
        plt.scatter(i, counter[i], c=colors[MU.index(mu)], s=60)
    plt.scatter(i, counter[i], c=colors[MU.index(mu)], s=60, label='{} = {:.2f}'.format(chr(956), mu))
    #理论值
    ys=[]
    xs=list(counter.keys())
    xs.sort()
    for i in xs:
        term1=np.log(comb(N, i))
        term2=i*np.log((mu-1)*(lam-2))
        term3=(N-i)*np.log((lam-1)*(mu-2))
        term4=N*np.log((mu-1)*(lam-2)+(lam-1)*(mu-2))
        ys.append(np.exp(term1+term2+term3-term4))
    plt.plot(xs, ys, c='black', lw=2.5)
    #打印KL散度
    kl=0
    for i in xs:
        kl+=counter[i]*np.log(counter[i]/ys[xs.index(i)])
    print("KL = {:.3f}\n".format(kl),end=" ")
plt.xlim([200, 800])
plt.ylim([0, 0.03])
plt.xlabel("$N_1$", fontsize=25)
plt.ylabel("$P$", fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=18,loc='best')
plt.savefig("./saves/{:.2f}.pdf".format(lam), dpi=500,bbox_inches='tight')
plt.show()