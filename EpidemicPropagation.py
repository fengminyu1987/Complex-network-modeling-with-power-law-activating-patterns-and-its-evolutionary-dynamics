# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 16:47:10 2023

@author: zziya
"""
network_type='rrg'
#SIS Propagation Model
#network_type=rrg, sw, sf
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import json
#参数列
lam=2.1
mu=2.1
delt=1#状态更新参数，Poisson过程参数
#<<<<<<<网络参数
N=1000
k=6#平均度
G=nx.random_regular_graph(k, N)
#<<<<<<<
n=1000
tnow=0
B=np.arange(1,12,1)
c=1
#函数列
def powerlaw_sample(alpha):#控制随机数在1-10000
    xmin=1
    u=random.uniform(0,1)
    result=xmin*math.pow(u, 1/(1-alpha))
    while result>10000:
        u=random.uniform(0,1)
        result=xmin*math.pow(u, 1/(1-alpha))
    return result
def get_fitness(G, changer, node_state, strategy, b, c):
    result=0
    w=0.01
    neis=G.neighbors(changer)
    for i in neis:
        if node_state[i]==1:
            if strategy[changer]==0 and strategy[i]==0:
                result+=(b-c)
            if strategy[changer]==0 and strategy[i]==1:
                result+=(-c)
            if strategy[changer]==1 and strategy[i]==0:
                result+=(b)
    return 1-w+w*result
def DB_updating(G, changer, node_state, strategy, b, c):
    neis=G.neighbors(changer)
    f=0
    fc=0
    fd=0
    for i in neis:
        if node_state[i]==1:
            if strategy[i]==0:
                fc+=get_fitness(G, i, node_state, strategy, b, c)
            if strategy[i]==1:
                fd+=get_fitness(G, i, node_state, strategy, b, c)
            f+=get_fitness(G, i, node_state, strategy, b, c)
    if f==0:
        return strategy[changer]
    probac=fc/f
    if 0<random.uniform(0,1)<=probac:
        return 0
    else:
        return 1
#计算合作者固定概率
result_c={}
for b in B:
    nc=0
    for avg in range(n):
        investigator=0
        #初始化
        next_transition={}#所有节点的下一次相变时间
        node_state={}#节点状态，1为活跃，0为不活跃
        next_change_strategy={}#活跃节点下一次更新策略的时刻
        strategy={}
        invader=random.choice(list(G.nodes))
        for i in G.nodes:
            node_state[i]=int(0<random.uniform(0,1)<0.5)
            if node_state[i]==0:
                next_transition[i]=powerlaw_sample(lam)#幂律分布的随机数,参数为lam
            if node_state[i]==1:
                next_transition[i]=powerlaw_sample(mu)#幂律分布的随机数，参数为mu
                next_change_strategy[i]=random.expovariate(delt)
            if i==invader:
                strategy[i]=investigator
            else:
                strategy[i]=int(1-investigator)
        density_c=N-sum(strategy.values())
        #演化开始，全合作或全背叛就退出
        while (True):
            print("\r b = {:.2f}, tnow = {:.2f}, nc = {:d}, n = {:d}, k = {:d}, lam = {:.2f}, mu = {:.2f}, Nc = {:d}".format(b, tnow, nc, avg, k ,lam, mu, density_c),end='        ')
            state_transition_time=min(next_transition.values())
            strategy_transition_time=min(next_change_strategy.values())
            if state_transition_time<strategy_transition_time:#更新节点状态
                changer=min(next_transition.items(),key=lambda x: x[1])[0]
                tnow=next_transition[changer]
                if node_state[changer]==1:#变得不活跃
                    node_state[changer]=0
                    next_change_strategy.pop(changer)
                    next_transition[changer]+=powerlaw_sample(lam)#幂律分布的随机数，参数为lam
                elif node_state[changer]==0:#变得活跃
                    node_state[changer]=1
                    next_change_strategy[changer]=tnow+random.expovariate(delt)
                    next_transition[changer]+=powerlaw_sample(mu)#幂律分布的随机数，参数为mu
            if state_transition_time>strategy_transition_time:#更新策略
                changer=min(next_change_strategy.items(),key=lambda x: x[1])[0]
                tnow=next_change_strategy[changer]
                test=list(G.neighbors(changer))
                active_neis=[]
                for i in G.neighbors(changer):
                    if node_state[i]==1:
                        active_neis.append(i)
                if len(active_neis)!=0:
                    strategy[changer]=DB_updating(G, changer, node_state, strategy, b, c)
                    next_change_strategy[changer]+=random.expovariate(delt)
                else:
                    next_change_strategy[changer]+=random.expovariate(delt)
            density_c=N-sum(strategy.values())
            if density_c==N:
                nc=nc+1
                break
            if density_c==0:
                break
    result_c['{:.2f}.'.format(b)]=nc/n
json_str=json.dumps(result_c)
with open('.\\saves\\rhoc_{:.2f}_{:.2f}_{}_{:d}.json'.format(lam,mu,network_type,k), 'w') as json_file:
    json_file.write(json_str)