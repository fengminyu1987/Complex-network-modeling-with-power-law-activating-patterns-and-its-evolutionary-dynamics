# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 16:41:17 2024

@author: ziyan
"""
mu=2.6
lam=3.5
def ee(a):
    return (a-1)/(a-2)
q0=ee(mu)/(ee(mu)+ee(lam))
print(q0)