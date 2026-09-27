# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:58:26 2023
Fixation probability plot for evolutionary games
@author: zziya
"""
import json
import matplotlib.pyplot as plt
import numpy as np
import math
N=1000
lam=3.5
mu=2.6
MU=[2.60, 3.70]
filenames=['americanfootball','ca-sandi_auths','contiguous-usa','dolphins','rt-retweet']
filename='contiguous-usa'
Cs=['red','blue']
B=np.linspace(1,10,15)
plt.figure(figsize=(8,6))
for mu in MU:
    q0=(((mu-1)/(mu-2))/((lam-1)/(lam-2)+(mu-1)/(mu-2)))
    filename1=".\\saves\\rhoc_"+"{:.2f}_".format(lam)+"{:.2f}_".format(mu)+filename
    filename2=".\\saves\\rhod_"+"{:.2f}_".format(lam)+"{:.2f}_".format(mu)+filename
    f1=open("{}.json".format(filename1))
    rhoc=json.load(f1)
    f2=open("{}.json".format(filename2))
    rhod=json.load(f2)
    c=[]
    d=[]
    for b in B:
        c.append(rhoc['{:.2f}'.format(b)])
        d.append(rhod['{:.2f}'.format(b)])
    plt.scatter(B, np.array(c)-np.array(d),s=120, color = Cs[MU.index(mu)],marker='^', label = '$\\mu = {:.2f}$'.format(mu))
    #p2=(1-math.pow(1-q0,k))/k
    #bc=(N-2)/(N*p2-2)#Theoretical result
    #plt.axvline(bc, color = Cs[MU.index(mu)], alpha=1, linestyle='-.')
    result=np.array(c)-np.array(d)
    z1=np.polyfit(B, result, 1)
    p1=np.poly1d(z1)
    plt.plot(np.linspace(1,10,15), p1(np.linspace(1,10,15)),color = Cs[MU.index(mu)], lw=2)
plt.xlim([0, 11])
plt.ylim([-0.03, 0.02])
plt.plot([0,11], [0,0],c='grey', linestyle='--',lw=2)
plt.xlabel("$b$", fontsize=20)
plt.xticks(fontsize=20)
if filename=='dolphins':
    plt.ylabel("$\\rho_C-\\rho_D$",fontsize=20)
    plt.legend(fontsize=20)
if filename=='rt-retweet':
    plt.ylabel("$\\rho_C-\\rho_D$",fontsize=20)
plt.yticks(fontsize=20)
plt.grid()
plt.savefig(".\\saves\\{}.pdf".format(filename), dpi=500, bbox_inches='tight')
plt.show()