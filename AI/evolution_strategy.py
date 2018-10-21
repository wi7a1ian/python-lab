'''
Created on 2010-10-31

@author: Joo
'''

#! /usr/bin/env python
import math
import re
from random import random
from copy import deepcopy, copy
import time

#positive infinity and not-a-number constants
PosInf = 1e300000
#NaN = PosInf/PosInf

#BINARY FLOATING POINT :(
dec = float
cos = math.cos
sin = math.sin
pow = math.pow
sqrt = math.sqrt
log = lambda x: dec(math.log(x, math.e))
exp = math.exp
PI = math.pi
rand = random

#-------------------------------------------------------------
# Target Function Taken Into Consideration
#-------------------------------------------------------------
def fun(a, b, c, x):
    return a*(pow(x,2) - b*cos(c*PI*x))

class evolution_strategies():
    #-------------------------------------------------------------
    # Initialization of variables 
    #-------------------------------------------------------------
    def __init__(self, targFunction, argumentsNr, iter = 50, recoPlus = True, popSize = 100, offspringSize = 4):
        self.fun = targFunction;
        self.argNr = argumentsNr;
        self.iterNr = iter;
        self.P_SIZE = popSize;
        self.C_SIZE = offspringSize; # number of offspring
        self.D_SIZE = 0;
        self.data = [];
        self.ch = recoPlus; #recombination: 1 -(miu, lambda), 2 -(miu + lambda)
        self.pop = [[dec(0.0)]*(2*argumentsNr) for i in range(self.P_SIZE)]; #actual population
        self.pop_p = [[dec(0.0)]*(2*argumentsNr) for i in range(self.P_SIZE)]; #reproduced population
        self.pop_m = [[dec(0.0)]*(2*argumentsNr) for i in range(self.P_SIZE*self.C_SIZE)]; #mutated offspring population
        self.time = 0

        #calculate tau for mutation
        self.tau1 = [dec(0)]*argumentsNr #variance for r1
        self.tau2 = [dec(0)]*argumentsNr #variance for r2
        for i in range(self.argNr):
            self.tau1[i] = dec(1)/sqrt(dec(2)*self.P_SIZE)
            self.tau2[i] = dec(1)/(sqrt(dec(2)*sqrt(self.P_SIZE)))
        self.initialize();

    #-------------------------------------------------------------
    # Reads self.data from file
    #-------------------------------------------------------------
    def read_file(self, path="AIdata12.dat"):
        fil = open(path, "r");
        regexp = re.compile(r"([\d\.,e\-+]+)")
        for line in fil.readlines():
            res = re.findall(regexp, line)
            self.data.append([dec(str(res[i]).replace(",",".")) for i in range(len(res))])
        fil.close()
        self.D_SIZE = len(self.data)
        return len(self.data)

    #-------------------------------------------------------------
    # Calculate 0 Norm
    #-------------------------------------------------------------
    def normal(self, st_dev):
        size = len(st_dev)
        v = [dec(0.0)]*size
        abc = [dec(0)]*size
        while True:
            v = [2*rand()-1 for i in range(size)]
            s = dec(0)
            for i in range(size):
                s += pow(v[i], 2)
            if s < 1:
                break
        sq = sqrt((-2/s)*log(s))
        for i in range(size):
            abc[i] = st_dev[i]*v[i]*sq
        return abc

    #-------------------------------------------------------------
    # Fitness function, measures fitness of individual
    #-------------------------------------------------------------
    def dist(self, *args):
        y_f = dec(0)
        dis = dec(0)
        for i in range(self.D_SIZE):
            y_f = self.fun(*(args + (self.data[i][0], )))
            dis += pow((y_f-self.data[i][1]), 2)
        return sqrt(dis)
    #-------------------------------------------------------------
    # Initialize, set random values for each individual
    #-------------------------------------------------------------
    def initialize(self):
        for i in range(self.P_SIZE):
            for j in range(2*self.argNr):
                self.pop[i][j] = rand()

    #-------------------------------------------------------------
    # Evaluate (gather fitness information for each individual)
    # After this we know which one is best
    # P_O    True    calculate for parents population (pop)
    #        False    calculate for mutated population (pop_m)
    #-------------------------------------------------------------
    def evaluate(self, P_O):
        if P_O:
            dst_tab = [dec(0)]*self.P_SIZE
            for i in range(self.P_SIZE):
                dst_tab[i] = self.dist(*tuple(self.pop[i][0:self.argNr]))
        else:
            dst_tab = [dec(0)]*(self.C_SIZE*self.P_SIZE)
            for i in range(self.P_SIZE*self.C_SIZE):
                dst_tab[i] = self.dist(*tuple(self.pop_m[i][0:self.argNr]))

        return dst_tab

    #-------------------------------------------------------------
    # Reproduce population
    #-------------------------------------------------------------
    def reproduce(self):
        self.pop_p = deepcopy(self.pop)

    #-------------------------------------------------------------
    # Mutate population
    ## object variable and strategy parameter
    #-------------------------------------------------------------
    def mutate(self):
        xLen = self.argNr #object variable length (how many variables are in our system)
        r = [[dec(0)]*xLen for i in range(self.C_SIZE*self.P_SIZE)]
        s_d = [[dec(0)]*xLen for i in range(self.C_SIZE*self.P_SIZE)] #covariance matrix
        st_dev = [dec(0)]*xLen #vector of standard deviations
        rx = [dec(0)]*xLen #normally distributed random vector with mean eq. to zero
        t1 = [dec(0)]*xLen #normalized tau1
        t2 = [dec(0)]*xLen #normalized tau2

        #calculate coefficients needed to mutate our new individuals
        for i in range(self.P_SIZE):
            st_dev = self.pop_p[i][-xLen:]
            for j in range(self.C_SIZE):
                rx = self.normal(st_dev)
                t1 = self.normal(self.tau1)
                t2 = self.normal(self.tau2)
                for k in range(xLen):
                    r[self.C_SIZE*i+j][k] = rx[k]
                    s_d[self.C_SIZE*i+j][k] = exp(t1[k])*exp(t2[k])

        #mutate all offspring (made from parent)
        for i in range(self.P_SIZE):
            for j in range(self.C_SIZE):
                for k in range(xLen):
                    self.pop_m[self.C_SIZE*i+j][k] = self.pop_p[i][k] + r[self.C_SIZE*i+j][k]
                    self.pop_m[self.C_SIZE*i+j][k+xLen] = self.pop_p[i][k+xLen]*s_d[self.C_SIZE*i+j][k]

    #-------------------------------------------------------------
    # Select
    #-------------------------------------------------------------
    def select(self, parent_tab, offspring_tab):
        size = 0
        idx = [0]*self.P_SIZE
        common = [dec(0)]*(self.C_SIZE*self.P_SIZE)#table with all individuals taken into consideration
        for i in range(self.C_SIZE*self.P_SIZE):
            common[i] = offspring_tab[i]

        #section made of offspring
        if not self.ch:
            size = self.C_SIZE*self.P_SIZE
        #selection made of both offspring and parents
        else:
            size = (self.C_SIZE+1)*self.P_SIZE
            for i in range(self.C_SIZE*self.P_SIZE, (self.C_SIZE+1)*self.P_SIZE):
                common.append(parent_tab[i-self.C_SIZE*self.P_SIZE])

        for i in range(self.P_SIZE):
            idx[i] = common.index(min(common))
            common[idx[i]] = PosInf; #mark as already selected
            for k in range(2*self.argNr):
                if idx[i] >= (self.C_SIZE*self.P_SIZE):
                    self.pop[i][k] = self.pop_p[idx[i]-self.C_SIZE*self.P_SIZE][k] #take from set of parents
                else:
                    self.pop[i][k] = self.pop_m[idx[i]][k] #take from set of offspring

    # MAIN -------------------------------------------------------
    def execute(self, accuracy = None):
        if len(self.data) == 0: return
        self.time = time.time()
        cnt = 0
        tab = [dec(0.0)]*self.P_SIZE
        tab1 = [dec(0.0)]*(self.C_SIZE*self.P_SIZE)
        if accuracy == None:
            while cnt < self.iterNr:
                tab = self.evaluate(True);
                self.reproduce(); #make a copy of parents
                #genetic operations:
                #- mutation
                self.mutate(); #create mutated offspring
                tab1 = self.evaluate(False);
                #- recombination
                self.select(tab, tab1);
                cnt += 1
        else:
            accuracy = dec(accuracy)
            while self.dist(*tuple(self.pop[0][0:self.argNr])) > accuracy:
                tab = self.evaluate(True);
                self.reproduce();
                self.mutate();
                tab1 = self.evaluate(False);
                self.select(tab, tab1);
                cnt += 1
                #print self.dist(*tuple(self.pop[0][0:self.argNr]))
        self.time = (time.time()-self.time) # in seconds
        return cnt

    # Calculated final values
    def results(self):
        if len(self.data) == 0: return
        return tuple(self.pop[0][0:self.argNr]) #self.pop[0] because while selecting, we set optimum as first

    def error(self):
        if len(self.data) == 0: return
        return self.dist(*tuple(self.pop[0][0:self.argNr]))


#USAGE EXAMPLE
evoStrat = evolution_strategies(fun, 3, 100, True, 100, 2);
evoStrat.read_file()
interationsNr = evoStrat.execute()
a, b, c = evoStrat.results()
dist = evoStrat.error()
print("Optimal values of a =" , a , ", b =" , b , " and c =" , c)
print("Distance = " , dist)
print("Number of iterations:", interationsNr)
print("Calculation time:",evoStrat.time,"s");
