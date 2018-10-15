with open("results.txt") as i, open("results_filtered.txt" ,"w") as o:
    for line in i:
        if "ERROR" in line:
            o.write(line)
