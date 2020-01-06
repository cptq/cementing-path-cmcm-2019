''' Slab class and dynamic programming algorithms for the three slab repair models.
'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
from constants import *

class Slab():
    def __init__(self, height=0, run=0, cross=0, W=DEFAULT_W, L=DEFAULT_L, broken=False,
            age=0, ft_cycles=0, carb_depth=0):
        self.height = height
        self.run = run
        self.cross = cross
        self.W = W
        self.L = L
        self.broken = broken
        self.age = age
        self.ft_cycles = ft_cycles
        self.carb_depth = carb_depth

def repairs_m1(slabs, htol=3, raise_rate=RAISE_RATE, replace_rate=REPLACE_RATE, cut_rate=CUT_RATE):
    ''' Model 1
        Assumes heights are integers
    '''
    def cost(h, slab):
        ''' Cost to raise or repair from current height to target height
        '''
        if slab.broken:
            return replace_rate*slab.W*slab.L
        elif h == slab.height:
            return 0
        elif slab.height-2 <= h < slab.height:
            return cut_rate*slab.L
        elif h > slab.height:
            return raise_rate*slab.W*slab.L
        else:
            return replace_rate*slab.W*slab.L

    min_h, max_h = min([s.height for s in slabs]), max([s.height for s in slabs])
    height_ran = list(range(min_h, max_h+1))
    M = [[np.inf for i in height_ran] for k in range(len(slabs))]

    for i, h in enumerate(height_ran):
        M[0][i] = cost(h, slabs[0])

    for k in range(1, len(slabs)):
        for i, h in enumerate(height_ran): # checking current height
            mini = np.inf
            for i_prev in range(max(i-htol, 0), min(i+htol, len(height_ran)-1)+1): # previous heights
                cost_k = cost(h, slabs[k]) + M[k-1][i_prev]
                mini = min(mini, cost_k)
            M[k][i] = mini

    min_cost = np.min(M[-1])
    return min_cost, M


def repairs_m2(slabs, road_runs, htol=3, rtol=6, raise_rate=RAISE_RATE, replace_rate=REPLACE_RATE, cut_rate=CUT_RATE):
    ''' Model 2
    '''
    def cost(h, run, slab):
        if slab.broken:
            return replace_rate*slab.W*slab.L
        elif h == slab.height and run == slab.run:
            return 0
        elif (slab.height-htol <= h <= slab.height) and ((slab.height-h-2)/slab.L <= run <= h/slab.L):
            return cut_rate*slab.L
        elif (h >= slab.height) and (h+run*slab.L >= slab.height+slab.run*slab.L):
            return raise_rate*slab.L*slab.W
        else:
            return replace_rate*slab.L*slab.W
    
    n = len(slabs)
    min_h, max_h = min([s.height for s in slabs]), max([s.height for s in slabs])
    height_ran = list(range(min_h-htol, max_h+htol+1))
    min_run, max_run = min([s.run for s in slabs]), max([s.run for s in slabs])
    min_run, max_run = min(min_run, min(road_runs)), max(max_run, max(road_runs))
    run_ran = list(range(min_run-rtol, max_run+rtol+1))
    M = [[[np.inf for j in run_ran] for i in height_ran] for k in range(n)]
    for i, h in enumerate(height_ran):
        for j, r in enumerate(run_ran):
            M[0][i][j] = cost(h, r, slabs[0])
    for k in range(1, n):
        for i, h in enumerate(height_ran): # cost of height h
            for j, r in enumerate(run_ran): # cost of run r
                mini = np.inf
                min_valid_h = h - slabs[k-1].L*slabs[k-1].run*CONV_RUN - htol
                max_valid_h = h - slabs[k-1].L*slabs[k-1].run*CONV_RUN + htol
                valid_prev_h = intv_to_range(height_ran, min_valid_h, max_valid_h)
                for i_prev in valid_prev_h:
                    for j_prev in range(max(road_runs[k]-rtol,0), min(road_runs[k]+rtol,
                        len(run_ran)-1)+1):
                        cost_t = cost(h, r, slabs[k]) + M[k-1][i_prev][j_prev]
                        mini = min(mini, cost_t)
                M[k][i][j] = mini

    min_cost = np.min(M[-1])
    return min_cost, M

def repairs_m3(slabs, road_runs, htol=3, rtol=6, ctol=3, raise_rate=RAISE_RATE, replace_rate=REPLACE_RATE, cut_rate=CUT_RATE):
    ''' Model 3
    '''
    def cost(h, run, cross, slab):
        if slab.broken:
            return replace_rate*slab.W*slab.L
        elif h == slab.height and run == slab.run:
            return 0
        elif (slab.height-htol <= h <= slab.height) and ((slab.height-h-2)/slab.L <= run <= h/slab.L):
            return cut_rate*slab.L
        elif (h >= slab.height) and (h+run*slab.L >= slab.height+slab.run*slab.L):
            return raise_rate*slab.L*slab.W
        else:
            return replace_rate*slab.L*slab.W
    
    n = len(slabs)
    min_h, max_h = min([s.height for s in slabs]), max([s.height for s in slabs])
    height_ran = list(range(min_h-htol, max_h+htol+1))
    min_run, max_run = min([s.run for s in slabs]), max([s.run for s in slabs])
    min_run, max_run = min(min_run, min(road_runs)), max(max_run, max(road_runs))
    run_ran = list(range(min_run-rtol, max_run+rtol+1))
    min_cross, max_cross = min([s.cross for s in slabs]), max([s.cross for s in slabs])
    cross_ran = list(range(min_cross-ctol, max_cross+ctol+1))
    M = [[[[np.inf for l in cross_ran] for j in run_ran] for i in height_ran] for k in range(n)]

    # initial values
    for i, h in enumerate(height_ran):
        for j, r in enumerate(run_ran):
            for l, c in enumerate(cross_ran):
                M[0][i][j][l] = cost(h, r, c, slabs[0])

    for k in range(1, n):
        for i, h in enumerate(height_ran): # height h
            for j, r in enumerate(run_ran): # run r
                for l, c in enumerate(cross_ran): # cross c
                    mini = np.inf
                    min_valid_h = h - slabs[k-1].L*slabs[k-1].run*CONV_RUN - htol
                    max_valid_h = h - slabs[k-1].L*slabs[k-1].run*CONV_RUN + htol
                    valid_prev_h = intv_to_range(height_ran, min_valid_h, max_valid_h)
                    for i_prev in valid_prev_h: 
                        prev_h = height_ran[i_prev]
                        for j_prev in range(max(road_runs[k]-rtol,0), min(road_runs[k]+rtol,
                                len(run_ran)-1)+1):
                            min_valid_cross = (h + c*slabs[k].W - prev_h - htol)/slabs[k-1].W
                            max_valid_cross = (h + c*slabs[k].W - prev_h + htol)/slabs[k-1].W
                            valid_prev_crosses = intv_to_range(cross_ran, min_valid_cross, max_valid_cross)
                            for l_prev in valid_prev_crosses:
                                cost_t = cost(h, r, c, slabs[k]) + M[k-1][i_prev][j_prev][l_prev]
                                mini = min(mini, cost_t)
                    M[k][i][j][l] = mini
    
    min_cost = np.min(M[-1])
    return min_cost, M

def intv_to_range(A, low, high):
    ''' returns list of indices k of A s.t. low <= A[k] <= high
        assumes A sorted
    '''
    mini_i, maxi_i = -1, -1
    for k, a in enumerate(A):
        if mini_i == -1 and a >= low:
            mini_i = k
        elif maxi_i == -1 and a > high:
            maxi_i = k-1
    if mini_i != -1 and maxi_i == -1:
        maxi_i = len(A)-1
    ret = list(range(mini_i, maxi_i+1))
    return ret
