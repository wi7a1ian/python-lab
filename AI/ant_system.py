#python version 2.5.2

import math
import re
from random import random
from copy import deepcopy, copy
import time

#positive infinity and not-a-number constants
PosInf = 1e300000
dec = float
cos = math.cos
sin = math.sin
pow = math.pow
sqrt = math.sqrt
log = lambda x: dec(math.log(x, math.e))
exp = math.exp
PI = math.pi
rand = random

#---------------------------------------------------------------------------
#Class representing walking Ant
#---------------------------------------------------------------------------
class AntWalker:
    def __init__(self, canWalkBack = False, allowedLoops = 5, a = 1, b = 5, p = 0.5):
        """ a - influence of pheromone, b - influence of path cost, p - pheromone evaporation"""
        self.position = 0 #Actual ant position
        self.memory = [0] #List with visited cities
        #Controll parameters
        self.pParam = p #pheromon evaporation
        self.aParam = a #influence of pheromon
        self.bParam = b #influence of path cost
        self.isDead = False
        if canWalkBack: #set 'choosePath' func as one with possibility to move back
            self.choosePath = self.choosePathBack
            self.allowedLoops = allowedLoops
        else: #set 'choosePath' func as one moving constantly along the enumeration (forward)
            self.choosePath = self.choosePathForward
            self.allowedLoops = 0

    def memorize(self, step): #put on stock newly choosen step
        self.memory.append(step)
    def choosePath(self, paths): #abstract function (overloaded)
        pass

    def choosePathBack(self, paths):
        return self.decisionAlg(paths)

    def choosePathForward(self, paths):
        paths = [route for route in paths if route.id > self.position]# return list of items that meet condition
        return self.decisionAlg(paths)

    def decisionAlg(self, paths):
        #Decision calculation
        denomSum = 0
        for route in paths:
            desire = pow(route.pheroConc, self.aParam)*pow(1/route.cost, self.bParam)
            denomSum += desire
            route.decDesire = desire
        for route in paths:
            #print route.decDesire, denomSum
            if denomSum == 0:
                route.decDesire = 0
            else:
                route.decDesire = route.decDesire/denomSum

        #check if ant was already in one of these spots (if walking back is On, we allow more visits)
        paths = [route for route in paths if self.memory.count(route.id) <= self.allowedLoops]
        if len(paths) < 1: #probably a dead end
            return self.kill() #die u lazy ant!

        #Probability calculation
        choice = random() #wandom number from [0;1)
        probabSum = 0
        denomSum = 0
        for route in paths:
            denomSum += route.decDesire
        for route in paths:
            if denomSum == 0:
                route.decProbability = 0
            else:
                route.decProbability = route.decDesire/denomSum

            #print route.id+1, route.decProbability
            probabSum += route.decProbability
            if choice <= probabSum: #Estimate if this route is chosen one
                chosenRoute = route.id
                break
        else:#if something goes wrong, select last path
            chosenRoute = paths[len(paths)-1].id
        self.position = chosenRoute #new position
        self.memorize(chosenRoute) #update memory
        return None


    def kill(self): #Sometimes ants need to be killed because she lost or meet dead end
        #I was thinking about returning negative pheromone concentration along the path
        #so the next ant won't choose the same path so easily
        self.isDead = True
        return False

#---------------------------------------------------------------------------
#Class representating one route along path (one connection)
#---------------------------------------------------------------------------
class AntRoute:
    def __init__(self, id, cost = 0, pheromone = 0):
        self.id = id
        self.cost = cost
        self.pheroConc = pheromone #pheromone concentration along this path
        #used by decision algorithm
        self.decDesire = 0 #decision desire
        self.decProbability = 0 #decision probability

