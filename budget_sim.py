import numpy as np

start_year = 2019
num_years = 25
start_CO2 = 0.0061*start_year-11.51

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


def init_slabs(n=1000, mean_age=10):
    if mean_age == 0:
        ages = [0]*n
    else:
        ages = np.random.chisquare(mean_age,size=n)

    slabs = []
    for age in ages:
        ave_ft_cycles = (-0.0842*8.1**2 - .154*8.1 + 13.1)*12
        ft_cycles = ave_ft_cycles*age
        carb_depth = 4.4*np.sqrt(start_CO2*age*365)
        slab = Slab(age=age, ft_cycles=ft_cycles, carb_depth=carb_depth)
        slabs.append(slab)
    return set(slabs)

def does_break(slab):
    ''' return true if this slab breaks now
    '''
    r1, r2, r3 = 0, 0, 0
    if slab.ft_cycles > 500:
        r1 = np.random.rand()
    if slab.carb_depth > 4*25.4: # inch to millimeter
        r2 = np.random.rand()
    if slab.age > 30:
        r3 = np.random.rand()
    return r1 > .98 or r2 > .98 or r3 > .98

def time_step(slab, CO2, ft_cycles=80):
    slab.age += 1
    slab.ft_cycles += ft_cycles

    carb_depth = 4.4 * np.sqrt(CO2*365)
    slab.carb_depth += carb_depth

def simulate(new_blocks_per_year=6):
    num_sims = 10
    start_blocks = 700
    sim_results = []
    means = []
    live_slabs = []
    for s in range(num_sims):
        live_slabs = init_slabs(n=start_blocks*78, mean_age=7)
        broke_per_year = []
        for k in range(num_years):
            broken_slabs = 0
            y = start_year + k
            CO2 = (0.0061*y-11.51)/1000
            ave_temp = 8.1 + k * (6/80)
            ft_cycles = (-0.0842*ave_temp**2 - .154*ave_temp + 13.1)*12
            for slab in live_slabs:
                time_step(slab, CO2, ft_cycles=ft_cycles)
            for slab in list(live_slabs):
                if does_break(slab):
                    live_slabs.remove(slab)
                    new_slab = init_slabs(n=1, mean_age=0)
                    live_slabs.add(new_slab.pop())
                    broken_slabs += 1
            new_slabs = init_slabs(n=new_blocks_per_year*78, mean_age=0)
            live_slabs.update(new_slabs)
            broke_per_year.append(broken_slabs)
        sim_results.append(broke_per_year)

    means = [np.mean([res[k] for res in sim_results]) for k in range(num_years)]
    costs = [m*22*4*6*(1.02)**k for k, m in enumerate(means)]
    return costs 

if __name__ == '__main__':
    m = simulate()
    print(m)
