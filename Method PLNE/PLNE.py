from Multiple_knapsack import Multiple_knapsack
import numpy as np
import datetime as dt
import math
import minilp.result
from minilp import *
import time

class PLNE():
    def __init__(self):
        self.flat = 0                # sizes of knapsacks 
        self.nb_knapsack = 0         # amount of knapsack
        self.servers = 0             # list of servers
        self.nb_servers = 0          # amount of servers
        self.existence_servers = []  # existence of a server j in knapsack i
        self.sizes_server = []       # size of servers
        self.capacities_server = []  # calculating capacity of servers
        self.result = []             # final result of existence_servers
        self.time_consumption = None # time comsumption of PLNE method
        self.score = 0               # calculating capacity of all servers palced

    def read_file(self, path):
        #read file and import variable values, more details are in Multiple_knapsack.py
        pb = Multiple_knapsack(path)         
        self.servers = pb.servers
        self.flat = pb.flat()
        self.nb_knapsack = len(pb.flat())
        self.nb_servers = len(self.servers)
        for server in self.servers:
            self.sizes_server.append(server[0])
            self.capacities_server.append(server[1])
            
    def solve(self):
        #solve the problem
        start_time = time.time()
        lp = problem('PLNE')
        self.existence_servers = np.array(lp.integer_var_list(self.nb_knapsack*self.nb_servers,0,1)) \
                                                        .reshape(self.nb_knapsack,self.nb_servers)
        # a server exists only one time
        for i in range(self.nb_servers):
            lp.add_constraint(sum(self.existence_servers.T[i]) <= 1)
        # each sac has limited size
        for j in range(self.nb_knapsack):
            lp.add_constraint( sum(self.existence_servers[j]*self.sizes_server) <= self.flat[j] )
        # set objective function to be maximized
        lp.set_objective( sum(sum(self.existence_servers*self.capacities_server)), sense=max)
        result=banb(lp)
        
        self.time_consumption = time.time() - start_time
        self.score = result.objective
        # get the existence of servers in each knapsack
        for j in range(self.nb_knapsack):
            self.result.append(result.get_values(self.existence_servers[j]))
        print("OK, problem is solved within %.2f seconds" %(self.time_consumption))



def get_first_non_integral(p, s):
    """ Given a problem p and a result s, returns the first integer variables
    that has a fractional value in s, or None if no such variable was found. """
    for v in p.variables:
        if v.category == int:
            if abs(round(s.get_value(v)) - s.get_value(v)) > 1e-6:
                return v
    return None

def banb(p, lp_solver=None):
    if lp_solver is None:
        lp_solver = solvers.get_default_solver()
    def cmp(l, r):
        if np.isnan(r.objective):
            return True
        if p.sense == min:
            return l.objective < r.objective
        return l.objective > r.objective

    res = minilp.result.result()
    #res = p.lp_solve(lp_solver)
    nodes = [[]] # nodes = list of constraints
    cnt = 0
    
    print('B&B using {} to solve linear relaxation'.format(lp_solver.__class__.__name__))
    while nodes:
        if cnt % 10 == 0:
            print('{} {:5d} {:5d} {:9g}'.format(dt.datetime.now().strftime('%T'), cnt, 
                                                len(nodes), res.objective))
        cnt += 1
        cns = nodes.pop()
        cs = p.add_constraints(cns)
        s = p.lp_solve(lp_solver)
        p.del_constraints(cs)
        if s:
            fni = get_first_non_integral(p, s)
            if fni is None: # integral solution
                if cmp(s, res):
                    res = s
                    print('{} {:5d} {:5d} {:9g}*'.format(dt.datetime.now().strftime('%T'), cnt, 
                                                         len(nodes), res.objective))
            elif cmp(s, res):
                fl = math.floor(s.get_value(fni))
                nodes.append(cns + [fni <= fl])
                nodes.append(cns + [fni >= fl + 1])
    return res
