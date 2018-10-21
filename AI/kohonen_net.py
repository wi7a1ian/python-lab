#! /usr/bin/env python
import os
import math
import re
from random import random
import time
from copy import deepcopy
from copy import copy

#types:
class PatternVector(list):
    def __init__(self, MaxDim):
        self.extend([0.0]*MaxDim);
class OutputVector(list):
    def __init__(self, MaxClass):
        self.extend([0.0]*MaxClass);
class WeightMatrix(list):
    def __init__(self, MaxClass, MaxDim):
        for i in range(0, MaxClass):
            self.append(PatternVector(MaxDim));
class CovarType(list):
    def __init__(self):
        self.extend([[0.0]*2, [0.0]*2]);


class KohonenNet():
    def __init__(self, MaxCycle = 100,  MaxClass = 10, N = 2.0, Alpha = 0.5, MaxPattern = 300, MaxPatternDim=5):
        # Predefined variables
        self.MaxPatternDim = MaxPatternDim;#max dimension of input
        self.MaxPattern = MaxPattern;#max number of patterns

        self.MaxClass = MaxClass;#max number of classes
        self.MaxCycle = MaxCycle;#max number of training cycles

        self.N = N;#2.0 initial neighborhood
        self.Alpha = Alpha;#0.5 initial learning rate

        self.W = WeightMatrix(self.MaxClass, self.MaxPatternDim);
        self.NClasses = 0;# { current number of classes }
        self.NPatterns = 0;#{ current number of patterns }
        self.InputSize = 0;# { current pattern space dimension }
        self.X = [PatternVector(self.MaxPatternDim) for i in range(self.MaxPattern)]#{ pattern data array }
        self.Winner = 0;# { current winner unit }
        self.Pattern = 0;# { current pattern }
        self.DeltaN = 0.0;
        self.DeltaAlpha = 0.0;
        self.CycleNo = 0;
        self.Membership = [0 for i in range(self.MaxPattern)]#   : array[1..MaxPattern] of byte;
        self.Initialize()
        self.RandomWeights();

    def EuclideanNorm(self, xx,vv):
        sum = 0
        for i in range(self.InputSize):
            sum += (xx[i]-vv[i])*(xx[i]-vv[i])
        return sum

    def Norm(self, vv,xx):
        return self.EuclideanNorm(xx,vv)

    def FindNearest(self, P):
        q = 0
        z = 0.0
        min = 1.0e38
        for i in range(self.MaxClass):
            z = self.Norm(self.X[P], self.W[i]);
            if z < min:
                min = z
                q = i
        return q

    def ChangeWeights(self):
        k = 0
        self.DeltaW = PatternVector(self.MaxPatternDim)
        self.Ni = 0

        self.N -= self.DeltaN#the radius of neighbourhood - real value
        self.Ni = int(round(self.N))#neighbourhood converted to integer value
        self.Alpha -= self.DeltaAlpha#;change of the learning coeff.
        for j in range(self.InputSize):# calculation of DeltaW correction
            self.DeltaW[j] = self.Alpha*(self.X[self.Pattern][j]-self.W[self.Winner][j]) # type here upgrade of weights for Winner neuron

        for i in range(self.Winner-self.Ni, self.Winner+self.Ni):
            k = ((i + self.MaxClass) % self.MaxClass)
            for j in range(self.InputSize):
                self.W[k][j] = self.W[k][j] + self.DeltaW[j];# type here modification of neurons weights

    def LearnSingle(self):
        #self.Pattern = int(math.floor(random()*self.NPatterns))#; {randomly choosen single input pattern} trunc
        self.Pattern = int(random()*(self.NPatterns-1))
        self.Winner = self.FindNearest(self.Pattern)#;   {finding the neuron closest to input}
        self.ChangeWeights()#                  {changing of winner's weights}

    def ReadPatterns(self, path = "DANE.DAT"): #{ reads patterns from disk file }
        fil = open(path, "r");
        regexp = re.compile(r"([\d\.]+)")
        k = 0
        for line in fil.readlines():
            res = re.findall(regexp, line)
            for i in range(len(res)):
                self.X[k][i] = float(res[i])
            self.InputSize = len(res)
            k+=1
        fil.close()
        self.NPatterns = k
        return k

    def updateMembership(self):
        for i in range(self.NPatterns):
            self.Membership[i] = self.FindNearest(i);

    def AddPattern(self, pat):
        self.X[self.NPatterns] = deepcopy(pat)
        self.NPatterns +=1
        self.FindNearest(self.NPatterns-1)
        self.Membership[self.NPatterns-1] = self.FindNearest(self.NPatterns-1);

    def RandomWeights(self): #{ randomize weights in weight matrix }
        for i in range(self.MaxClass):
            for j in range(self.MaxPatternDim):
                self.W[i][j] = random()

    def Initialize(self):
        self.DeltaN = self.N/self.MaxCycle#;    { alpha correction factor }
        self.DeltaAlpha = self.Alpha/self.MaxCycle#;  { neighborhood shrink correction factor }
        self.CycleNo = 0;

    def Step(self):
        if self.InputSize == 0 or self.MaxCycle <= self.CycleNo: return None
        self.LearnSingle();
        self.CycleNo += 1;
        return self.CycleNo

#{---------------------- main ---------------------}

#if __name__ == "__main__":
#    koh = KohonenNet();
#    koh.ReadPatterns();
#    while koh.Step():
#        koh.updateMembership();
#        outStr = ""
#        for i in range(koh.MaxClass):
#            cnt = 0
#            for j in range(koh.NPatterns):
#                if koh.Membership[j] == i:
#                    cnt += 1
#            outStr += "Class "+str(i)+": "+str(cnt)+"\n"
#        print outStr
