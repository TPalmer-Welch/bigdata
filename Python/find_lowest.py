import csv
import os
import requests


class conf:

    def __init__(self, numSims, numIts, numChild, lcf, permId, reorgSeed, permSeed, reorgPer, memOff, reorgStrat, convTol):
        self.numSims = numSims
        self.numIts = numIts
        self.numChild = numChild
        self.lcf = lcf
        self.permId =permId
        self.reorgSeed = reorgSeed
        self.permSeed = permSeed
        self.reorgPer = reorgPer
        self.memOff = memOff
        self.reorgStrat = reorgStrat
        self.convTol = convTol

    def to_list(self):
        return [self.numSims, self.numIts, self.numChild, self.lcf, self.permId, self.reorgSeed, self.permSeed, self.reorgPer, self.memOff, self.reorgStrat, self.convTol]


def scraper(file_path, all_mins):
    for dire in os.listdir(file_path):
        fpath = r"{}\{}\global-cost.csv".format(file_path, str(dire))

        try:
            with open(fpath, "r") as f1:
                lines = f1.readlines()
                f1.close()
        except:
            continue

        lines.pop(0)
        top_sims = []
        for line in lines:

            sims = line.split(",")[3:]
            sims = [float(x) for x in sims]
            sims = sorted(sims)
            top_sims.append(sims[0])
            #print(sims[0])

        fpath = r"{}\{}\used_conf.txt".format(file_path, str(dire))

        try:
            with open(fpath, "r") as f1:
                file = f1.readlines()
                f1.close()
        except:
            continue

        numSims = file[4].strip().replace("numSimulations = ", "")
        numIts = file[9].strip().replace("numIterations = ", "")
        numChild = file[10].strip().replace("numChildren = ", "")
        lcf = file[15].strip().replace("local cost function = ", "")
        permId = file[18].strip().replace("permutationID = ", "")
        reorgSeed = file[19].strip().replace("reorganizationSeed = ", "")
        permSeed = file[20].strip().replace("permutationSeed = ", "")
        reorgPer = file[22].strip().replace("reorganizationPeriod = ", "")
        memOff = file[23].strip().replace("memorizationOffset = ", "")
        reorgStrat = file[24].strip().replace("reorganizationStrategy = ", "")
        convTol = file[25].strip().replace("convergenceTolerance = ", "")

        c = conf(numSims, numIts, numChild, lcf, permId, reorgSeed, permSeed, reorgPer, memOff, reorgStrat, convTol)

        top_sims = sorted(top_sims)

        all_mins.append((top_sims[0], r"{} {}".format(file_path, str(dire)), c))

all_mins = []

scraper(r"/home/tpw/big-data/bigdata/Python/instance_1/output", all_mins)
scraper(r"/home/tpw/big-data/bigdata/Python/instance_2/output", all_mins)
scraper(r"/home/tpw/big-data/bigdata/Python/instance_3/output", all_mins)
scraper(r"/home/tpw/big-data/bigdata/Python/instance_4/output", all_mins)
scraper(r"/home/tpw/big-data/bigdata/Python/instance_5/output", all_mins)

all_mins = sorted(all_mins, key=lambda x: x[0])

total_runs = len(all_mins)
best = all_mins[0]
best_val = best[0]
best_path = best[1]
best_conf = best[2]

url = "https://script.google.com/macros/s/AKfycbwz1IPRKHUV4Bibm5ZVa48-_NdocvGCXf8XJi6uik47g1m4y082kN7-FBnlzHQUS8e-/exec"

params = {
    "numRuns": total_runs,
    "variance": best_val,
    "path": best_path,
    "numChild": best_conf.numChild,
    "reorgStrat": best_conf.reorgStrat,
    "lcf": best_conf.lcf,
    "memOff": best_conf.memOff,
    "convTol": best_conf.convTol,
    "numIts": best_conf.numIts,
    "numSims": best_conf.numSims,
}

requests.post(url, params=params)
