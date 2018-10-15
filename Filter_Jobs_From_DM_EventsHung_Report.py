import re
import os

reg = re.compile("DMJOB_(\w{2}\d{7})")
currDir = os.path.dirname(os.path.realpath(__file__))

results = []
inputFile = currDir+r"\error_msg.txt"
with open(inputFile, "r") as fileIn:
    for line in fileIn:
        res = reg.search(line)
        if res != None:
            print(res.group(1))
        
input()
