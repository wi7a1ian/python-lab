import fileinput

inputFile = "qweqefwefwe.csv"
outputFile = "SR686651_VE561_DocWithoutOrganizerText_All_CDG.csv"

fileIn = open(inputFile, "r")
fileOut = open(outputFile, "w")
lololo = "asasas,asasa,asasas,asassa,qefrwefwfrwgr,wefwefwfefwe,wefwef"

counter = 0

for line in fileIn:
    lineArr = line.split(",")
    line = "\"{0[0]:s}\",\"{0[1]:s}\",\"{0[2]:s}\",\"{0[3]:s}\",\"{1:s}\"".format(lineArr, ",".join(lineArr[4:]))
    fileOut.write(line)
    counter += 1

fileIn.close()
fileOut.close()

print("{0!s} rows affected [From total: 1038141]".format(counter))
