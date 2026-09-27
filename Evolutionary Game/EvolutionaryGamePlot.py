# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:58:26 2023
Fixation probability plot for evolutionary games
@author: zziya
lam=3.5
mu=2.6, 3.7, 6.4
network_type='sw' or 'rrg'
"""
import json
import matplotlib.pyplot as plt
import numpy as np
import math
lam=3.5
mu=2.6
N=100
MU=[2.6]#, 3.7, 6.4]
network_type='rrg'
Ks=[4, 8]
Cs=['red', 'blue', 'green', 'black']
Ms=['^','o','+','s']
B=np.arange(1,20,1)
NTs=['rrg', 'sw']
for mu in MU:
    for network_type in NTs:
        q0=(((mu-1)/(mu-2))/((lam-1)/(lam-2)+(mu-1)/(mu-2)))
        plt.figure(figsize=(8,6))
        for k in Ks:
            filename1="rhoc_"+"{:.2f}_".format(lam)+"{:.2f}_".format(mu)+network_type+"_{:d}".format(k)
            filename2="rhod_"+"{:.2f}_".format(lam)+"{:.2f}_".format(mu)+network_type+"_{:d}".format(k)
            f1=open(".\\saves\\{:d}\\{}\\{}.json".format(N,network_type, filename1))
            rhoc=json.load(f1)
            f2=open(".\\saves\\{:d}\\{}\\{}.json".format(N,network_type, filename2))
            rhod=json.load(f2)
            c=[]
            d=[]
            for b in B:
                c.append(rhoc['{:.2f}'.format(b)])
                d.append(rhod['{:.2f}'.format(b)])
            plt.scatter(B, np.array(c)-np.array(d),s=90, color = Cs[Ks.index(k)],marker=Ms[Ks.index(k)], label = '$k = {:d}$'.format(k))
            result=np.array(c)-np.array(d)
            z1=np.polyfit(B, result, 1)
            p1=np.poly1d(z1)
            plt.plot(np.arange(1, 20, 0.1), p1(np.arange(1, 20, 0.1)),color = Cs[Ks.index(k)], lw=2)
            p2=(1-math.pow(1-q0,k))/k
            bc=(N-2)/(N*p2-2)#Theoretical result
            plt.axvline(bc, color = Cs[Ks.index(k)], alpha=1, linestyle='-.')
            #plt.axvline(k*(mu-1)*(lam-2)/((mu-1)*(lam-2)+(lam-1)*(mu-2)), color = Cs[Ks.index(k)], alpha=1, linestyle='dotted')
        plt.xlim([0, 20])
        plt.ylim([-0.08, 0.08])
        plt.plot([0,20], [0,0],c='grey', linestyle='--',lw=2)
        plt.xlabel("$b$", fontsize=20)
        plt.xticks(fontsize=18)
        plt.ylabel("$\\rho_C-\\rho_D$",fontsize=20)
        plt.yticks(fontsize=18)
        plt.legend(fontsize=20)
        plt.savefig(".\\saves\\{}_{:.2f}_{:d}.pdf".format(network_type, mu,N),dpi=500, bbox_inches='tight')
        #plt.grid()
        plt.show()