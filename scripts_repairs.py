import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
from constants import *
from repairs import *

def main():
    # test model 1
    heights1 = [1,2,52,49,47,45,43,41]
    slabs = [Slab(height=h) for h in heights1]
    min_cost1, M1 = repairs_m1(slabs)
    print("Cost:", min_cost1, "| All replace cost:", len(heights1)*REPLACE_RATE*DEFAULT_W*DEFAULT_L)
    heights2 = np.random.randint(0,100, size=100)
    slabs = [Slab(height=h) for h in heights2]
    min_cost2, M2 = repairs_m1(slabs)
    print("Cost:", min_cost2, "| All replace cost:", len(heights2)*REPLACE_RATE*DEFAULT_W*DEFAULT_L)

    # test model 2
    num_slabs = 100
    slabs = []
    for k in range(num_slabs):
        h = np.random.randint(0,100)
        r = 0 # all same run
        slab = Slab(height=h, run=r)
        slabs.append(slab)
    road_runs = [0]*num_slabs
    min_cost, M = repairs_m2(slabs, road_runs)
    print("Cost:", min_cost, "| All replace cost:", num_slabs*REPLACE_RATE*DEFAULT_W*DEFAULT_L)

    num_slabs = 100
    slabs = []
    for k in range(num_slabs):
        h = np.random.randint(1,100)
        r = np.random.randint(-1,1)
        slab = Slab(height=h, run=r)
        slabs.append(slab)
    road_runs = [0]*num_slabs
    min_cost, M = repairs_m2(slabs, road_runs)
    print("Cost:", min_cost, "| All replace cost:", num_slabs*REPLACE_RATE*DEFAULT_W*DEFAULT_L)

    # test model 3
    num_slabs = 100
    slabs = []
    for k in range(num_slabs):
        h = np.random.randint(0,10)
        r = np.random.randint(-1,1)
        c = np.random.randint(-1,1)
        slab = Slab(height=h, run=r, cross=c)
        slabs.append(slab)
    min_cost, M = repairs_m3(slabs, road_runs)
    print("Cost:", min_cost, "| All replace cost:", num_slabs*REPLACE_RATE*DEFAULT_W*DEFAULT_L)


def p1_plot(num_slab_ran=range(30,100,3), height_ran=(0,10)):
    data = []
    iters = 30
    for n in num_slab_ran:
        level = []
        for i in range(iters):
            slabs = [Slab(height=h) for h in np.random.randint(height_ran[0], height_ran[1], size=n)]
            for slab in random.sample(slabs, int(np.round(BROKEN_RATE*len(slabs)+
                        np.random.normal(0,.3)))): # about 5% plus some Gaussian noise are broken
                slab.broken = True
            min_cost, _ = repairs_m1(slabs)
            level.append(min_cost)
        data.append(np.mean(level))
    plt.plot(num_slab_ran, data)
    plt.xlabel('number of slabs')
    plt.ylabel('mean cost ($)')
    #plt.xscale('log')
    #plt.yscale('log')

def plot1():
    num_slab_ran = range(30,100,3)
    matplotlib.rcParams.update({'font.size': 16})
    plt.figure(figsize=(9,6))
    h_range = (10,20,30,40, 50)
    for h in h_range:
        p1_plot(num_slab_ran = num_slab_ran, height_ran=(0,h))
    #plt.plot(num_slab_ran, [n*REPLACE_RATE*DEFAULT_W*DEFAULT_L for n in num_slab_ran], 'k--')
    plt.legend(list(h_range) + ['all replaced'])
    #plt.savefig('figures/11-17-1.png', dpi=500)
    plt.show()

def p2_plot(num_slab_ran=range(30,100,3), height_ran=(0,10), var=2):
    ''' Markov chain determines heights
    '''
    data = []
    iters = 50
    for n in num_slab_ran:
        level = []
        for i in range(iters):
            slabs = []
            slab = Slab(height=np.random.randint(*height_ran))
            slabs.append(slab)
            
            for k in range(1,n):
                h = int(np.round(np.random.normal(slabs[-1].height, var)))
                h = min(max(h, 0), height_ran[1]) # keep within range
                slab = Slab(height=h)
                slabs.append(slab)

            for slab in random.sample(slabs, int(np.round(BROKEN_RATE*len(slabs)+
                        np.random.normal(0,.3)))): # BROKEN_RATE plus some Gaussian noise are broken
                slab.broken = True

            min_cost, _ = repairs_m1(slabs)
            level.append(min_cost)
        data.append(np.mean(level))
    plt.plot(num_slab_ran, data)
    plt.xlabel('number of slabs')
    plt.ylabel('mean cost ($)')
    #plt.xscale('log')
    #plt.yscale('log')


