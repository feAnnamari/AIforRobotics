# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:34:19 2019

@author: student
"""

import numpy as np

world = [['R','G','G','R','R'],
['R','R','G','R','R'],
['R','R','G','G','R'],
['R','R','R','R','R']]
world = np.asmatrix(world)
y = 4
x = 5
n = y*x
measurements = ['G','G','G','G','G']
motions = [[0,1],[1,0],[1,0],[0,1],[0,1]] # [0,1]:right [0,-1]:left [1,0]:down [-1,0]:up
pHit = 0.6
pMiss = 0.2
pExact = 0.8 #probability of moving exactly U cells
pOvershoot = 0.1 #probability of moving U+1 cells
pUndershoot = 0.1 #probability of moving U-1 cells

def init_p():
    places = np.full((y, x), 1/n)
    return places

"""
p = init_p()
print('\nThe uniform distribution:')
print(p)
"""

def sense(p, Z):
    if Z == 'R': 
        p[world == Z] *= pHit
        p[world != Z] *= pMiss
    if Z == 'G':
        p[world == Z] *= pHit
        p[world != Z] *= pMiss
    return p

"""
print('\nThe sense function called with red parameter:')
print(sense(p, 'R'))
print('\nThe sense function called with green parameter:')
print(sense(p, 'G'))

# :,0
U = [1,0]
"""

def move_inexact(p, U):
    
    if U[1] == 1: # vízszintes mozgás, sor
        for j in range(np.size(p,0)): #végig megy a sorokon
            q = []
            for i in range(np.size(p,1)): #végig megy az elemeken
                s = pExact * p[j,(i-U[1]) % np.size(p,1)]
                s = s + pOvershoot * p[j,(i-U[1]-1) % np.size(p,1)]
                s = s + pUndershoot * p[j,(i-U[1]+1) % np.size(p,1)]
                q.append(s)
            p[j,:] = np.asmatrix(q) #kicseréli a sor elemeit
        
    else: # függőleges mozgás, oszlop
        for j in range(np.size(p,1)): #végig megy az oszlopokon
            q = []
            for i in range(np.size(p,0)): #végig megy az elemeken
                s = pExact * p[(i-U[0] % np.size(p,0), j)]
                s = s + pOvershoot * p[(i-U[0]-1) % np.size(p,0), j]
                s = s + pUndershoot * p[(i-U[0]+1) % np.size(p,0), j]
                q.append(s)
            p[:,j] = np.asmatrix(q) #kicseréli az oszlop elemeit
    return p

"""
print('\nThe p list after the move_inexact function:')
print(move_inexact(p, U))

"""

p = init_p()
# add your cycle here #

for i in range(len(measurements)):
    p = sense(p, measurements[i])
    p = move_inexact(p, motions[i])
    message = '\nThe p list after sensing ' + measurements[i] + ' and moving ' + str(motions[i])
    print(message)
    print(p)

p = p/p.sum(keepdims=1)


def show(p):
    print('\n Result:')
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print ('[' + ',\n '.join(rows) + ']')
    
show(p)

"""
The calculated distribution should look like:
[[0.02459,0.01120,0.01838,0.04408,0.04028],
 [0.01882,0.00589,0.00937,0.04882,0.05713],
 [0.08765,0.01081,0.01266,0.11795,0.40596],
 [0.02760,0.00920,0.00470,0.01102,0.03391]]
"""