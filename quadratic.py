from gurobipy import *  
import numpy as np

def dist(loc, i, j):
    return np.linalg.norm(np.array(loc[i])-np.array(loc[j]))

# Create a new model
m = Model("Quadratic Semi-Assignment Problem")
#locations of worksites
loc = [[277, 302], [340, 304], [432, 281], [463, 171], [467, 154], [573, 225], [481, 237]
, [455, 276], [501, 347], [417, 362], [367, 383], [366, 411], [472, 388], [476, 420], [563, 492], 
[606, 334], [631, 367], [673, 405], [721, 374], [710, 401], [402, 482]]
s = len(loc) 
# prespecify the number of clusters desired  
k = 3
# Create binary variables

#add vars
vv = m.addVars(s, k, vtype=GRB.BINARY)

# Set Objective
obj = QuadExpr()
for w in range(k):
    for i in range(s):
        for j in range(i+1, s):
            obj.add(vv[i, w]*vv[j, w]*dist(loc, i, j))

#obj.add()   
m.setObjective(obj, GRB.MINIMIZE)

# Add constraints
for i in range(s):
    expr = vv.sum(i, '*')
    m.addConstr(expr, GRB.EQUAL, 1)

# Optimize model
m.optimize()

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)

