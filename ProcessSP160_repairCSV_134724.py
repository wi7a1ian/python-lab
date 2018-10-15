import codecs

inputFile = "134724-001-01.csv"
outputFile = "134724-001-01_repaired.csv"
counter = 0
#with codecs.open(inputFile, "r", "utf-8") as fileIn:
#with codecs.open(inputFile, "r", "unicode") as fileIn:
#with codecs.open(inputFile, "r", "latin1") as fileIn:
with codecs.open(inputFile, "r", "utf-16") as fileIn, codecs.open(outputFile, "w", "utf-16") as fileOut:
#with open(inputFile, "r") as fileIn:
    for line in fileIn:
        lineArr = line.split('","')
        lineArr[0] = lineArr[0][1:]
        lineArr[-1] = lineArr[-1].rstrip('\r\n')[0:-1]
        if any('"' in s for s in lineArr):
            counter += 1
            lineArr = [s.replace('"', '""') for s in lineArr]
            lineArr[0] = '"'+lineArr[0]
            lineArr[-1] = lineArr[-1]+'"\r\n'
            line = '","'.join(lineArr)
        fileOut.write(line) 

print("({0:d}) rows affected.".format(counter))
input()
## To gracefully deal with such items in the list by skipping the non-iterable items, use the following:
## [el for el in lst if isinstance(el, collections.Iterable) and (st in el)]
## then, with such a list:
## lst = [None, 'abc-123', 'def-456', 'ghi-789', 'abc-456', 123]
## st = 'abc'
## you will still get the matching items (['abc-123', 'abc-456'])
