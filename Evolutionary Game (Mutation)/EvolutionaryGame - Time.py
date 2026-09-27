# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 16:47:10 2023

@author: zziya
"""
network_type='rrg'
#DB update rule, PD type game
#network_type=rgg, sw, sf
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import json
#参数列
lam=3.5#3.5
mu=3.7#2.6, 3.7, 6.4
delt=1#状态更新参数，Poisson过程参数
#<<<<<<<网络参数
N=100
k=4#平均度4, 8, 12, 16
#Random Regular Graph
if network_type=='rrg':
    G=nx.random_regular_graph(k, N)
#Watts Strogatz Small-world Network
if network_type=='sw':
    G=nx.generators.watts_strogatz_graph(N, k, 0.4)
#Barabasi Albert Scale-free network
#if network_type=='sf':
#    G=nx.generators.barabasi_albert_graph(N, k/2)
#<<<<<<<
n=1
b=2
tmax=10000
c=1
mutation_rate=0.1
#函数列
def powerlaw_sample(alpha):#控制随机数在1-10000
    xmin=1
    u=random.uniform(0,1)
    result=xmin*math.pow(u, 1/(1-alpha))
    if result>10000:
        return 10000
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
    f=fc+fd
    if f==0:
        return strategy[changer]
    probac=fc/f
    if 0<random.uniform(0,1)<=probac:
        return 0
    else:
        return 1
plt.figure(figsize=(8, 6))
#计算合作者固定概率
result_c={}
tlist=[]
for avg in range(n):
    investigator=0
    tnow=0
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
    fc=[]
    while (tnow<tmax):
        #print("\r b = {:.2f}, tnow = {:.2f}, nc = {:d}, n = {:d}, k = {:d}, lam = {:.2f}, mu = {:.2f}, Nc = {:d}".format(b, tnow, nc, avg, k ,lam, mu, density_c),end='        ')
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
            if random.uniform(0, 1)>mutation_rate:#不突变
                active_neis=[]
                for i in G.neighbors(changer):
                    if node_state[i]==1:
                        active_neis.append(i)
                if len(active_neis)!=0:
                    strategy[changer]=DB_updating(G, changer, node_state, strategy, b, c)
                    next_change_strategy[changer]+=random.expovariate(delt)
                else:
                    next_change_strategy[changer]+=random.expovariate(delt)
            else:#突变
                strategy[changer]=int(random.uniform(0,2))
                next_change_strategy[changer]+=random.expovariate(delt)
        density_c=(N-sum(strategy.values()))/N
        fc.append(density_c)
        tlist.append(tnow)
plt.figure(figsize=(8,8))
plt.plot(tlist,fc)
plt.xscale('log')
plt.xlabel('$t$', fontsize=20)
plt.ylabel('$p_C$', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#plt.ylim([-0.04, 1.04])
#plt.savefig('.\\saves\\fc_t_{}_{}_cinvade.pdf'.format(network_type, k), dpi=350, bbox_inches='tight')
plt.show()
plt.figure(figsize=(8, 6))
#计算背叛者固定概率
'''
result_c={}
for avg in range(n):
    tnow=0
    investigator=1
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
    tlist=[]
    fclist=[]
    #演化开始，全合作或全背叛就退出
    while (True):
        tlist.append(tnow)
        fclist.append(density_c/N)
        print("\r b = {:.2f}, tnow = {:.2f}, n = {:d}, k = {:d}, lam = {:.2f}, mu = {:.2f}, Nc = {:d}".format(b, tnow, avg, k ,lam, mu, density_c),end='        ')
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
            plt.plot(tlist,fclist, color='red', lw=2, linestyle='--', alpha=0.6)
            break
        if density_c==0:
            plt.plot(tlist,fclist, color='blue', lw=2, linestyle='--', alpha=0.6)
            break
plt.xscale('log')
plt.xlabel('$t$', fontsize=20)
plt.ylabel('$p_C$', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.ylim([-0.04, 1.04])
plt.savefig('.\\saves\\fc_t_{}_{}_dinvade.pdf'.format(network_type, k), dpi=350, bbox_inches='tight')
plt.show()'''