#---------------------------------------------------------------------------
#Class using Ant System algorithm to find cheapest path between two cities
#---------------------------------------------------------------------------
class AntSystem():
    def __init__(self, colonySize = 1000, randomInitPhero = False, canWalkBack = False, allowedLoops = 5, a = 1, b = 5, p = 0.5):
        """ colonySize - size of the ants colony
        randomInitPhero - random initial pheromone distribution
        canWalkBack - allow ants to walk to the one city several times
        allowedLoops -  how many times ant can visit the same city
        a - influence of pheromone, b - influence of path cost, p - pheromone evaporation"""
        self.costMap = [] #square matrix with costs
        self.paths = [] #pheromone concentration
        self.randomInitPhero = randomInitPhero
        self.colonySize = colonySize#colonySize #number of traversing ants
        self.canWalkBack = canWalkBack
        self.allowedLoops = 5
        self.deadAnts = 0
        self.tourSchemes = []
        self.tourCosts = []
        self.tourCostsList = []
        self.finalCost = None
        self.finalCostsList = None
        self.finalPath = None
        self.time = 0 #total execution time calculated at the end
        self.pParam = p #pheromon evaporation
        self.aParam = a #influence of pheromon
        self.bParam = b #influence of path cost

    def readFile(self, path): #read costs map from file
        fil = open(path, "r");
        self.readMap(fil.read())
        fil.close()

    def readMap(self, mapStr): #validate and decrypt costs map from sting
        newData = []
        tab = mapStr.split("\n")
        if tab[len(tab)-1] == "":
            tab.pop(len(tab)-1)
        l = len(tab)
        regexp = re.compile(r"([\d\.,e\-+]+)")
        for line in tab:
            res = re.findall(regexp, line)
            if(l != len(res)):
                return False
            for i in range(len(res)):
                if res[i] == ".":
                    res[i] = PosInf
            newData.append([dec(i) for i in res])
        self.costMap = newData
        return True

    def initialize(self): #set initial pheromone concentartion (random or equal)
        self.deadAnts = 0
        self.tourSchemes = []
        self.tourCosts = []
        self.tourCostsList = []
        self.pathsHistory = []
        self.finalCost = None
        self.finalPath = None
        self.finalCostsList = None
        mapSize = len(self.costMap) #Nuumber of cities
        self.paths = []
        #Creating tree with paths connecting each city, including their costs & pheromone concentration
        for i in range(mapSize):
            cityPaths = []
            for j in range(mapSize):
                if self.costMap[i][j] != PosInf: #If connection was found
                    initialPhero = 0
                    if self.randomInitPhero: #Random initial pheromone concentration
                        initialPhero = 0.05+random()*0.25 # range: <0.05 ; 0.3>
                    else: #Equal initial pheromone concentration
                        initialPhero = 1.0/mapSize
                    cityPaths.append(AntRoute(j, self.costMap[i][j], initialPhero))
            self.paths.append(cityPaths)

    def departAnt(self):#Set off one ant, and return whole path and its cost
        ant = AntWalker(self.canWalkBack, self.allowedLoops, self.aParam, self.bParam, self.pParam)
        food = len(self.paths)-1
        while (not ant.isDead) and (ant.position != food):
            #choose route to another spot
            ant.choosePath(self.paths[ant.position])
        #print ant.memory, ant.isDead
        if ant.isDead:
            self.deadAnts += 1
            return None
        else:
            return ant.memory

    def updatePath(self, antMemo):
        if antMemo == None: #if ant died, we do nothing
            return None, None
        for branch in self.paths: #pheromone evaporation
            for route in branch:
                route.pheroConc = (1-self.pParam)*route.pheroConc
        #Whole path cost
        costsSum = 0
        costsList = []
        for i in range(len(antMemo)-1): #calculate total cost
            for route in self.paths[antMemo[i]]:
                if route.id == antMemo[i+1]:
                    costsSum += route.cost
                    costsList.append(route.cost)
        #Update pheromone on the path
        for i in range(len(antMemo)-1):
            for route in self.paths[antMemo[i]]:
                if route.id == antMemo[i+1]:
                    route.pheroConc += 1/costsSum
        return costsSum, costsList

    def execute(self): #start algorithm
        self.time = time.time()
        self.initialize()
        if len(self.paths[0]) < 1: #no connections
            return False
        antNr = 0
        #self.pathsHistory.append(deepcopy(self.paths))
        while antNr < self.colonySize:
            tour = self.departAnt()
            if tour != None:
                (tourCost, tourCostsList) = self.updatePath(tour)
                self.tourSchemes.append(tour)
                self.tourCosts.append(tourCost)
                self.tourCostsList.append(tourCostsList)
                #self.pathsHistory.append(deepcopy(self.paths))
            antNr += 1

        self.time = (time.time()-self.time) # in seconds
        optimumIndex = self.tourCosts.index(min(self.tourCosts)) #optimum path cost
        self.finalCost = self.tourCosts[optimumIndex]
        self.finalPath = self.tourSchemes[optimumIndex]
        self.finalCostsList = self.tourCostsList[optimumIndex]
        return [a+1 for a in self.finalPath], self.finalCost #optimum path and cost

#EXAMPLE
#AS = AntSystem(1000, False, False, 5, 2, 1, 0.5)
#AS.readFile("../mapa.asm")
#print AS.execute()
#print AS.time
#print AS.deadAnts

#a = 1, b = 5, p = 0.5
##aTab = [0.1, 0.5, 1, 2, 5, 10]
##bTab = [0.1, 0.5, 1, 2, 5, 10]
##pTab = [0, 0.1, 0.2, 0.5, 0.7, 0.9]