def plot2():
    num_slab_ran = range(30,100,4)
    matplotlib.rcParams.update({'font.size': 16})
    plt.figure(figsize=(9,6))
    var_range = (2,3,4,5)
    for var in var_range:
        p2_plot(num_slab_ran = num_slab_ran, height_ran=(0,30), var=var)
    plt.legend(list(var_range), loc='upper left')
    #plt.savefig('figures/11-17-3.png', dpi=500)
    plt.show()

def p3_plot(height_ran=(0,10), var=3, 
        run_change_ran=range(0,5), n=70, road_runs=[0]*70 ):
    ''' Markov chain determines heights
        Flat road
    '''
    data = []
    iters = 30
    for max_r in run_change_ran:
        run_ran = (-max_r, max_r)
        level = []
        for i in range(iters):
            slabs = []
            slab = Slab(height=np.random.randint(*height_ran))
            slabs.append(slab)
            
            for k in range(1,n):
                h = int(np.round(np.random.normal(slabs[-1].height+slabs[-1].run*slabs[-1].L*CONV_RUN, var)))
                h = min(max(h, 0), height_ran[1]) # keep within range
                slab = Slab(height=h)
                slabs.append(slab)

            for slab in random.sample(slabs, int(np.round(BROKEN_RATE*len(slabs)+
                        np.random.normal(0,.3)))): # BROKEN_RATE plus some Gaussian noise are broken
                slab.broken = True

            # runs
            for k in range(n):
                r = np.random.randint(*run_ran) if run_ran != (0,0) else 0
                slabs[k].run = r+road_runs[k]

            min_cost, _ = repairs_m2(slabs, road_runs)
            level.append(min_cost)
        data.append(np.mean(level))
    plt.plot(run_change_ran, data)
    plt.xlabel('run range')
    plt.ylabel('mean cost ($)')
    #plt.xscale('log')
    #plt.yscale('log')


