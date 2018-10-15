import os
fileIn = "Slice_List_In.txt"
fileOut = "Slice_List_Out.txt"

uniqSlices = set([i.strip() for i in open(fileIn) if len(i.strip()) > 0])
open(fileOut, "w").write("\n".join(sorted(list(uniqSlices))))#os.linesep
    
input("{0} unique slices".format(len(uniqSlices)))