##Alpha investigation
#outStr = ""
#b = 1
#p = 0.5
#for a in aTab:
#    maxError = 0
#    sumError = 0
#    timeSum = 0
#    deadSum = 0
#    for i in range(100):
#        AS = AntSystem(1000, False, False, 5, a, b, p)
#        AS.readFile("../mapa.asm")
#        AS.execute()
#        sumError += AS.finalCost-26
#        timeSum += AS.time
#        deadSum += AS.deadAnts
#        if maxError < AS.finalCost-26:
#            maxError = AS.finalCost-26
#
#    outStr += " ".join([str(a), str(b), str(p), str(timeSum), str(deadSum), str(maxError), str(sumError)])+"\n"
#
#fil = open("resultA", "w");
#fil.write(outStr)
#fil.close()
#
##Beta investigation
#outStr = ""
#a = 1
#p = 0.5
#for b in bTab:
#    maxError = 0
#    sumError = 0
#    timeSum = 0
#    deadSum = 0
#    for i in range(100):
#        AS = AntSystem(1000, False, False, 5, a, b, p)
#        AS.readFile("../mapa.asm")
#        AS.execute()
#        sumError += AS.finalCost-26
#        timeSum += AS.time
#        deadSum += AS.deadAnts
#        if maxError < AS.finalCost-26:
#            maxError = AS.finalCost-26
#
#    outStr += " ".join([str(a), str(b), str(p), str(timeSum), str(deadSum), str(maxError), str(sumError)])+"\n"
#
#fil = open("resultB", "w");
#fil.write(outStr)
#fil.close()
#
##P investigation
#outStr = ""
#a = 1
#b = 1
#for p in pTab:
#    maxError = 0
#    sumError = 0
#    timeSum = 0
#    deadSum = 0
#    for i in range(100):
#        AS = AntSystem(1000, False, False, 5, a, b, p)
#        AS.readFile("../mapa.asm")
#        AS.execute()
#        sumError += AS.finalCost-26
#        timeSum += AS.time
#        deadSum += AS.deadAnts
#        if maxError < AS.finalCost-26:
#            maxError = AS.finalCost-26
#
#    outStr += " ".join([str(a), str(b), str(p), str(timeSum), str(deadSum), str(maxError), str(sumError)])+"\n"
#
#fil = open("resultP", "w");
#fil.write(outStr)
#fil.close()

#Standard
#outStr = ""
#maxError = 0
#sumError = 0
#timeSum = 0
#deadSum = 0
#a = 1
#b = 1
#p = 0.5
#d = 0
#
#BASE_HREF = ""#r"d:\\Projects\\pyAnt_system\\src\\"
#
#for i in range(100):
#    AS = AntSystem(1000, False, False, 5, a, b, p)
#    AS.readFile(BASE_HREF+"mapa.asm")
#    AS.execute()
#    sumError += AS.finalCost-26
#    timeSum += AS.time
#    deadSum += AS.deadAnts
#    if maxError < AS.finalCost-26:
#        maxError = AS.finalCost-26
#outStr += " ".join([str(d), str(timeSum), str(deadSum), str(maxError), str(sumError)])+"\n"
#for i in range(100):
#    AS = AntSystem(1000, True, False, 5, a, b, p)
#    AS.readFile(BASE_HREF+"mapa.asm")
#    AS.execute()
#    sumError += AS.finalCost-26
#    timeSum += AS.time
#    deadSum += AS.deadAnts
#    if maxError < AS.finalCost-26:
#        maxError = AS.finalCost-26
#outStr += " ".join([str(d), str(timeSum), str(deadSum), str(maxError), str(sumError)])+"\n"
#
#dTab = [0, 1, 2, 5, 10]
#for d in dTab:
#    for i in range(100):
#        AS = AntSystem(1000, False, True, d, a, b, p)
#        AS.readFile(BASE_HREF+"mapa.asm")
#        AS.execute()
#        sumError += AS.finalCost-26
#        timeSum += AS.time
#        deadSum += AS.deadAnts
#        if maxError < AS.finalCost-26:
#            maxError = AS.finalCost-26
#    outStr += " ".join([str(d), str(timeSum), str(deadSum), str(maxError), str(sumError)])+"\n"
#
#
#fil = open(BASE_HREF+"resultNRD.txt", "w");
#fil.write(outStr)
#fil.close()

##AS = AntSystem(20, False, False, 5, 0.5, 1, 0.1)
##AS.readFile(BASE_HREF+"mapa.asm")
##AS.execute()
##outStr = ""
##for path in AS.pathsHistory:
##    routesIds = []
##    routes = []
##    for i in range(len(path)):
##        for route in path[i]:
##            if route.id > i:
##                routes.append(str(route.pheroConc).replace(".", ","))
##                routesIds.append(str(i)+"-"+str(route.id))
##    if AS.pathsHistory.index(path) == 0:
##        outStr += " ".join(routesIds)+"\n"
##    outStr += " ".join(routes)+"\n"
##fil = open(BASE_HREF+"resultPhero.txt", "w");
##fil.write(outStr)
##fil.close()
##print(outStr);