def plot3():
    matplotlib.rcParams.update({'font.size': 16})
    plt.figure(figsize=(9,6))
    var = 3 # fix variance 3 for heights
    run_change_ran = range(2,13,2)
    n = 78
    p3_plot(height_ran=(0,30), var=var, 
            run_change_ran=run_change_ran, n=n, road_runs = [0]*n)
    scale_height = n//7
    # hill
    hill_road_runs = [0]*n
    for k in range(n//2+1):
        hill_road_runs[k] = k//scale_height
    for k in range(n//2+1,n):
        hill_road_runs[k] = (n-k)//scale_height
    print(hill_road_runs)
    p3_plot(height_ran=(0,30), var=3, 
            run_change_ran=run_change_ran, n=n, road_runs = hill_road_runs)
    # incline 
    incline_road_runs = [0]*n
    for k in range(n):
        incline_road_runs[k] = k//scale_height
    print(incline_road_runs)
    p3_plot(height_ran=(0,30), var=3, 
            run_change_ran=run_change_ran, n=n, road_runs = incline_road_runs)

    plt.legend(['flat', 'hill', 'incline'])
    #plt.savefig('figures/11-17-7.png', dpi=500)
    plt.show()

def p4_plot(height_ran=(0,10), var=3, 
        run_change_ran=range(0,5), n=70, road_runs=[0]*70,
        run_vars = range(1,5), run_ran=(-8,8)):
    ''' Markov chain determines heights
        Flat road
    '''
    data = []
    iters = 20
    for run_var in run_vars:
        level = []
        for i in range(iters):
            slabs = []
            slab = Slab(height=np.random.randint(*height_ran))
            slabs.append(slab)
            
            for k in range(1,n):
                h = int(np.round(np.random.normal(slabs[-1].height+slabs[-1].run*slabs[-1].L*CONV_RUN, var)))
                h = min(max(h, 0), height_ran[1]) # keep within range
                slab = Slab(height=h)
                slabs.append(slab)

            for slab in random.sample(slabs, int(np.round(BROKEN_RATE*len(slabs)+
                        np.random.normal(0,.3)))): # BROKEN_RATE plus some Gaussian noise are broken
                slab.broken = True

            # runs
            for k in range(n):
                r = int(np.round(np.random.normal(road_runs[k], run_var)))
                r = min(max(r, run_ran[0]), run_ran[1]) # keep within range

                slabs[k].run = r+road_runs[k]

            min_cost, _ = repairs_m2(slabs, road_runs)
            level.append(min_cost)
        data.append(np.mean(level))
    plt.plot(run_vars, data)
    plt.xlabel('run variance')
    plt.ylabel('mean cost ($)')
    #plt.xscale('log')
    #plt.yscale('log')


def plot4():
    matplotlib.rcParams.update({'font.size': 16})
    plt.figure(figsize=(9,6))
    var = 3 # fix variance 3 for heights
    run_change_ran = range(0,5)
    n = 78
    run_vars = (.25, .5, 1, 1.5, 2)
    p4_plot(height_ran=(0,30), var=var, 
            run_vars=run_vars, n=n, road_runs = [0]*n)
    scale_height = n//7
    # hill
    hill_road_runs = [0]*n
    for k in range(n//2+1):
        hill_road_runs[k] = k//scale_height
    for k in range(n//2+1,n):
        hill_road_runs[k] = (n-k)//scale_height
    print(hill_road_runs)
    p4_plot(height_ran=(0,30), var=3,  run_vars=run_vars,
            run_change_ran=run_change_ran, n=n, road_runs = hill_road_runs)
    # incline 
    incline_road_runs = [0]*n
    for k in range(n):
        incline_road_runs[k] = int(k//scale_height * .7)
    print(incline_road_runs)
    p4_plot(height_ran=(0,30), var=3, run_vars=run_vars,
            run_change_ran=run_change_ran, n=n, road_runs = incline_road_runs)

    plt.legend(['flat', 'hill', 'incline'])
    plt.savefig('figures/11-17-8.png', dpi=500)
    plt.show()

def model3_compute():
    data = []

    num_slabs = n = 78
    road_runs = [0]*n
    hill_road_runs = [0]*n
    scale_height = n//7
    for k in range(n//2+1):
        hill_road_runs[k] = k//scale_height
    for k in range(n//2+1,n):
        hill_road_runs[k] = (n-k)//scale_height

    incline_road_runs = [0]*n
    for k in range(n):
        incline_road_runs[k] = int(k//scale_height *.7)

    road_runs = hill_road_runs

    num_sims = 10
    for _ in range(num_sims):
        height_ran = (0,30)
        var = 3
        run_var = .5
        slabs = []
        slab = Slab(height=np.random.randint(*height_ran))
        slabs.append(slab)
                
        for k in range(1,n):
            h = int(np.round(np.random.normal(slabs[-1].height+slabs[-1].run*slabs[-1].L*CONV_RUN, var)))
            h = min(max(h, 0), height_ran[1]) # keep within range
            slab = Slab(height=h)
            slabs.append(slab)

        for slab in random.sample(slabs, int(np.round(BROKEN_RATE*len(slabs)+
                    np.random.normal(0,.3)))): # BROKEN_RATE plus some Gaussian noise are broken
            slab.broken = True

        run_ran = (-4,4)
        # runs
        for k in range(n):
            r = int(np.round(np.random.normal(road_runs[k], run_var)))
            r = min(max(r, run_ran[0]), run_ran[1]) # keep within range

            slabs[k].run = r+road_runs[k]
            c = np.random.randint(-2,2)
            slabs[k].cross = c

        min_cost, M = repairs_m3(slabs, road_runs)
        data.append(min_cost)
    print("Cost:", np.mean(data), "| All replace cost:", num_slabs*REPLACE_RATE*DEFAULT_W*DEFAULT_L)



if __name__ == '__main__':
    #plot1()
    #plot2()
    #plot3()
    #plot4()
    model3_compute()
    #main()

